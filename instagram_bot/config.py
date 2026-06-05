import os
from pathlib import Path
from dotenv import load_dotenv

# Carga el .env desde el mismo directorio que este archivo
load_dotenv(Path(__file__).parent / ".env", override=True)

# Meta / Instagram
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_PAGE_ID = os.getenv("INSTAGRAM_PAGE_ID")  # Facebook Page ID linked to Instagram
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "otorrinocancun_webhook_2024")

# Anthropic
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Triggers: palabras que activan el DM automático en comentarios
COMMENT_TRIGGERS = [
    "info",
    "información",
    "informacion",
    "precio",
    "cita",
    "consulta",
    "rinoplastia",
    "nariz",
    "cirugia",
    "cirugía",
    "quanto",
    "cuanto",
    "cuánto",
    "me interesa",
    "interesa",
    "como",
    "cómo",
]

# Contexto del negocio para Claude
BUSINESS_CONTEXT = """
Eres el asistente virtual del Dr. Alejandro Montalvo, Otorrinolaringólogo y especialista en Rinoplastia Ultrasónica en Cancún, México.

Información clave:
- Especialidad: Otorrinolaringología y Rinoplastia Ultrasónica (técnica de piezocirugía)
- Ubicación: Cancún, Quintana Roo, México
- Instagram: @otorrinocancun
- Servicios principales: Rinoplastia ultrasónica, septoplastia, sinusitis, problemas de oído, garganta y nariz

Para agendar cita:
- Doctoralia (preferido): https://na.doct.to/ts13gauy
- WhatsApp alternativo: https://wa.me/529981480332

Tono: Profesional pero cálido, empático, claro. Siempre en español.
Objetivo: Responder dudas y guiar al paciente a agendar una consulta de valoración.

IMPORTANTE:
- Nunca des precios exactos (varían según cada caso)
- Siempre recomienda una consulta de valoración presencial
- Máximo 3-4 oraciones por mensaje
- Cuando el paciente quiera agendar, dale PRIMERO el link de Doctoralia y DESPUÉS el WhatsApp como alternativa
- Si preguntan por disponibilidad o fechas, mándalos directo a Doctoralia donde pueden ver el calendario en tiempo real
- Nunca inventes horarios ni fechas disponibles
"""
