from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import datetime
from decimal import Decimal
from typing import Literal


# ==========================================
# ESQUEMAS PARA CUENTAS
# ==========================================
class CuentaBase(BaseModel):
    numero_cuenta: str = Field(..., max_length=8, description="Número de cuenta exacto de 8 dígitos")
    titular: str = Field(..., max_length=100)
    email: EmailStr = Field(..., description="Correo electrónico del usuario") 
    saldo: Decimal = Field(default=Decimal('0.00'), max_digits=7, decimal_places=2)

class CuentaCreate(BaseModel):
    """Esquema para crear cuenta. El usuario envía sus datos y contraseña."""
    numero_cuenta: str = Field(..., max_length=8)
    titular: str = Field(..., max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    

class CuentaResponse(CuentaBase):
    """Esquema para devolver datos de la cuenta al usuario"""
    ultima_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)
    
class CuentaLogin(BaseModel):
    """Esquema para que el usuario inicie sesión solo con Email y Password"""
    email: EmailStr
    password: str

class SolicitudRecuperacion(BaseModel):
    """Esquema para solicitar el mail de recuperación"""
    email: EmailStr

class ResetPassword(BaseModel):
    """Esquema para guardar la nueva contraseña usando el token del email"""
    token: str = Field(..., description="El token de seguridad enviado por email")
    password_nueva: str = Field(..., min_length=6)
    password_confirmacion: str = Field(..., min_length=6)


# ==========================================
# ESQUEMAS PARA TRANSACCIONES
# ==========================================
class TransaccionBase(BaseModel):
    numero_cuenta: str = Field(..., max_length=8)
    tipo_operacion: Literal['D', 'R', 'P'] = Field(..., description="D: Depósito, R: Retiro, P: Pago")
    monto: Decimal = Field(..., gt=0, max_digits=7, decimal_places=2)

class TransaccionCreate(TransaccionBase):
    """Esquema para que el usuario envíe una nueva transacción desde la web"""
    pass

class TransaccionResponse(TransaccionBase):
    """Esquema de respuesta al consultar el historial de transacciones"""
    id_transaccion: int
    fecha_operacion: datetime

    model_config = ConfigDict(from_attributes=True)
