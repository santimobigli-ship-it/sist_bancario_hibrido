import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 1- Cargar las variables desde el archivo .env
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

# Construir la URL de conexión dinámica
# Formato: mysql+pymysql://usuario:password@host:puerto/basededatos
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear el motor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear la sesión local para hacer las consultas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la que heredarán nuestros modelos (tablas)
Base = declarative_base()