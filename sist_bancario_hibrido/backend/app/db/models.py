from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sist_bancario_hibrido.backend.app.db.database import Base  

# ==========================================
# MODELO: CUENTAS
# ==========================================
class Cuenta(Base):
    __tablename__ = "cuentas"

    numero_cuenta = Column(String(8), primary_key=True, index=True)
    titular = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    saldo = Column(Numeric(7, 2), nullable=False, default=0.00)
    ultima_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    transacciones = relationship("Transaccion", back_populates="cuenta")


# ==========================================
# MODELO: TRANSACCIONES
# ==========================================
class Transaccion(Base):
    __tablename__ = "transacciones"

    id_transaccion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    numero_cuenta = Column(String(8), ForeignKey("cuentas.numero_cuenta"), nullable=False)
    tipo_operacion = Column(String(1), nullable=False)
    monto = Column(Numeric(7, 2), nullable=False)
    fecha_operacion = Column(DateTime, server_default=func.now())

    cuenta = relationship("Cuenta", back_populates="transacciones")


# ==========================================
# MODELO: EXCEPCIONES BATCH (ERRORES COBOL)
# ==========================================
class ExcepcionBatch(Base):
    __tablename__ = "excepciones_batch"

    id_error = Column(Integer, primary_key=True, index=True, autoincrement=True)
    numero_cuenta = Column(String(8), nullable=False)
    monto_intentado = Column(Numeric(7, 2))
    motivo_rechazo = Column(String(38))
    fecha_procesamiento = Column(DateTime, server_default=func.now())