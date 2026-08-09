from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from decimal import Decimal
import sist_bancario_hibrido.backend.app.db.models as models
import sist_bancario_hibrido.backend.app.schemas.schemas as schemas 

def obtener_cuenta(db: Session, numero_cuenta: str):
    """Devuelve los datos contables puros de la cuenta."""
    return db.query(models.Cuenta).filter(models.Cuenta.numero_cuenta == numero_cuenta).first()

def calcular_saldo_disponible(db: Session, numero_cuenta: str) -> Decimal:
    """
    Calcula el saldo real al vuelo: Saldo Contable (Mainframe) + Movimientos de HOY.
    """
    cuenta = obtener_cuenta(db, numero_cuenta)
    if not cuenta:
        return None

    # Obtenemos la fecha de hoy para filtrar
    hoy = date.today()

    # Buscamos todas las transacciones de esta cuenta hechas el día de HOY
    transacciones_hoy = db.query(models.Transaccion).filter(
        models.Transaccion.numero_cuenta == numero_cuenta,
        func.date(models.Transaccion.fecha_operacion) == hoy
    ).all()

    saldo_disponible = cuenta.saldo

    # Sumamos y restamos según el tipo de operación
    for tx in transacciones_hoy:
        if tx.tipo_operacion == 'D': # Depósito
            saldo_disponible += tx.monto
        elif tx.tipo_operacion in ('R', 'P'): # Retiro o Pago
            saldo_disponible -= tx.monto

    return saldo_disponible

def crear_transaccion(db: Session, transaccion: schemas.TransaccionCreate):
    """
    Registra una transacción validando primero si hay fondos suficientes.
    """
    #Calculamos cuánto dinero tiene REALMENTE disponible ahora mismo
    saldo_actual = calcular_saldo_disponible(db, transaccion.numero_cuenta)
    
    if saldo_actual is None:
        return {"error": "cuenta_no_encontrada"}
        
    if transaccion.tipo_operacion in ('R', 'P'):
        if transaccion.monto > saldo_actual:
            return {"error": "fondos_insuficientes"}

    #Si todo está bien, registramos la transacción (¡NO modificamos la tabla cuentas!)
    nueva_tx = models.Transaccion(
        numero_cuenta=transaccion.numero_cuenta,
        tipo_operacion=transaccion.tipo_operacion,
        monto=transaccion.monto
    )
    
    db.add(nueva_tx)
    db.commit()
    db.refresh(nueva_tx)
    
    return nueva_tx

def obtener_historial_transacciones(db: Session, numero_cuenta: str, skip: int = 0, limit: int = 10):
    """
    Devuelve las transacciones paginadas.
    skip: Cuántos registros me salto (Offset).
    limit: Cuántos registros traigo como máximo.
    """
    return db.query(models.Transaccion).filter(
        models.Transaccion.numero_cuenta == numero_cuenta
    ).order_by(
        models.Transaccion.fecha_operacion.desc()
    ).offset(skip).limit(limit).all()