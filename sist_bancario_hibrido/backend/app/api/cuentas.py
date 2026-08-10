from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud import crud
from app.schemas import schemas

router = APIRouter(
    prefix="/cuentas",
    tags=["Cuentas"]
)

@router.post("/", response_model=schemas.CuentaResponse, status_code=status.HTTP_201_CREATED)
def crear_nueva_cuenta(cuenta: schemas.CuentaCreate, db: Session = Depends(get_db)):
    """
    Crea una cuenta nueva. Valida que el número de cuenta no exista previamente.
    """
    # Verificamos que el número de cuenta no esté tomado
    cuenta_existente = crud.obtener_cuenta(db, numero_cuenta=cuenta.numero_cuenta)
    if cuenta_existente:
        raise HTTPException(status_code=400, detail="El número de cuenta ya está registrado.")
    
    return crud.crear_cuenta(db=db, cuenta=cuenta)

@router.post("/login")
def iniciar_sesion(credenciales: schemas.CuentaLogin, db: Session = Depends(get_db)):
    """
    Valida las credenciales del usuario.
    (En un entorno real, aquí devolveríamos un Token JWT. Por ahora devolvemos un mensaje de éxito).
    """
    cuenta_valida = crud.autenticar_cuenta(db, credenciales.numero_cuenta, credenciales.password)
    
    if not cuenta_valida:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Número de cuenta o contraseña incorrectos."
        )
        
    return {
        "mensaje": "Login exitoso", 
        "cuenta": credenciales.numero_cuenta
    }

@router.put("/{numero_cuenta}/password")
def cambiar_contrasena(
    numero_cuenta: str, 
    passwords: schemas.CuentaUpdatePassword, 
    db: Session = Depends(get_db)
):
    """
    Permite a un usuario cambiar su contraseña validando la anterior.
    """
    # Primero usamos la misma lógica de login para validar la identidad
    cuenta_valida = crud.autenticar_cuenta(db, numero_cuenta, passwords.password_actual)
    
    if not cuenta_valida:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="La contraseña actual es incorrecta."
        )
        
    # Si todo está bien, la actualizamos
    crud.actualizar_password(db, numero_cuenta, passwords.password_nueva)
    
    return {"mensaje": "Contraseña actualizada correctamente"}