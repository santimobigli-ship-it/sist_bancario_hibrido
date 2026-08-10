-- 1. Crear la base de datos
CREATE DATABASE IF NOT EXISTS banco_hibrido;
USE banco_hibrido;

-- 2. Tabla de Cuentas (Aquí guardaremos el saldo que actualiza COBOL)
CREATE TABLE cuentas (
    numero_cuenta VARCHAR(8) PRIMARY KEY,
    titular VARCHAR(100) NOT NULL,
    saldo DECIMAL(7, 2) NOT NULL DEFAULT 0.00,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 3. Tabla de Transacciones (Historial para el Home Banking)
CREATE TABLE transacciones (
    id_transaccion INT AUTO_INCREMENT PRIMARY KEY,
    numero_cuenta VARCHAR(8) NOT NULL,
    tipo_operacion CHAR(1) NOT NULL,
    monto DECIMAL(7, 2) NOT NULL,
    fecha_operacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (numero_cuenta) REFERENCES cuentas(numero_cuenta)
);

-- 4. Tabla de Errores (Lo que escupió tu archivo ERRORES de COBOL)
CREATE TABLE excepciones_batch (
    id_error INT AUTO_INCREMENT PRIMARY KEY,
    numero_cuenta VARCHAR(8) NOT NULL,      -- Extraído del string de 60 espacios
    monto_intentado DECIMAL(7, 2), -- Extraído y limpiado (sin el $)
    motivo_rechazo VARCHAR(38),    
    fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE cuentas 
ADD COLUMN hashed_password VARCHAR(255) NOT NULL AFTER titular;

ALTER TABLE cuentas 
ADD COLUMN email VARCHAR(150) NOT NULL UNIQUE AFTER titular;