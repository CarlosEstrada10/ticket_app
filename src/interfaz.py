import os
import sys
import subprocess
from tkinter import Tk, Button, Label, filedialog

def resource_path(relative_path):
    """
    Obtiene la ruta absoluta al recurso.
    Funciona tanto en desarrollo (cuando ejecutas el script con Python) 
    como cuando está empaquetado en un ejecutable con PyInstaller.
    """
    try:
        # Si está congelado, sys._MEIPASS existe y es la carpeta temporal donde PyInstaller extrae los archivos.
        base_path = sys._MEIPASS
    except AttributeError:
        # En modo desarrollo, se usa la carpeta actual.
        base_path = os.getcwd()
    return os.path.join(base_path, relative_path)

def seleccionar_carpeta():
    return filedialog.askdirectory(title="Selecciona la carpeta de trabajo")

def actualizar_archivos():
    carpeta = seleccionar_carpeta()
    if carpeta:
        # Obtiene la ruta correcta para actualizar.py
        actualizar_script = resource_path("src/actualizar.py")
        # Usa sys.executable para que se ejecute con el intérprete de Python adecuado
        subprocess.run([sys.executable, actualizar_script, carpeta])
        label_result.config(text="Actualización completada.")
    else:
        label_result.config(text="No se seleccionó carpeta.")

def extraer_ticket():
    carpeta = seleccionar_carpeta()
    if carpeta:
        # Obtiene la ruta correcta para ticket.py
        ticket_script = resource_path("src/ticket.py")
        subprocess.run([sys.executable, ticket_script, carpeta])
        label_result.config(text="Ticket generado.")
    else:
        label_result.config(text="No se seleccionó carpeta.")

# Configuración de la interfaz
root = Tk()
root.title("Generador de Ticket")

btn_actualizar = Button(root, text="Actualizar carpeta", command=actualizar_archivos, width=30, height=2)
btn_actualizar.pack(pady=10)

btn_ticket = Button(root, text="Extraer ticket", command=extraer_ticket, width=30, height=2)
btn_ticket.pack(pady=10)

label_result = Label(root, text="", fg="blue")
label_result.pack(pady=10)

root.mainloop()
