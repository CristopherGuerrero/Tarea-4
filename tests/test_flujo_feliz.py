from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

# ==========================
# CONFIGURACIÓN DEL DRIVER
# ==========================

options = Options()
options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

wait = WebDriverWait(driver, 10)

# Crear carpeta screenshots_feliz si no existe
if not os.path.exists("screenshots_feliz"):
    os.makedirs("screenshots_feliz")

# ==========================
# 1. LOGIN (CAMINO FELIZ)
# ==========================

driver.get("file:///C:/Users/crist/Downloads/ITLA/III/index.html")

# INGRESAR USUARIO
wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys("admin")

# INGRESAR CONTRASEÑA
driver.find_element(By.ID, "password").send_keys("1234")

# CLIC EN ENTRAR
driver.find_element(By.TAG_NAME, "button").click()

time.sleep(1)
driver.save_screenshot("screenshots_feliz/login_exitoso.png")

# VALIDAR QUE ESTÁ EN DASHBOARD
assert "dashboard" in driver.current_url.lower(), "ERROR: No se abrió el dashboard"

# ==========================
# 2. CREAR REGISTRO
# ==========================

wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys("Juan Pérez")
driver.find_element(By.ID, "email").send_keys("juan@example.com")
driver.find_element(By.ID, "age").send_keys("25")

driver.find_element(By.XPATH, "//button[contains(text(),'Guardar')]").click()

time.sleep(1)
driver.save_screenshot("screenshots_feliz/creado.png")

# VALIDAR QUE APARECE EN TABLA
table = driver.find_element(By.ID, "tableBody").text
assert "Juan Pérez" in table, "ERROR: Registro no creado en tabla"

# ==========================
# 3. EDITAR REGISTRO
# ==========================

edit_button = wait.until(
    EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Editar')]"))
)
edit_button.click()

time.sleep(1)

# MODIFICAR CAMPOS
nombre_input = driver.find_element(By.ID, "name")
nombre_input.clear()
nombre_input.send_keys("Juan Editado")

email_input = driver.find_element(By.ID, "email")
email_input.clear()
email_input.send_keys("juan_edit@example.com")

age_input = driver.find_element(By.ID, "age")
age_input.clear()
age_input.send_keys("30")

driver.find_element(By.XPATH, "//button[contains(text(),'Guardar')]").click()

time.sleep(1)
driver.save_screenshot("screenshots_feliz/editado.png")

tabla = driver.find_element(By.ID, "tableBody").text
assert "Juan Editado" in tabla, "ERROR: Registro no actualizado"

# ==========================
# 4. ELIMINAR REGISTRO
# ==========================

delete_button = wait.until(
    EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Eliminar')]"))
)
delete_button.click()

time.sleep(1)
driver.save_screenshot("screenshots_feliz/eliminado.png")

tabla_final = driver.find_element(By.ID, "tableBody").text
assert "Juan Editado" not in tabla_final, "ERROR: Registro no eliminado"

# ==========================
# FIN DE LA PRUEBA
# ==========================

print("\n===============================")
print(" CAMINO FELIZ COMPLETADO ✔️")
print("===============================")

driver.quit()
