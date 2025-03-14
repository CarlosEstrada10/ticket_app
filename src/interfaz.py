import os
import sys
import subprocess
from tkinter import Tk, Button, Label, filedialog

def resource_path(relative_path):
    """
    Obtiene la ruta absoluta del recurso, ya sea en modo desarrollo o empaquetado.
    En modo desarrollo se utiliza el directorio donde está este archivo.
    En modo "congelado" se usa sys._MEIPASS.
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def seleccionar_carpeta():
    return filedialog.askdirectory(title="Selecciona la carpeta de trabajo")

def actualizar_archivos():
    carpeta = seleccionar_carpeta()
    if carpeta:
        # En desarrollo y producción, 'actualizar.py' se encontrará en el mismo directorio.
        script_path = resource_path("actualizar.py")
        subprocess.run([sys.executable, script_path, carpeta])
        label_result.config(text="Actualización completada.")
    else:
        label_result.config(text="No se seleccionó carpeta.")

def extraer_ticket():
    carpeta = seleccionar_carpeta()
    if carpeta:
        script_path = resource_path("ticket.py")
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
