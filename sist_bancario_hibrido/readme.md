# 🏦 Core Bancario Batch (IBM Mainframe / COBOL)

Este repositorio contiene el "Motor Core" de un Sistema Bancario Híbrido. Está diseñado para ejecutarse en un entorno IBM Mainframe (z/OS) y procesa transacciones financieras masivas utilizando arquitecturas de procesamiento por lotes (*Batch Processing*).

Este proyecto forma parte de la **Fase 1** de un sistema híbrido que eventualmente se integrará con un backend en FastAPI (Python) y bases de datos relacionales (MySQL) mediante procesos ETL.

## ⚙️ Arquitectura y Características Técnicas

*   **Split-Processing (Enrutamiento Dinámico):** Implementación de lógica de separación de flujos. Las transacciones exitosas se dirigen a un archivo de saldos (`LRECL=20`), mientras que las excepciones se derivan a un archivo de auditoría independiente (`LRECL=60`).
*   **Estándares de Codificación COBOL:**
    *   Uso de variables empaquetadas (`COMP-3`) para optimización matemática.
    *   Máscaras de edición de salida (ej. `$$$,$$9.99`) para reportes financieros.
    *   Uso de constantes figurativas (`ALL`) y manejo estricto de variables de estado (File Status).
*   **Orquestación JCL:** Script multi-paso que maneja la compilación (`IGYWCL`), ejecución condicional (`COND=(0,NE)`) e impresión de utilidades del sistema (`IEBGENER`).

## ⚠️ Nota de Ejecución (Requisitos del Entorno)

Este código es **nativo de Mainframe**. No puede ejecutarse directamente en compiladores de PC estándar (como GnuCOBOL) sin modificaciones, ya que depende fuertemente de la infraestructura de z/OS y del gestor de trabajos JCL.

Para revisores o reclutadores, se han incluido ejemplos de los archivos de entrada y salida generados por el sistema dentro de la carpeta `/data` para demostrar el funcionamiento lógico del programa sin necesidad de un entorno IBM Z.

## 📂 Estructura del Proyecto

*   `/src/BANCOCOR.cbl`: Código fuente principal (Lógica de negocios).
*   `/jcl/RUNBANCO.jcl`: Job Control Language para compilación, ejecución y enrutamiento de Spool.
*   `/data/`: Archivos de prueba (Secuenciales / PS) con datos de muestra y resultados procesados por el Mainframe.

## 👨‍💻 Autor
[Tu Nombre/Usuario] - *Desarrollo de Software y Arquitectura Backend*
