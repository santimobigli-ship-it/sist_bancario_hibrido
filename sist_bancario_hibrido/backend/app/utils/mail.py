import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from dotenv import load_dotenv

# Cargamos las variables de entorno
load_dotenv()

# Configuramos la conexión SMTP
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def enviar_correo_recuperacion(email_destino: EmailStr, token: str):
    """
    Construye y envía el correo electrónico en formato HTML.
    """
    
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip('/')

    enlace = f"{frontend_url}/reset-password?token={token}"
    
    html = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #2c3e50;">Recuperación de Contraseña</h2>
        <p>Has solicitado restablecer tu contraseña en el Banco Híbrido.</p>
        <p>Haz clic en el siguiente enlace para continuar. Este enlace es seguro y temporal:</p>
        <a href="{enlace}" style="display: inline-block; padding: 10px 20px; background-color: #3498db; color: white; text-decoration: none; border-radius: 5px;">Restablecer mi contraseña</a>
        <p style="margin-top: 20px; font-size: 12px; color: #7f8c8d;">Si no solicitaste este cambio, puedes ignorar este correo de forma segura.</p>
    </div>
    """

    message = MessageSchema(
        subject="Recuperación de Contraseña - Banco Híbrido",
        recipients=[email_destino],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)