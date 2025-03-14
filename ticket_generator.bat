@echo off
REM Cambia al directorio donde está este archivo .bat
cd d %~dp0
REM Ejecuta el script interfaz.py (asegúrate de que Python esté en el PATH)
python src\interfaz.py
pause