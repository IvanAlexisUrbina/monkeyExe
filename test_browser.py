from web_automation import WebBot
import time

def test_browser():
    print("[INFO] Iniciando test del navegador...")
    
    bot = WebBot(browser_type="chrome", headless=False)
    
    if bot.start_browser():
        print("[OK] Navegador iniciado correctamente")
        
        # Navegar a una página simple
        if bot.navigate_to_page("https://www.google.com"):
            print("[OK] Navegacion exitosa")
            time.sleep(5)  # Mantener abierto 5 segundos
        else:
            print("[ERROR] Error en navegacion")
        
        print("[INFO] Cerrando navegador...")
        bot.close_browser()
        print("[OK] Test completado")
    else:
        print("[ERROR] Error iniciando navegador")

if __name__ == "__main__":
    test_browser()