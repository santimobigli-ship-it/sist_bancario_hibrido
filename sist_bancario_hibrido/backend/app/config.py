import os
from dotenv import load_dotenv

load_dotenv()

# 1. Python descubre dónde está parado de forma dinámica
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. Lee del .env el nombre de la carpeta (o usa 'core_cobol/data' por defecto)
CARPETA_DATOS = os.getenv("CARPETA_DATOS_COBOL", "core_cobol/data")

# 3. Construye la ruta final, a prueba de balas y portátil
RUTA_BASE_DATOS = os.path.join(BASE_DIR, CARPETA_DATOS)

# Rutas específicas listas para usar en todo tu proyecto:
RUTA_TRANSACCIONES = os.path.join(RUTA_BASE_DATOS, "TRANSACC.txt")
RUTA_SALDOS = os.path.join(RUTA_BASE_DATOS, "SALDOS.txt")
RUTA_ERRORES = os.path.join(RUTA_BASE_DATOS, "ERRORES.txt")