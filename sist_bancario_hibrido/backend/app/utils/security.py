import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

# Obtenemos la clave secreta desde el .env
SECRET_KEY = os.getenv("SECRET_KEY", "clave_por_defecto_insegura")
ALGORITHM = "HS256"

def crear_token_recuperacion(email: str, expiracion_minutos: int = 15) -> str:
    """
    Genera un JWT firmado que contiene el email del usuario y expira en 15 minutos.
    """
    # Usamos timezone.utc para evitar problemas de zonas horarias en los servidores
    expire = datetime.now(timezone.utc) + timedelta(minutes=expiracion_minutos)
    
    
    to_encode = {"sub": email, "exp": expire}
    
    # Firmamos el token con nuestra clave secreta
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ... (imports y clave secreta quedan igual) ...

def verificar_token_recuperacion(token: str) -> dict:
    """
    Desencripta el token y verifica su validez.
    Devuelve un diccionario con el estado, el email (si es válido) o el error específico.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        return {
            "valido": True, 
            "email": email
        }
        
    except jwt.ExpiredSignatureError:
        # El token es de nuestro sistema, pero ya pasaron los 15 minutos
        return {
            "valido": False, 
            "error": "expirado",
            "mensaje": "El enlace ha expirado. Por favor, solicita uno nuevo."
        }
        
    except jwt.InvalidTokenError:
        # Alguien alteró el token en la URL o no tiene nuestra firma
        return {
            "valido": False, 
            "error": "invalido",
            "mensaje": "El enlace de recuperación es inválido o ha sido modificado."
        }