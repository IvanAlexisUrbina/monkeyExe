from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

class WebBot:
    def __init__(self, headless=False):
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.driver = None

    def start_browser(self):
        try:
            self.driver = webdriver.Chrome(options=self.options)
            return True
        except Exception as e:
            print(f"Error iniciando navegador: {e}")
            return False

    def close_browser(self):
        if self.driver:
            self.driver.quit()

    def navigate_to_page(self, url):
        try:
            self.driver.get(url)
            return True
        except Exception as e:
            print(f"Error navegando a {url}: {e}")
            return False

    def donar_una_vez(self):
        try:
            print("🔍 PASO 1: Abriendo página de donación...")
            if not self.navigate_to_page("https://caballerosdelavirgen.com.co/donacion/"):
                raise Exception("No se pudo cargar la página")
            wait = WebDriverWait(self.driver, 15)

            print("🔍 PASO 2: Haciendo clic en 'UNA VEZ'...")
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(translate(text(), 'UNAVEZ', 'unavez'), 'una vez')]"))
            ).click()
            time.sleep(0.5)

            print("🔍 PASO 3: Haciendo clic en '$10.000'...")
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), '$ 10.000')]"))
            ).click()
            time.sleep(0.5)

            print("🔍 PASO 4: Confirmar botón azul")
            boton_azul = wait.until(EC.presence_of_element_located((
                By.XPATH, "//button[@type='submit' and not(@disabled)]//*[contains(text(), '10.000')]"
            )))
            self.driver.execute_script("arguments[0].click();", boton_azul)
            time.sleep(1)

            print("🔍 PASO 6: Llenando formulario...")
            wait.until(EC.presence_of_element_located((By.NAME, "full_name"))).send_keys("Juan Pérez")
            self.driver.find_element(By.NAME, "email").send_keys("juan@example.com")
            self.driver.find_element(By.NAME, "phone").send_keys("3001234567")

            select_element = wait.until(EC.presence_of_element_located((By.NAME, "document_type")))
            select = Select(select_element)
            select.select_by_visible_text("Cédula de ciudadanía")

            self.driver.find_element(By.NAME, "document").send_keys("123456789")

            print("🔍 PASO 7: Aceptando términos...")
            checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='checkbox']")))
            self.driver.execute_script("arguments[0].click();", checkbox)
            time.sleep(1)

            print("🔍 PASO 8: Clic final en botón de donación...")
            boton_final = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[.//span[contains(text(), 'Una vez') and contains(text(), '10.000')]]"
            )))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_final)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", boton_final)
            time.sleep(3)

            print("🔍 PASO 9: Esperando carga de campos de tarjeta...")

            # Subir al inicio de la página (por si está oculto más abajo)
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)

            # Esperar que los campos estén presentes (espera extendida a 30s)
            wait = WebDriverWait(self.driver, 30)
            campo_tarjeta = wait.until(EC.presence_of_element_located((By.NAME, "cardPan")))
            campo_exp = wait.until(EC.presence_of_element_located((By.NAME, "cardExpireFull")))
            campo_cvv = wait.until(EC.presence_of_element_located((By.NAME, "cvv2")))

            # Esperar que estén visibles e interactuables
            wait.until(EC.element_to_be_clickable((By.NAME, "cardPan")))

            # Scroll específico para asegurar visibilidad (más confiable que scrollTo(0, 0))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", campo_tarjeta)
            time.sleep(1)

            # Limpiar y llenar campo de tarjeta (type="phone" pero necesita número de tarjeta)
            campo_tarjeta.clear()
            campo_tarjeta.send_keys("5306917110894537")
            
            campo_exp.clear()
            campo_exp.send_keys("12/26")
            
            campo_cvv.clear()
            campo_cvv.send_keys("914")

            print("✅ Campos de tarjeta llenados")
            time.sleep(1)

            print("🔍 PASO 10: Confirmando donación final...")
            boton_donar = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'UNA VEZ') and contains(text(), '$ 10.000')]")
            ))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_donar)
            self.driver.execute_script("arguments[0].click();", boton_donar)
            time.sleep(3)

            print("✅ Proceso completado exitosamente")
            return True

        except Exception as e:
            print(f"❌ ERROR ESPECÍFICO: {e}")
            print(f"❌ URL ACTUAL: {self.driver.current_url if self.driver else 'N/A'}")
            return False



# 👉 Uso del bot
if __name__ == "__main__":
    bot = WebBot(headless=False)  # Cambia a True si quieres navegador oculto
    if bot.start_browser():
        success = bot.donar_una_vez()
        print("✅ Donación simulada con éxito" if success else "❌ Falló la donación")
        bot.close_browser()
