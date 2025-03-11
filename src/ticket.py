import os
import pandas as pd
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import askdirectory

def seleccionar_carpeta():
    Tk().withdraw()
    return askdirectory(title="Selecciona la carpeta con los archivos .xlsx")

# Encabezados deseados para cada archivo (los valores que quieres ver en el ticket)
encabezados_por_archivo = {
    "movtoscaja.xlsx": ["concepto", "fecha", "importe", "cancelado"],
    "cheques.xlsx": ["FOLIO", "FECHA", "IMPORTE", "EFECTIVO", "TARJETA"],
    "descuentosycortesiasaproductos.xlsx": ["cantidad", "descripcion", "precio"],
    "productoscancelados.xlsx": ["mesero", "cantidad", "descripcion", "razon", "fecha"],
    "productosvendidosperiodo.xlsx": ["DESCRIPCION", "PRECIO", "CANTIDAD", "VENTA_TOTAL"],
    "ventasmeseros.xlsx": ["nombre", "importe", "efectivo", "tarjeta", "propina"]
}

# Diccionario para títulos personalizados de cada sección
titulos_por_archivo = {
    "movtoscaja.xlsx": "Movimientos de Caja",
    "cheques.xlsx": "Cheques",
    "descuentosycortesiasaproductos.xlsx": "Descuentos y Cortesías",
    "productoscancelados.xlsx": "Productos Cancelados",
    "productosvendidosperiodo.xlsx": "Productos Vendidos en el Período",
    "ventasmeseros.xlsx": "Ventas por Mesero"
}

# Función para transformar una fecha a solo HH:MM:SS
def transformar_fecha(valor):
    try:
        dt = datetime.strptime(valor.strip(), "%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        try:
            dt = datetime.strptime(valor.strip(), "%Y-%m-%d %H:%M:%S")
        except Exception:
            return valor
    return dt.strftime("%H:%M:%S")

# Función para leer el archivo con el header correcto
def leer_archivo(ruta_archivo, archivo):
    if archivo in ["cheques.xlsx", "productosvendidosperiodo.xlsx"]:
        return pd.read_excel(ruta_archivo, header=4, dtype=str)
    else:
        return pd.read_excel(ruta_archivo, header=0, dtype=str)

# Función para procesar un archivo y generar su bloque formateado
def procesar_archivo(carpeta, archivo, encabezados_deseados):
    ruta_archivo = os.path.join(carpeta, archivo)
    if not os.path.exists(ruta_archivo):
        print(f"⚠ {archivo} no encontrado.")
        return None
    try:
        df = leer_archivo(ruta_archivo, archivo)
        # Preparar nombres de columnas para comparación (minúsculas y sin espacios extras)
        df_cols = [col.strip().lower() for col in df.columns]
        deseados = [col.strip().lower() for col in encabezados_deseados]
        if not all(col in df_cols for col in deseados):
            print(f"❌ {archivo}: faltan columnas requeridas.")
            return None
        # Mapear cada encabezado deseado al nombre real en el DataFrame
        mapping = {}
        for col in deseados:
            for orig in df.columns:
                if orig.strip().lower() == col:
                    mapping[col] = orig
                    break
        df_seleccionado = df[[mapping[col] for col in deseados]].copy()
        
        # Transformar valores de columnas que contengan "fecha"
        for i, col in enumerate(deseados):
            if "fecha" in col:
                df_seleccionado.iloc[:, i] = df_seleccionado.iloc[:, i].apply(lambda x: transformar_fecha(x) if pd.notnull(x) else x)
        
        # Para movtoscaja.xlsx: filtrar registros cancelados y agregar fila de totales en "importe"
        if archivo == "movtoscaja.xlsx":
            idx_cancelado = deseados.index("cancelado")
            df_seleccionado = df_seleccionado[~df_seleccionado.iloc[:, idx_cancelado].str.strip().str.lower().eq("true")].reset_index(drop=True)
            idx_importe = deseados.index("importe")
            try:
                total = pd.to_numeric(df_seleccionado.iloc[:, idx_importe], errors="coerce").sum()
            except Exception:
                total = ""
            totales = [""] * len(deseados)
            totales[0] = "TOTAL"
            totales[idx_importe] = total
            df_total = pd.DataFrame([totales], columns=encabezados_deseados)
            df_seleccionado = pd.concat([df_seleccionado, df_total], ignore_index=True)
        
        # No reindexamos las columnas; mantenemos los encabezados deseados.
        df_seleccionado.columns = encabezados_deseados  # Esto conserva los títulos que definiste
        
        # Crear bloque: fila de título, fila de encabezado y los datos, seguidos de una fila separadora.
        bloque_titulo = pd.DataFrame([[titulos_por_archivo.get(archivo, archivo)] + [""] * (len(encabezados_deseados) - 1)], columns=encabezados_deseados)
        bloque_encabezado = pd.DataFrame([encabezados_deseados], columns=encabezados_deseados)
        bloque_separador = pd.DataFrame([[""] * len(encabezados_deseados)], columns=encabezados_deseados)
        bloque_final = pd.concat([bloque_titulo, bloque_encabezado, df_seleccionado, bloque_separador], ignore_index=True)
        return bloque_final
    except Exception as e:
        print(f"❌ Error al procesar {archivo}: {e}")
        return None

# Función para generar el ticket final
def generar_ticket(carpeta):
    bloques = []
    for archivo, encabezados in encabezados_por_archivo.items():
        bloque = procesar_archivo(carpeta, archivo, encabezados)
        if bloque is not None:
            bloques.append(bloque)
    if bloques:
        # Escribir cada bloque uno debajo del otro en la misma hoja, comenzando en la columna A
        output_path = os.path.join(carpeta, "TICKET.xlsx")
        writer = pd.ExcelWriter(output_path, engine="xlsxwriter")
        sheet_name = "Ticket"
        current_row = 0
        for bloque in bloques:
            bloque.to_excel(writer, sheet_name=sheet_name, startrow=current_row, startcol=0, index=False, header=False)
            current_row += bloque.shape[0]
        writer.close()
        print(f"✅ Ticket generado correctamente en: {output_path}")
    else:
        print("⚠ No se pudieron procesar los archivos para generar el ticket.")

if __name__ == "__main__":
    carpeta = seleccionar_carpeta()
    if carpeta:
        generar_ticket(carpeta)
    else:
        print("⚠ No se seleccionó ninguna carpeta.")
