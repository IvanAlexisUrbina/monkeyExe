@echo off
echo Instalando dependencias...
pip install -r requirements.txt

echo Creando ejecutable independiente...
pyinstaller main.spec

echo Copiando archivos adicionales...
if not exist "dist\chromedriver-win64" mkdir "dist\chromedriver-win64"
copy "chromedriver-win64\*" "dist\chromedriver-win64\"
copy "tarjetas_ejemplo.csv" "dist\"

echo.
echo ========================================
echo EJECUTABLE CREADO EXITOSAMENTE
echo ========================================
echo Ubicacion: dist\BotAutomatizacion.exe
echo.
echo El ejecutable incluye:
echo - ChromeDriver integrado
echo - Todas las dependencias Python
echo - Archivo de ejemplo de tarjetas
echo - Base de datos SQLite
echo.
echo Para usar:
echo 1. Ejecutar BotAutomatizacion.exe
echo 2. Login: admin / 123456
echo 3. Subir archivo Excel/CSV
echo 4. Checkear tarjetas
echo ========================================
pause