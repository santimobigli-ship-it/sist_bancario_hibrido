def formatear_para_cobol(valor_decimal):
    """
    Transforma un decimal (ej: 150.50) al formato PIC 9(05)V99 (ej: 0015050)
    ocupando exactamente 7 caracteres sin el punto decimal.
    """
    if valor_decimal is None:
        valor_decimal = 0.00
    
    # Multiplicamos por 100 para eliminar decimales y convertimos a entero
    centavos = int(round(float(valor_decimal) * 100))
    # Formateamos a 7 dígitos con ceros a la izquierda para cumplir con PIC 9(05)V99
    return f"{centavos:07d}" #f"{entavos:07d}" asegura que siempre tenga 7 dígitos, rellenando con ceros a la izquierda si es necesario."

def parsear_de_cobol(valor_cobol):
    """
    Transforma un string PIC 9(05)V99 de COBOL (ej: '0015050')
    de vuelta a un decimal de Python (ej: 150.50).
    """
    if not valor_cobol or not valor_cobol.isdigit():
        return 0.00
    
    # Convertimos a entero y dividimos por 100
    return float(valor_cobol) / 100.0

# utils.py (Agregar esta nueva función)

def limpiar_moneda_cobol(valor_str):
    """
    Convierte una cadena con máscara de edición COBOL (ej: PIC $$$,$$9.99)
    como '  $1,250.50' en un valor decimal nativo de Python (1250.50).
    """
    if not valor_str or not valor_str.strip():
        return 0.00
        
    # 1. Quitamos espacios en blanco de los extremos
    # 2. Eliminamos el símbolo del dólar
    # 3. Eliminamos las comas de los miles
    valor_limpio = valor_str.strip().replace('$', '').replace(',', '')
    
    try:
        # Convertimos a float de forma segura
        return float(valor_limpio)
    except ValueError:
        print(f"ADVERTENCIA: No se pudo convertir el valor COBOL '{valor_str}' a decimal.")
        return 0.00