# main.py (El archivo principal de tu FastAPI)
from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from sist_bancario_hibrido.backend.PROCESO_ETL.etl import ejecutar_proceso_etl 

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

@app.get("/")
def read_root():
    return {"mensaje": "Backend Home Banking Operativo"}