import anthropic
from config import ANTHROPIC_API_KEY, BUSINESS_CONTEXT


client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def generate_dm_response(trigger_comment: str, username: str) -> str:
    """Genera una respuesta de DM personalizada basada en el comentario del usuario."""
    prompt = f"""
Un usuario llamado @{username} comentó en tu publicación de Instagram: "{trigger_comment}"

Escribe un mensaje directo (DM) para enviarle. El mensaje debe:
1. Saludar por su nombre de usuario
2. Agradecer su interés
3. Responder a su pregunta o curiosidad de forma breve
4. Invitarle a agendar una consulta de valoración

Solo responde con el texto del mensaje, sin explicaciones adicionales.
"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=BUSINESS_CONTEXT,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def generate_dm_reply(conversation_history: list[dict], new_message: str) -> str:
    """Genera una respuesta inteligente a un DM entrante con historial de conversación."""
    system_prompt = BUSINESS_CONTEXT + """

Para respuestas de DM:
- Sé conversacional y natural
- Si el paciente hace preguntas médicas específicas, invítalo a la consulta en lugar de diagnosticar
- Si pide agendar, proporciona el contacto directo: enlace de WhatsApp o Instagram
- Responde preguntas frecuentes comunes sobre rinoplastia ultrasónica
"""

    messages = conversation_history + [{"role": "user", "content": new_message}]

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        system=system_prompt,
        messages=messages,
    )
    return response.content[0].text
