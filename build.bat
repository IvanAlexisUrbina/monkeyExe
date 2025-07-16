@echo off
echo Instalando dependencias...
pip install -r requirements.txt

echo Creando ejecutable...
pyinstaller --onefile --windowed --name "BotAutomatizacion" --add-data "chromedriver-win64;chromedriver-win64" --add-data "tarjetas_ejemplo.csv;." --hidden-import=tkinter --hidden-import=pandas --hidden-import=selenium --hidden-import=bcrypt --hidden-import=sqlite3 main.py

echo Ejecutable creado en dist/BotAutomatizacion.exe
pause