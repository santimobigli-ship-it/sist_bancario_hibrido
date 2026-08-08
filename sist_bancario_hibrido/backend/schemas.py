from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from decimal import Decimal

# ==========================================
# ESQUEMAS PARA CUENTAS
# ==========================================
class CuentaBase(BaseModel):
    numero_cuenta: str = Field(..., max_length=8, description="Número de cuenta exacto de 8 dígitos")
    titular: str = Field(..., max_length=100)
    saldo: Decimal = Field(default=Decimal('0.00'), max_digits=7, decimal_places=2)

class CuentaCreate(CuentaBase):
    """Esquema para crear una cuenta nueva"""
    pass

class CuentaResponse(CuentaBase):
    """Esquema para devolver datos de la cuenta al usuario"""
    ultima_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# ESQUEMAS PARA TRANSACCIONES
# ==========================================
class TransaccionBase(BaseModel):
    numero_cuenta: str = Field(..., max_length=8)
    tipo_operacion: str = Field(..., max_length=1, description="D: Depósito, R: Retiro, P: Pago")
    monto: Decimal = Field(..., gt=0, max_digits=7, decimal_places=2)

class TransaccionCreate(TransaccionBase):
    """Esquema para que el usuario envíe una nueva transacción desde la web"""
    pass

class TransaccionResponse(TransaccionBase):
    """Esquema de respuesta al consultar el historial de transacciones"""
    id_transaccion: int
    fecha_operacion: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# ESQUEMAS PARA EXCEPCIONES BATCH
# ==========================================
class ExcepcionBatchResponse(BaseModel):
    """Las excepciones son de solo lectura, no necesitamos un esquema 'Create'"""
    id_error: int
    numero_cuenta: str
    monto_intentado: Decimal
    motivo_rechazo: str
    fecha_procesamiento: datetime

    model_config = ConfigDict(from_attributes=True)