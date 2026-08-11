from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud import crud
from app.schemas import schemas
from app.utils.mail import enviar_correo_recuperacion
from app.utils.security import crear_token_recuperacion, verificar_token_recuperacion

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
    
    if crud.obtener_cuenta_por_email(db, email=cuenta.email):
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")
    
    return crud.crear_cuenta(db=db, cuenta=cuenta)

@router.post("/login")
def iniciar_sesion(credenciales: schemas.CuentaLogin, db: Session = Depends(get_db)):
    """
    Valida las credenciales del usuario.
    (En un entorno real, aquí devolveríamos un Token JWT. Por ahora devolvemos un mensaje de éxito).
    """
    cuenta_valida = crud.autenticar_cuenta(db, credenciales.email, credenciales.password)
    
    if not cuenta_valida:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email o contraseña incorrectos."
        )
        
    return {
        "mensaje": "Login exitoso", 
        "cuenta": cuenta_valida.numero_cuenta,
        "email": cuenta_valida.email,
        "titular": cuenta_valida.titular
    }
@router.post("/recuperar-password")
async def solicitar_recuperacion(
    solicitud: schemas.SolicitudRecuperacion, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    """
    Recibe el email y envía un correo con un JWT criptográfico.
    """
    cuenta = crud.obtener_cuenta_por_email(db, solicitud.email)
    
    if cuenta:
        # 1. Generamos el JWT real válido por 15 minutos
        token_seguro = crear_token_recuperacion(email=cuenta.email)
        
        # 2. Enviamos el correo de fondo con el enlace firmado
        background_tasks.add_task(enviar_correo_recuperacion, cuenta.email, token_seguro)

    return {"mensaje": "Si el correo está registrado, recibirás un enlace de recuperación en breve."}

@router.put("/reset-password")
def resetear_password(datos: schemas.ResetPassword, db: Session = Depends(get_db)):
    """
    Valida el JWT y permite cambiar la contraseña si todo es correcto.
    """
    # 1. Validamos que las contraseñas escritas coincidan
    if datos.password_nueva != datos.password_confirmacion:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden.")
        
    # 2. Verificamos la firma criptográfica
    resultado_token = verificar_token_recuperacion(datos.token)
    
    # 3. Manejo de errores específico
    if not resultado_token["valido"]:
        # Aquí arrojamos el error 400, pero con el mensaje exacto (expirado o inválido)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=resultado_token["mensaje"]
        )
        
    # Si es válido, extraemos el email del diccionario
    email_extraido = resultado_token["email"]
    
    # 4. Verificamos que la cuenta aún exista en la base de datos
    cuenta = crud.obtener_cuenta_por_email(db, email_extraido)
    if not cuenta:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        
    # 5. Actualizamos la contraseña forzosamente
    crud.actualizar_password(db, email_extraido, datos.password_nueva)
    
    return {"mensaje": "Contraseña actualizada correctamente. Ya puedes iniciar sesión."}