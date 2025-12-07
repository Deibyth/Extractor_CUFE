import os
import re
import sqlite3
from PyPDF2 import PdfReader
from pathlib import Path

def extract_cufe_from_pdf(pdf_path):
    """
    Extrae el CUFE desde un archivo PDF usando patrones hexadecimales.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""

        # Extrae el texto de todas las páginas
        for page in reader.pages:
            text += page.extract_text()

        # Expresión regular para CUFE con saltos de línea
        pattern = r'\b([0-9a-fA-F]\n*){95,100}\b'
        match = re.search(pattern, text)

        if match:
            return match.group(0).replace('\n', '')

        # Búsqueda alternativa sin saltos de línea
        text_clean = text.replace('\n', '')
        pattern_clean = r'\b[0-9a-fA-F]{95,100}\b'
        match_clean = re.search(pattern_clean, text_clean)

        return match_clean.group(0) if match_clean else None

    except Exception as e:
        print(f"Error al procesar {pdf_path}: {str(e)}")
        return None

def get_pdf_info(pdf_path):
    """
    Obtiene número de páginas y tamaño del archivo PDF.
    """
    try:
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)
        file_size = os.path.getsize(pdf_path)
        return num_pages, file_size
    except Exception as e:
        print(f"Error al obtener información de {pdf_path}: {str(e)}")
        return None, None

def create_database(db_name="facturas.db"):
    """
    Crea la base de datos y la tabla principal.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_archivo TEXT NOT NULL,
            numero_paginas INTEGER,
            cufe TEXT,
            peso_archivo INTEGER,
            fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    return conn

def process_pdf_folder(folder_path, db_conn):
    """
    Procesa todos los PDF de una carpeta y los registra en la base de datos.
    """
    cursor = db_conn.cursor()
    folder = Path(folder_path)

    if not folder.exists():
        print(f"La carpeta {folder_path} no existe.")
        return

    pdf_files = list(folder.glob("*.pdf"))

    if not pdf_files:
        print("No se encontraron archivos PDF.")
        return

    print(f"Procesando {len(pdf_files)} archivos...\n")

    for pdf_file in pdf_files:
        print(f"Procesando: {pdf_file.name}")

        num_pages, file_size = get_pdf_info(pdf_file)
        cufe = extract_cufe_from_pdf(pdf_file)

        cursor.execute('''
            INSERT INTO facturas (nombre_archivo, numero_paginas, cufe, peso_archivo)
            VALUES (?, ?, ?, ?)
        ''', (pdf_file.name, num_pages, cufe, file_size))

        print(f"  - Páginas: {num_pages}")
        print(f"  - Tamaño: {file_size} bytes")
        print(f"  - CUFE: {cufe or 'No encontrado'}\n")

    db_conn.commit()
    print("Procesamiento completado.")

def show_results(db_conn):
    """
    Muestra los registros almacenados en la base de datos.
    """
    cursor = db_conn.cursor()
    cursor.execute('SELECT nombre_archivo, numero_paginas, cufe, peso_archivo FROM facturas')

    results = cursor.fetchall()

    print("\n" + "="*80)
    print("RESULTADOS REGISTRADOS")
    print("="*80 + "\n")

    for row in results:
        print(f"Archivo: {row[0]}")
        print(f"Páginas: {row[1]}")
        print(f"Peso: {row[3]} bytes")
        print(f"CUFE: {row[2] or 'No encontrado'}")
        print("-" * 80)

def main():
    """
    Ejecuta el procesamiento de facturas y registra los resultados.
    """
    carpeta_facturas = "Facturas"

    pdf_files = [
        "E54180324100719R001359975500.PDF",
        "E54180324100737R001359977300.PDF",
        "E54200324101609R001360619800.PDF",
        "E54200324101610R001360620700.PDF",
        "E54240424095827R001365163400.PDF",
        "E54240424095827R001365163600.PDF",
        "E54270424123712R001365720600.PDF",
        "E54300424101133R001366167400.PDF",
        "E54110424120908R001363335100.PDF",
        "E54130324071704R001359470200.PDF"
    ]

    print("="*80)
    print("EXTRACTOR DE CUFE DE FACTURAS")
    print("="*80 + "\n")
    print(f"Carpeta: {carpeta_facturas}")
    print(f"Archivos a procesar: {len(pdf_files)}\n")

    db_conn = create_database()

    for pdf_filename in pdf_files:
        pdf_path = os.path.join(carpeta_facturas, pdf_filename)
        print(f"Procesando: {pdf_filename}")

        if not os.path.exists(pdf_path):
            print(f"Archivo no encontrado: {pdf_path}")
            cursor = db_conn.cursor()
            cursor.execute('''
                INSERT INTO facturas (nombre_archivo, numero_paginas, cufe, peso_archivo)
                VALUES (?, ?, ?, ?)
            ''', (pdf_filename, None, "ARCHIVO NO ENCONTRADO", None))
            continue

        num_pages, file_size = get_pdf_info(pdf_path)
        cufe = extract_cufe_from_pdf(pdf_path)

        cursor = db_conn.cursor()
        cursor.execute('''
            INSERT INTO facturas (nombre_archivo, numero_paginas, cufe, peso_archivo)
            VALUES (?, ?, ?, ?)
        ''', (pdf_filename, num_pages, cufe, file_size))

        print(f"Páginas: {num_pages}")
        print(f"Tamaño: {file_size} bytes")
        print(f"CUFE: {cufe or 'No encontrado'}\n")

    db_conn.commit()

    print("="*80)
    print("Procesamiento finalizado.")
    print("="*80 + "\n")

    show_results(db_conn)
    db_conn.close()

    print("\n✓ Base de datos generada: facturas.db")

if __name__ == "__main__":
    main()
