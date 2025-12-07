# Extractor de CUFE 

Sistema desarrollado en Python para extraer CUFE desde archivos PDF y almacenar los resultados en una base de datos SQLite.

## Características

- Extracción automática del CUFE usando expresiones regulares.
- Análisis de cada archivo PDF:
  - Número de páginas
  - Tamaño del archivo
  - CUFE encontrado o no
- Procesamiento masivo de archivos desde una carpeta.
- Base de datos SQLite generada automáticamente.
- Manejo de errores para archivos corruptos o no encontrados.
- Visualización en consola de todos los resultados procesados.

---

## Requisitos Previos

- Python 3.8 o superior  
- pip  
- Librerías necesarias:  
  - PyPDF2
    
---

## Instalación

### Clonar el repositorio

    git clone https://github.com/Deibyth/Extractor_CUFE.git
    cd Extractor_CUFE

### Crear y activar entorno virtual

**Windows:**

    python -m venv venv
    venv\Scripts\activate

**Linux/Mac:**

    python3 -m venv venv
    source venv/bin/activate

### Instalar dependencias

Si tienes requirements.txt:

    pip install -r requirements.txt

Instalación manual:

    pip install PyPDF2

---

## Uso

### Preparar carpeta de facturas

Crear una carpeta llamada "Facturas" dentro del proyecto y colocar allí los archivos PDF.

### Ejecutar el script principal

    python extractor_cufe.py

El sistema procesará los archivos PDF y creará la base de datos "facturas.db".

---

## Ejemplo de salida en consola

    ========================================================================
    EXTRACTOR DE CUFE DE FACTURAS
    ========================================================================

    Carpeta: Facturas
    Archivos a procesar: 5

    Procesando: E54180324100719R001359975500.PDF
    Páginas: 5
    Tamaño: 1024 bytes
    CUFE: 1234567890abcdef...

    Procesando: E54180324100737R001359977300.PDF
    Páginas: 3
    Tamaño: 2048 bytes
    CUFE: No encontrado

    ========================================================================
    Procesamiento finalizado.
    ========================================================================

    Base de datos generada: facturas.db

---

## Consultar la Base de Datos en "facturas.db" 

---


## Autor

**Deibith**  
GitHub: @Deibyth
