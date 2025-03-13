import os
import sys
import subprocess
from tkinter import Tk, Button, Label, filedialog

def resource_path(relative_path):
    """ Obtiene la ruta absoluta del recurso, considerando si está empaquetado o no. """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def seleccionar_carpeta():
    return filedialog.askdirectory(title="Selecciona la carpeta de trabajo")

def actualizar_archivos():
    carpeta = seleccionar_carpeta()
    if carpeta:
        script_path = resource_path(os.path.join('src', 'actualizar.py'))
        subprocess.run([sys.executable, script_path, carpeta])
        label_result.config(text="Actualización completada.")
    else:
        label_result.config(text="No se seleccionó carpeta.")

def extraer_ticket():
    carpeta = seleccionar_carpeta()
    if carpeta:
        script_path = resource_path(os.path.join('src', 'ticket.py'))
        subprocess.run([sys.executable, script_path, carpeta])
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
