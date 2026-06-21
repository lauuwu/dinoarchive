import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger("dinoarchive.email")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_NAME = os.getenv("SMTP_FROM_NAME", "DinoArchive")


def send_welcome_email(to_email: str, username: str) -> bool:
    """
    Envía un email de bienvenida cuando un usuario se registra.

    Importante: nunca lanza una excepción hacia afuera. Si el SMTP no está
    configurado o falla, el registro del usuario debe poder completarse
    igual; solo se loguea el error.
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.warning(
            "SMTP_USER/SMTP_PASSWORD no configurados. Email de bienvenida "
            "NO enviado a %s (usuario: %s).", to_email, username
        )
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "¡Bienvenido a DinoArchive! 🦕"
    msg["From"] = f"{FROM_NAME} <{SMTP_USER}>"
    msg["To"] = to_email

    text = (
        f"Hola {username},\n\n"
        "Tu cuenta en DinoArchive fue creada con éxito.\n"
        "Ya podés iniciar sesión, explorar especies y sumar puntos en los quizzes.\n\n"
        "— El equipo de DinoArchive"
    )
    html = f"""
    <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto; color: #222;">
      <h2>🦕 ¡Bienvenido a DinoArchive, {username}!</h2>
      <p>Tu cuenta fue creada con éxito. Ya podés iniciar sesión, explorar
      especies y poner a prueba lo que sabés en los quizzes para subir en
      el ranking.</p>
      <p style="color:#7fae6f;">— El equipo de DinoArchive</p>
    </div>
    """

    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to_email, msg.as_string())
        logger.info("Email de bienvenida enviado a %s", to_email)
        return True
    except Exception as exc:
        logger.error("No se pudo enviar el email de bienvenida a %s: %s", to_email, exc)
        return False
