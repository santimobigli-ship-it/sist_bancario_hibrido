import os
from sqlalchemy import text
from app.db.database import engine
from app.utils.utils import limpiar_moneda_cobol
from app.config import RUTA_ERRORES, RUTA_SALDOS

def actualizar_bd_desde_cobol():
    """
    Fase 3: Lee los archivos de salida del Mainframe y actualiza MySQL.
    """
    
    print("Iniciando Fase 3: Actualizando Base de Datos...")

    # Usamos engine.begin() en lugar de engine.connect() 
    # Esto abre una Transacción (si algo falla en medio del for, se hace un Rollback automático)
    try:
        with engine.begin() as conexion:
            
            # 1. ACTUALIZAR SALDOS
            if os.path.exists(RUTA_SALDOS):
                with open(RUTA_SALDOS, "r", encoding='utf-8') as archivo_saldos:
                    for linea in archivo_saldos:
                        linea = linea.strip()
                        if not linea or "CUENTA" in linea or "-" * 5 in linea or 'REPORTE' in linea: 
                            continue
                        
                        cuenta = linea[0:8].strip()
                        
                        saldo_cobol = linea[10:20].strip() 
                        
                        nuevo_saldo = limpiar_moneda_cobol(saldo_cobol)

                        consulta_update = text("""
                            UPDATE cuentas 
                            SET saldo = :saldo 
                            WHERE numero_cuenta = :cuenta
                        """)
                        conexion.execute(consulta_update, {"saldo": nuevo_saldo, "cuenta": cuenta})
                
                print("Saldos actualizados en MySQL.")

            # 2. REGISTRAR EXCEPCIONES
            if os.path.exists(RUTA_ERRORES):
                with open(RUTA_ERRORES, "r", encoding='utf-8') as archivo_errores:
                    for linea in archivo_errores:
                        linea = linea.strip()
                        if not linea or "CUENTA" in linea or "REPORTE" in linea or "-" * 5 in linea: 
                            continue
                        
                        # Archivo LRECL=72 según tu diseño anterior
                        cuenta = linea[0:8].strip()
                        monto = linea[22:32].strip()
                        monto_formateado = limpiar_moneda_cobol(monto)
                        descripcion = linea[34:72].strip()

                        consulta_insert = text("""
                            INSERT INTO excepciones_batch (numero_cuenta, monto_intentado, motivo_rechazo)
                            VALUES (:cuenta, :monto, :motivo)
                        """)
                        conexion.execute(consulta_insert, {
                            "cuenta": cuenta, 
                            "monto": monto_formateado, 
                            "motivo": descripcion
                        })
                
                print("Excepciones registradas en MySQL (si las hubo).")

        print("FASE 3 COMPLETADA: El ciclo ETL ha finalizado con éxito.")

    except Exception as e:
        print(f"ERROR CRÍTICO en la actualización de la BD: {e}")