import os
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askdirectory

# Función para convertir .xls a .xlsx
def convertir_xls_a_xlsx(archivo_xls, archivo_xlsx):
    try:
        # Leer el archivo .xls con pandas
        df = pd.read_excel(archivo_xls, engine='xlrd')
        # Guardar como .xlsx
        df.to_excel(archivo_xlsx, index=False, engine='openpyxl')
        print(f"Archivo convertido y guardado como {archivo_xlsx}")
    except Exception as e:
        print(f"Error al convertir {archivo_xls}: {e}")

# Función para seleccionar la carpeta
def seleccionar_carpeta():
    Tk().withdraw()  # Ocultar la ventana principal de Tkinter
    carpeta = askdirectory(title="Selecciona la carpeta con los archivos .xls")  # Cuadro de diálogo para elegir la carpeta
    return carpeta

# Función para convertir el nombre de los archivos a minúsculas
def convertir_a_minusculas(directorio):
    for carpeta, _, archivos in os.walk(directorio):
        for archivo in archivos:
            if archivo.endswith('.xls') or archivo.endswith('.XLS'):
                archivo_original = os.path.join(carpeta, archivo)
                archivo_nuevo = os.path.join(carpeta, archivo.lower())
                os.rename(archivo_original, archivo_nuevo)  # Renombrar archivo a minúsculas
                print(f"Archivo renombrado: {archivo_original} -> {archivo_nuevo}")
                # Llamar a la función para convertirlo a .xlsx
                archivo_xlsx = archivo_nuevo.replace('.xls', '.xlsx')
                convertir_xls_a_xlsx(archivo_nuevo, archivo_xlsx)

# Llamar a la función para seleccionar la carpeta
directorio = seleccionar_carpeta()
if directorio:  # Verificar si se seleccionó una carpeta
    convertir_a_minusculas(directorio)
else:
    print("No se seleccionó ninguna carpeta.")

