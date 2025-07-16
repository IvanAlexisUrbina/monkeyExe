from web_automation_clean import WebBot
import time

def debug_form():
    print("[INFO] Iniciando debug del formulario...")
    
    bot = WebBot(browser_type="chrome", headless=False)
    
    if bot.start_browser():
        print("[OK] Navegador iniciado")
        
        if bot.navigate_to_page("https://caballerosdelavirgen.com.co/donacion/"):
            print("[OK] Pagina cargada")
            
            try:
                from selenium.webdriver.support.ui import WebDriverWait, Select
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.webdriver.common.by import By
                
                wait = WebDriverWait(bot.driver, 20)
                
                # Clic en UNA VEZ
                print("[INFO] Haciendo clic en UNA VEZ...")
                wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(text(), 'UNAVEZ', 'unavez'), 'una vez')]"))).click()
                time.sleep(1)
                
                # Clic en $10.000
                print("[INFO] Haciendo clic en $10.000...")
                wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '$ 10.000')]"))).click()
                time.sleep(1)
                
                # Clic en boton azul
                print("[INFO] Haciendo clic en boton azul...")
                boton_azul = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and not(@disabled)]//*[contains(text(), '10.000')]")))
                bot.driver.execute_script("arguments[0].click();", boton_azul)
                time.sleep(2)
                
                # Llenar campos basicos
                print("[INFO] Llenando campos basicos...")
                wait.until(EC.presence_of_element_located((By.NAME, "full_name"))).send_keys("Juan urbina melo")
                bot.driver.find_element(By.NAME, "email").send_keys("ivan@innclod.com")
                bot.driver.find_element(By.NAME, "phone").send_keys("3007264042")
                
                # Debug del select de documento
                print("[DEBUG] Analizando opciones del select de documento...")
                try:
                    document_select = Select(wait.until(EC.presence_of_element_located((By.NAME, "document_type"))))
                    print("[DEBUG] Opciones disponibles:")
                    for i, option in enumerate(document_select.options):
                        print(f"  {i}: '{option.text}' (value='{option.get_attribute('value')}')")
                except Exception as e:
                    print(f"[ERROR] Error con select: {e}")
                
                # Debug de checkboxes
                print("[DEBUG] Buscando checkboxes...")
                checkboxes = bot.driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
                print(f"[DEBUG] Encontrados {len(checkboxes)} checkboxes:")
                for i, cb in enumerate(checkboxes):
                    name = cb.get_attribute('name') or 'sin_nombre'
                    id_attr = cb.get_attribute('id') or 'sin_id'
                    print(f"  {i}: name='{name}', id='{id_attr}'")
                
                print("[INFO] Manteniendo navegador abierto por 30 segundos para inspeccion...")
                time.sleep(30)
                
            except Exception as e:
                print(f"[ERROR] Error en debug: {e}")
                time.sleep(10)
        
        bot.close_browser()
    else:
        print("[ERROR] No se pudo iniciar navegador")

if __name__ == "__main__":
    debug_form()