import subprocess
from app.config import RUTA_TRANSACCIONES, RUTA_ERRORES, RUTA_SALDOS

def ejecutar_batch_mainframe():
    """
    Fase 2: Se comunica con z/OS usando Zowe CLI para subir el lote,
    procesarlo y descargar los resultados.
    """
    print("Iniciando Fase 2: Sincronización con Mainframe...")

    try:
        # 1. Subir el archivo de transacciones al Dataset del Mainframe
        print("   -> Subiendo TRANSACC.txt...")
        subprocess.run([
            "zowe", "zos-files", "upload", "file-to-data-set", 
            RUTA_TRANSACCIONES, 
            "Z89300.DATOS.TRANSACC" # <-- Cambia esto por tu usuario/dataset real
        ], check=True) #lo subimos como una lista de string el comand, asi evitamos inyecciones de comandos ademas check=True hace que si fall el comando se detiene el programa y lanza una excepcion.

        # 2. Enviar el JCL para ejecutar el programa COBOL y esperar a que termine
        print("   -> Ejecutando JCL (BANCOCOR)...")
        subprocess.run([
            "zowe", "zos-jobs", "submit", "data-set", 
            "Z89300.JCL(RUNBANCO)", 
            "--wait-for-output"
        ], check=True)

        # 3. Descargar el archivo de Saldos actualizados
        print("   -> Descargando SALDOS...")
        subprocess.run([
            "zowe", "zos-files", "download", "data-set", 
            "Z89300.DATOS.SALDOS", 
            "-f", RUTA_SALDOS, "--overwrite"
        ], check=True)

        # 4. Descargar el archivo de Errores (si los hubo)
        print("   -> Descargando ERRORES...")
        subprocess.run([
            "zowe", "zos-files", "download", "data-set", 
            "Z89300.DATOS.ERRORES", 
            "-f", RUTA_ERRORES, "--overwrite"
        ], check=True)

        print("FASE 2 COMPLETADA: Archivos del Mainframe listos en local.")
        return True

    except subprocess.CalledProcessError as e:
        print(f"ERROR crítico de comunicación con el Mainframe: {e}")
        return False
