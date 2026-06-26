import anthropic
from config import ANTHROPIC_API_KEY, BUSINESS_CONTEXT

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Cierre fijo que se agrega a TODAS las respuestas — no depende de Claude
FIXED_CLOSING = """

📅 ¿Te gustaría agendar tu consulta de valoración?
👉 https://na.doct.to/ts13gauy
🕐 Lun-Vie 10:30am-5pm | Sáb 10:30am-2pm
💬 WhatsApp: https://wa.me/529981480332"""

# Respuesta automática cuando el paciente envía una foto — la revisa el Dr.
# (NO lleva cierre fijo: el paciente está en el flujo de proyección, no agendando)
PHOTO_ACK = (
    "¡Gracias por compartir tu foto! 📸 El Dr. Montalvo revisará tu caso "
    "personalmente y te responderá en la brevedad posible. 😊"
)


def generate_dm_response(trigger_comment: str, username: str) -> str:
    """Genera una respuesta de DM personalizada basada en el comentario del usuario."""
    prompt = f"""
Un usuario comentó en tu publicación de Instagram: "{trigger_comment}"

Escribe un mensaje directo (DM) para enviarle, siguiendo TODAS las reglas de tono y enfoque. El mensaje debe:
1. Saludar de forma breve y neutra (sin asumir género, sin "Bienvenido" y sin el emoji 👋)
2. Como el interés es sobre rinoplastia, ofrecer la proyección con foto (una foto de perfil y una de frente, sin compromiso, por este mismo medio) y, si lo prefiere, ayudarle a agendar su consulta de valoración
3. NO incluyas al final ningún contacto, link ni forma de agendar — eso se agrega automáticamente

Solo responde con el texto del mensaje, sin explicaciones adicionales.
"""
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=BUSINESS_CONTEXT,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text + FIXED_CLOSING


def generate_dm_reply(conversation_history: list[dict], new_message: str) -> str:
    """Genera una respuesta inteligente a un DM entrante con historial de conversación."""
    system_prompt = BUSINESS_CONTEXT + """

Para respuestas de DM:
- Sé conversacional y natural
- Si el paciente hace preguntas médicas específicas, invítalo a la consulta en lugar de diagnosticar
- NO incluyas al final ningún contacto, link ni forma de agendar — eso se agrega automáticamente
- Responde preguntas frecuentes comunes sobre rinoplastia ultrasónica
"""
    messages = conversation_history + [{"role": "user", "content": new_message}]

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        system=system_prompt,
        messages=messages,
    )
    return response.content[0].text + FIXED_CLOSING
