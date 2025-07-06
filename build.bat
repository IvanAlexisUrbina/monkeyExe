@echo off
echo Instalando dependencias...
pip install -r requirements.txt

echo Creando ejecutable...
pyinstaller --onefile --windowed --name "BotAutomatizacion" main.py

echo Ejecutable creado en dist/BotAutomatizacion.exe
pause