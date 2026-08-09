import os
from sqlalchemy import text
from sist_bancario_hibrido.backend.app.db.database import engine
from sist_bancario_hibrido.backend.app.utils.utils import formatear_para_cobol
from sist_bancario_hibrido.backend.app.config import RUTA_TRANSACCIONES

def generar_archivo_transacciones():
    # Subimos un nivel para llegar a core-cobol/data/
    os.makedirs(os.path.dirname(RUTA_TRANSACCIONES), exist_ok=True)
    
    # Consulta SQL par obtener las transacciones
    consulta_sql = text("""
        SELECT t.numero_cuenta, t.tipo_operacion, c.saldo AS saldo_inicial, t.monto
        FROM transacciones t
        JOIN cuentas c ON t.numero_cuenta = c.numero_cuenta
        WHERE DATE(t.fecha_operacion) = CURDATE() - INTERVAL 1 DAY
        ORDER BY t.numero_cuenta ASC
    """)

    try:
        with engine.connect() as conexion:
            resultados = conexion.execute(consulta_sql).fetchall()
            
            # Si no hubo transacciones ayer, evitamos generar un archivo basura, priorizando el rendimiento y evitando errores en COBOL.
            if not resultados:
                print("No hubo transacciones el día de ayer. No se requiere procesamiento Batch.")
                return False

            with open(RUTA_TRANSACCIONES, "w", encoding='utf-8') as archivo:
                for fila in resultados:
                    cuenta = str(fila.numero_cuenta).ljust(8)  
                    tipo = str(fila.tipo_operacion)            
                    saldo = formatear_para_cobol(fila.saldo_inicial) 
                    monto = formatear_para_cobol(fila.monto)         
                    
                    linea = f"{cuenta}{tipo}{saldo}{monto}\n"
                    archivo.write(linea)
                    
        print(f"ÉXITO: Se extrajeron {len(resultados)} transacciones de AYER y se preparó el lote para que COBOL lo procese.")
        return True
        
    except Exception as e:
        print(f"ERROR generando el archivo batch: {e}")
