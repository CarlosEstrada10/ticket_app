import os
import subprocess
from tkinter import Tk, Button, Label, filedialog

def seleccionar_carpeta():
    return filedialog.askdirectory(title="Selecciona la carpeta de trabajo")

def actualizar_archivos():
    carpeta = seleccionar_carpeta()
    if carpeta:
        # Llama al script actualizar_xls_a_xlsx.py pasando la carpeta
        subprocess.run(["python", "src/actualizar.py", carpeta])
        label_result.config(text="Actualización completada.")
    else:
        label_result.config(text="No se seleccionó carpeta.")

def extraer_ticket():
    carpeta = seleccionar_carpeta()
    if carpeta:
        # Llama al script extraer_ticket.py pasando la carpeta
        subprocess.run(["python", "src/ticket.py", carpeta])
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
