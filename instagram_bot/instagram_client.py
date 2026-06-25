import logging
import httpx
from config import INSTAGRAM_ACCESS_TOKEN

logger = logging.getLogger(__name__)

# Instagram Login flow — usa graph.instagram.com con el token IGAA... de la cuenta
BASE_URL = "https://graph.instagram.com/v21.0"


async def send_private_reply(comment_id: str, message_text: str) -> dict:
    """Envía un DM privado en respuesta a un comentario (Private Reply).

    NO requiere que el usuario haya escrito antes. Usa el comment_id como
    destinatario y tiene una ventana de 7 días. Solo requiere el permiso
    instagram_business_manage_comments.
    """
    url = f"{BASE_URL}/me/messages"
    payload = {
        "recipient": {"comment_id": comment_id},
        "message": {"text": message_text},
    }
    headers = {"Authorization": f"Bearer {INSTAGRAM_ACCESS_TOKEN}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        if not response.is_success:
            logger.error(f"Error Private Reply: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()


async def send_dm(recipient_instagram_id: str, message_text: str) -> dict:
    """Envía un DM a un usuario que ya inició conversación (ventana de 24h)."""
    url = f"{BASE_URL}/me/messages"
    payload = {
        "recipient": {"id": recipient_instagram_id},
        "message": {"text": message_text},
    }
    headers = {"Authorization": f"Bearer {INSTAGRAM_ACCESS_TOKEN}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        if not response.is_success:
            logger.error(f"Error DM: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()


async def reply_to_comment(comment_id: str, message: str) -> dict:
    """Responde públicamente a un comentario de Instagram."""
    url = f"{BASE_URL}/{comment_id}/replies"
    params = {"message": message}
    headers = {"Authorization": f"Bearer {INSTAGRAM_ACCESS_TOKEN}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
