from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db 
from app.crud import crud
from app.schemas import schemas


router = APIRouter(
    prefix="/transacciones",
    tags=["Transacciones"]
)

@router.post("/", response_model=schemas.TransaccionResponse, status_code=status.HTTP_201_CREATED)
def realizar_transaccion(transaccion: schemas.TransaccionCreate, db: Session = Depends(get_db)):
    """
    Registra un retiro, depósito o pago. Valida fondos disponibles al vuelo.
    """
    nueva_tx = crud.crear_transaccion(db=db, transaccion=transaccion)
    
    if type(nueva_tx) is dict:
        if nueva_tx.get("error") == "cuenta_no_encontrada":
            raise HTTPException(status_code=404, detail="La cuenta especificada no existe.")
        if nueva_tx.get("error") == "fondos_insuficientes":
            raise HTTPException(status_code=400, detail="Fondos insuficientes para esta operación.")
            
    return nueva_tx

@router.get("/{numero_cuenta}", response_model=List[schemas.TransaccionResponse])
def ver_historial(numero_cuenta: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Devuelve el historial de transacciones de una cuenta con paginación.
    """
    # Verificamos si la cuenta existe primero
    cuenta = crud.obtener_cuenta(db, numero_cuenta=numero_cuenta)
    if not cuenta:
        raise HTTPException(status_code=404, detail="La cuenta especificada no existe.")
        
    transacciones = crud.obtener_historial_transacciones(db, numero_cuenta=numero_cuenta, skip=skip, limit=limit)
    return transacciones