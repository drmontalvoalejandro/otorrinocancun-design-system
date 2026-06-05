import logging
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import PlainTextResponse

from config import WEBHOOK_VERIFY_TOKEN, COMMENT_TRIGGERS
from claude_client import generate_dm_response, generate_dm_reply
from instagram_client import send_dm, get_user_profile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="OtorrinoCancun Instagram Bot")

# Almacén en memoria de conversaciones de DM (en producción usa Redis/DB)
# { instagram_scoped_id: [{"role": "user"|"assistant", "content": "..."}] }
dm_conversations: dict[str, list[dict]] = {}


def contains_trigger(text: str) -> bool:
    text_lower = text.lower()
    return any(trigger in text_lower for trigger in COMMENT_TRIGGERS)


@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    """Endpoint de verificación requerido por Meta al configurar el webhook."""
    if hub_mode == "subscribe" and hub_verify_token == WEBHOOK_VERIFY_TOKEN:
        logger.info("Webhook verificado exitosamente")
        return PlainTextResponse(hub_challenge)
    raise HTTPException(status_code=403, detail="Token de verificación incorrecto")


@app.post("/webhook")
async def handle_webhook(request: Request):
    """Recibe eventos de Instagram: comentarios y mensajes directos."""
    body = await request.json()
    logger.info(f"Webhook recibido: {body}")

    for entry in body.get("entry", []):
        # --- Manejo de COMENTARIOS ---
        for change in entry.get("changes", []):
            if change.get("field") == "comments":
                await handle_comment(change["value"])

        # --- Manejo de MENSAJES DIRECTOS ---
        for messaging in entry.get("messaging", []):
            if "message" in messaging:
                await handle_dm(messaging)

    return {"status": "ok"}


async def handle_comment(comment_data: dict):
    """Procesa un comentario entrante. Si tiene trigger, envía DM automático."""
    comment_text = comment_data.get("text", "")
    commenter_id = comment_data.get("from", {}).get("id")
    commenter_username = comment_data.get("from", {}).get("username", "amigo")

    if not commenter_id or not comment_text:
        return

    logger.info(f"Comentario de @{commenter_username}: {comment_text}")

    if not contains_trigger(comment_text):
        logger.info("Sin trigger detectado, ignorando comentario")
        return

    logger.info(f"Trigger detectado! Generando DM para @{commenter_username}")

    # Generar respuesta con Claude
    dm_text = generate_dm_response(
        trigger_comment=comment_text,
        username=commenter_username,
    )

    # Enviar DM
    try:
        result = await send_dm(recipient_instagram_id=commenter_id, message_text=dm_text)
        logger.info(f"DM enviado exitosamente: {result}")
    except Exception as e:
        logger.error(f"Error enviando DM a {commenter_id}: {e}")


async def handle_dm(messaging: dict):
    """Procesa un DM entrante y responde con Claude."""
    sender_id = messaging["sender"]["id"]
    message_text = messaging.get("message", {}).get("text", "")

    if not message_text:
        return

    logger.info(f"DM de {sender_id}: {message_text}")

    # Recuperar o inicializar historial de conversación
    history = dm_conversations.get(sender_id, [])

    # Generar respuesta con Claude
    reply = generate_dm_reply(
        conversation_history=history,
        new_message=message_text,
    )

    # Actualizar historial
    history.append({"role": "user", "content": message_text})
    history.append({"role": "assistant", "content": reply})
    # Mantener solo los últimos 10 turnos para no sobrecargar el contexto
    dm_conversations[sender_id] = history[-10:]

    # Enviar respuesta
    try:
        await send_dm(recipient_instagram_id=sender_id, message_text=reply)
        logger.info(f"Respuesta DM enviada a {sender_id}")
    except Exception as e:
        logger.error(f"Error respondiendo DM a {sender_id}: {e}")


@app.get("/health")
async def health():
    return {"status": "running", "bot": "OtorrinoCancun Instagram Bot"}
