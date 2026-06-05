# OtorrinoCancun Instagram Bot

Automatización de Instagram para @otorrinocancun:
- **Comentarios con trigger → DM automático** generado por Claude
- **DMs entrantes → Respuesta inteligente** con historial de conversación

## Estructura

```
instagram_bot/
├── main.py              # Servidor FastAPI + webhook endpoints
├── claude_client.py     # Integración con Claude API
├── instagram_client.py  # Instagram Graph API (envío de DMs)
├── config.py            # Triggers, tokens, contexto del negocio
├── requirements.txt
└── .env.example
```

## Setup local

```bash
cd instagram_bot
pip install -r requirements.txt
cp .env.example .env
# Edita .env con tus tokens reales
uvicorn main:app --reload --port 8000
```

## Exponer el webhook localmente (para pruebas)

```bash
# Instala ngrok si no lo tienes
brew install ngrok
ngrok http 8000
# Copia la URL https://xxxx.ngrok.io y úsala en Meta Developers
```

## Configurar Meta App

### 1. Crear la App en Meta for Developers
- Ve a [developers.facebook.com](https://developers.facebook.com)
- Crea una app tipo **Business**
- Agrega el producto **Instagram**

### 2. Permisos necesarios
- `instagram_manage_comments` — leer comentarios
- `instagram_manage_messages` — enviar y recibir DMs
- `pages_messaging` — mensajería de página

### 3. Configurar Webhook
- URL: `https://tu-dominio.com/webhook`
- Verify Token: el valor de `WEBHOOK_VERIFY_TOKEN` en tu `.env`
- Suscribirse a: `comments`, `messages`

### 4. Obtener Access Token
- En Meta Business Suite → Configuración → Acceso a la API
- Genera un **Page Access Token** de larga duración

## Deploy en Railway (recomendado)

```bash
# Instala Railway CLI
npm install -g @railway/cli
railway login
railway init
railway up
# Agrega las variables de entorno en el dashboard de Railway
```

## Palabras trigger configuradas

Modifica `COMMENT_TRIGGERS` en `config.py`:

```python
COMMENT_TRIGGERS = ["info", "precio", "cita", "rinoplastia", "nariz", ...]
```

## Personalizar respuestas

Edita `BUSINESS_CONTEXT` en `config.py` para ajustar el tono y la información del bot.
