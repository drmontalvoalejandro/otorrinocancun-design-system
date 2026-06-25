import logging
import httpx
from config import INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_BUSINESS_ID

logger = logging.getLogger(__name__)

BASE_URL = "https://graph.facebook.com/v21.0"


async def send_private_reply(comment_id: str, message_text: str) -> dict:
    """Envía un DM privado en respuesta a un comentario (Private Reply).

    A diferencia de send_dm, esto NO requiere que el usuario haya escrito antes.
    Usa el comment_id como destinatario y tiene una ventana de 7 días.
    Solo requiere el permiso instagram_manage_comments.
    """
    url = f"{BASE_URL}/{INSTAGRAM_BUSINESS_ID}/messages"
    payload = {
        "recipient": {"comment_id": comment_id},
        "message": {"text": message_text},
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        if not response.is_success:
            logger.error(f"Error Private Reply: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()


async def send_dm(recipient_instagram_id: str, message_text: str) -> dict:
    """Envía un DM a un usuario de Instagram usando la API de Instagram directa."""
    import logging
    logger = logging.getLogger(__name__)
    from config import INSTAGRAM_PAGE_ID

    # Intentar con el endpoint de Instagram directo (v21.0)
    url = f"{BASE_URL}/{INSTAGRAM_PAGE_ID}/messages"
    payload = {
        "recipient": {"id": recipient_instagram_id},
        "message": {"text": message_text},
        "access_token": INSTAGRAM_ACCESS_TOKEN,
        "messaging_type": "RESPONSE",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        if not response.is_success:
            logger.error(f"Error API: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()


async def reply_to_comment(comment_id: str, message: str) -> dict:
    """Responde públicamente a un comentario de Instagram."""
    url = f"{BASE_URL}/{comment_id}/replies"
    params = {
        "message": message,
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, params=params)
        response.raise_for_status()
        return response.json()


async def get_user_profile(instagram_scoped_id: str) -> dict:
    """Obtiene el perfil básico de un usuario (nombre, username)."""
    url = f"{BASE_URL}/{instagram_scoped_id}"
    params = {
        "fields": "name,username",
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()
