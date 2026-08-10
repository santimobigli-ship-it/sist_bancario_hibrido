from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from sist_bancario_hibrido.backend.PROCESO_ETL.etl import ejecutar_proceso_etl 
from app.api import cuentas, transacciones
from app.db import models
from app.db.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Esto se ejecuta CUANDO ARRANCA el backend, inicia el reloj interno y le dice que ejecute ese proceso a las 00:01
    print("Iniciando reloj interno (APScheduler)...")
    scheduler = BackgroundScheduler()
    
    # Programamos la tarea para las 00:00
    scheduler.add_job(ejecutar_proceso_etl, 'cron', hour=0, minute=1)
    scheduler.start()
    
    yield # Aquí FastAPI se queda escuchando peticiones de los usuarios, mientras espera a que se apague el backend continua respondiendo al resto de peticiones http.
    
    # Esto se ejecuta CUANDO APAGAS el contenedor de Docker
    print("Apagando reloj interno...")
    scheduler.shutdown()

# Iniciamos FastAPI pasándole el ciclo de vida (lifespan), asi se configura esto que dijimos antes de que se eejcute el proceso a esa hora y a la hora de apagar el contenedor no quedan procesos fantasmas.
app = FastAPI(lifespan=lifespan)

# ==========================================
# INICIALIZACIÓN DE LA BASE DE DATOS
# ==========================================
# Crea las tablas en MySQL si no existen (ideal para desarrollo)
models.Base.metadata.create_all(bind=engine)

# ==========================================
# INSTANCIA DE FASTAPI
# ==========================================
app = FastAPI(
    lifespan=lifespan,
    title="API Core Bancario Híbrido",
    description="Backend transaccional con soporte para procesamiento Batch (COBOL).",
    version="1.0.0"
)

# ==========================================
# REGISTRO DE ROUTERS (Tus endpoints)
# ==========================================
app.include_router(cuentas.router)
app.include_router(transacciones.router)

# ==========================================
# RUTA RAÍZ (Health Check)
# ==========================================
@app.get("/", tags=["Inicio"])
def root():
    return {
        "estado": "Online",
        "mensaje": "Bienvenido al Core Bancario Híbrido. Ve a /docs para ver la documentación de la API."
    }