@echo off
rem ==============================================================
rem Lanzador automático del dashboard de clustering (Windows)
rem ==============================================================

rem 1. Crear entorno virtual si no existe
if not exist ".venv" (
    echo [INFO] Creando entorno virtual...
    python -m venv .venv
)

rem 2. Activar entorno virtual
call .venv\Scripts\activate.bat

rem 3. Instalar / actualizar dependencias
python -m pip install --upgrade --quiet pip
pip install --quiet -r requirements.txt

rem 4. Iniciar Streamlit
streamlit run App.py

rem 5. Al cerrarse Streamlit, desactivar entorno
call deactivate 