"""Sección Declarativa: Programa que se correra a las 00.00hs para extraer las transacciones dle dia anterior asi el mainframe puede procesarlas en batch,
y asi actualizar los saldos de las cuentas. Se ejecuta en el backend de python y genera un archivo ordenado de las transacciones del dia anterior."""

from sist_bancario_hibrido.backend.PROCESO_ETL.COMUNICACION_MAINFRAME.generar_archivo_transacciones import generar_archivo_transacciones
from sist_bancario_hibrido.backend.PROCESO_ETL.COMUNICACION_MAINFRAME.ejecutar_JCL import ejecutar_batch_mainframe
from sist_bancario_hibrido.backend.PROCESO_ETL.COMUNICACION_MAINFRAME.actualizar_db import actualizar_bd_desde_cobol

def ejecutar_proceso_etl():
    print("Iniciando proceso ETL nocturno...")
    datos = generar_archivo_transacciones()
    
    if datos:
        exito_con_mainframe = ejecutar_batch_mainframe()
        if exito_con_mainframe:
           actualizar_bd_desde_cobol()
        else:
            "Error al ejecutar el programa COBOl en el mainframe"
    else:
        print("ETL Cancelado: No hay datos para procesar.")
if __name__ == "__main__":
    ejecutar_proceso_etl()