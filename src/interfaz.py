import os
import sys
import subprocess
from tkinter import Tk, Button, Label, filedialog

def get_script_path(filename):
    """
    Devuelve la ruta absoluta al script 'filename'.
    - En modo empaquetado (cuando existe sys._MEIPASS), se asume que
      los archivos se han incluido en una carpeta "src" dentro del ejecutable.
    - En desarrollo, se asume que los scripts están en el mismo directorio que este archivo.
    """
    try:
        base_path = sys._MEIPASS
        # En el ejecutable, los archivos se encuentran en 'src'
        return os.path.join(base_path, "src", filename)
    except AttributeError:
        # En desarrollo, 'interfaz.py', 'ticket.py' y 'actualizar.py' están en el mismo directorio
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

def seleccionar_carpeta():
    return filedialog.askdirectory(title="Selecciona la carpeta de trabajo")

def actualizar_archivos():
    carpeta = seleccionar_carpeta()
    if carpeta:
        script_path = get_script_path("actualizar.py")
        subprocess.run([sys.executable, script_path, carpeta])
        label_result.config(text="Actualización completada.")
    else:
        label_result.config(text="No se seleccionó carpeta.")

def extraer_ticket():
    carpeta = seleccionar_carpeta()
    if carpeta:
        script_path = get_script_path("ticket.py")
        subprocess.run([sys.executable, script_path, carpeta])
        label_result.config(text="Ticket generado.")
    else:
        label_result.config(text="No se seleccionó carpeta.")

# Configuración de la interfaz gráfica
root = Tk()
root.title("Generador de Ticket")

btn_actualizar = Button(root, text="Actualizar carpeta", command=actualizar_archivos, width=30, height=2)
btn_actualizar.pack(pady=10)

btn_ticket = Button(root, text="Extraer ticket", command=extraer_ticket, width=30, height=2)
btn_ticket.pack(pady=10)

label_result = Label(root, text="", fg="blue")
label_result.pack(pady=10)

root.mainloop()
