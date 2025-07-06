# Bot de Automatización

## Instalación

1. Instalar Python 3.8+
2. Descargar ChromeDriver y agregarlo al PATH
3. Ejecutar: `pip install -r requirements.txt`

## Uso

### Ejecutar en desarrollo:
```bash
python main.py
```

### Crear ejecutable:
```bash
build.bat
```

## Funcionalidades

- **Autenticación**: Login con usuario/contraseña
- **Sistema de créditos**: Cada acción descuenta créditos
- **Base de datos SQLite**: Almacena usuarios y créditos
- **Automatización web**: Selenium para interactuar con páginas
- **Interfaz gráfica**: Tkinter para facilidad de uso

## Usuario de prueba
- Usuario: `admin`
- Contraseña: `123456`
- Créditos iniciales: 10

## Personalización

Modifica `web_automation.py` para cambiar las acciones del bot:
- Cambiar URL objetivo
- Modificar selectores CSS
- Agregar nuevas funciones de automatización