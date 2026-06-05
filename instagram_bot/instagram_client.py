import httpx
from config import INSTAGRAM_ACCESS_TOKEN


BASE_URL = "https://graph.facebook.com/v21.0"


async def send_dm(recipient_instagram_id: str, message_text: str) -> dict:
    """Envía un DM a un usuario de Instagram por su IGSID (Instagram-scoped ID)."""
    url = f"{BASE_URL}/me/messages"
    payload = {
        "recipient": {"id": recipient_instagram_id},
        "message": {"text": message_text},
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
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
