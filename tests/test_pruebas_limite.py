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

# Crear carpeta correcta para screenshots de límites
if not os.path.exists("screenshots_limite"):
    os.makedirs("screenshots_limite")

# Ruta base para simplificar
SAVE = lambda name: driver.save_screenshot(f"screenshots_limite/{name}.png")

# ===========================================================
# 1️⃣ LOGIN – PRUEBAS DE LÍMITE
# ===========================================================

driver.get("file:///C:/Users/crist/Downloads/ITLA/III/index.html")

# --- Usuario vacío ---
wait.until(EC.presence_of_element_located((By.ID, "username"))).clear()
driver.find_element(By.ID, "password").clear()

driver.find_element(By.ID, "username").send_keys("")
driver.find_element(By.ID, "password").send_keys("")
driver.find_element(By.TAG_NAME, "button").click()

time.sleep(1)
SAVE("login_vacio")

error_msg = driver.find_element(By.ID, "loginError").text
assert error_msg.strip() != "", "ERROR: No se mostró mensaje en login vacío"


# --- Usuario muy corto ---
driver.find_element(By.ID, "username").clear()
driver.find_element(By.ID, "password").clear()

driver.find_element(By.ID, "username").send_keys("a")
driver.find_element(By.ID, "password").send_keys("1")
driver.find_element(By.TAG_NAME, "button").click()

time.sleep(1)
SAVE("login_usuario_corto")

error_msg = driver.find_element(By.ID, "loginError").text
assert error_msg.strip() != "", "ERROR: No se mostró mensaje con usuario corto"


# --- Contraseña muy larga ---
driver.find_element(By.ID, "username").clear()
driver.find_element(By.ID, "password").clear()

driver.find_element(By.ID, "username").send_keys("admin")
driver.find_element(By.ID, "password").send_keys("1" * 100)
driver.find_element(By.TAG_NAME, "button").click()

time.sleep(1)
SAVE("login_password_larga")

error_msg = driver.find_element(By.ID, "loginError").text
assert error_msg.strip() != "", "ERROR: No se mostró mensaje con password larga"


# ===========================================================
# 2️⃣ CREAR – PRUEBAS DE LÍMITE
# ===========================================================

# Login correcto
driver.find_element(By.ID, "username").clear()
driver.find_element(By.ID, "username").send_keys("admin")
driver.find_element(By.ID, "password").clear()
driver.find_element(By.ID, "password").send_keys("1234")
driver.find_element(By.TAG_NAME, "button").click()

# --- Edad = 0 ---
wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys("Prueba Limite")
driver.find_element(By.ID, "email").send_keys("limite@correo.com")
driver.find_element(By.ID, "age").send_keys("0")
driver.find_element(By.XPATH, "//button[contains(text(),'Guardar')]").click()

time.sleep(1)
alert = driver.switch_to.alert
alert_text = alert.text.lower()
alert.accept()
time.sleep(0.3)
SAVE("crear_edad_cero")

assert "edad" in alert_text or "obligatorios" in alert_text


# --- Nombre muy largo ---
driver.find_element(By.ID, "name").clear()
driver.find_element(By.ID, "email").clear()
driver.find_element(By.ID, "age").clear()

driver.find_element(By.ID, "name").send_keys("A" * 150)
driver.find_element(By.ID, "email").send_keys("test@correo.com")
driver.find_element(By.ID, "age").send_keys("25")

driver.find_element(By.XPATH, "//button[contains(text(),'Guardar')]").click()

time.sleep(1)
alert = driver.switch_to.alert
txt = alert.text.lower()
alert.accept()
time.sleep(0.3)
SAVE("crear_nombre_largo")

assert "obligatorios" in txt or "largo" in txt or "nombre" in txt


# --- Email inválido ---
driver.find_element(By.ID, "name").clear()
driver.find_element(By.ID, "email").clear()
driver.find_element(By.ID, "age").clear()

driver.find_element(By.ID, "name").send_keys("Correo Malo")
driver.find_element(By.ID, "email").send_keys("correo-malo")
driver.find_element(By.ID, "age").send_keys("30")

driver.find_element(By.XPATH, "//button[contains(text(),'Guardar')]").click()

time.sleep(1)
alert = driver.switch_to.alert
txt = alert.text.lower()
alert.accept()
time.sleep(0.3)
SAVE("crear_email_invalido")

assert "correo" in txt or "email" in txt or "formato" in txt


# ===========================================================
# 3️⃣ LEER – PRUEBAS DE LÍMITE
# ===========================================================

driver.find_element(By.ID, "name").clear()
driver.find_element(By.ID, "email").clear()
driver.find_element(By.ID, "age").clear()

driver.find_element(By.ID, "name").send_keys("Registro Lectura")
driver.find_element(By.ID, "email").send_keys("lectura@correo.com")
driver.find_element(By.ID, "age").send_keys("33")

driver.find_element(By.XPATH, "//button[contains(text(),'Guardar')]").click()

time.sleep(1)
SAVE("leer_registro")

tabla_txt = driver.find_element(By.ID, "tableBody").text
assert "Registro Lectura" in tabla_txt


# ===========================================================
# 4️⃣ EDITAR – PRUEBAS DE LÍMITE
# ===========================================================

driver.find_element(By.XPATH, "//button[contains(text(),'Editar')]").click()
time.sleep(1)

# Cambiar solo un carácter
name_input = driver.find_element(By.ID, "name")
old = name_input.get_attribute("value")

name_input.clear()
name_input.send_keys(old[:-1] + "X")

driver.find_element(By.XPATH, "//button[contains(text(),'Guardar')]").click()
time.sleep(1)

SAVE("editar_un_caracter")

tabla_txt = driver.find_element(By.ID, "tableBody").text
assert "X" in tabla_txt


# --- Edad muy alta ---
driver.find_element(By.XPATH, "//button[contains(text(),'Editar')]").click()
time.sleep(1)

age_input = driver.find_element(By.ID, "age")
age_input.clear()
age_input.send_keys("9999")

driver.find_element(By.XPATH, "//button[contains(text(),'Guardar')]").click()

time.sleep(1)
alert = driver.switch_to.alert
txt = alert.text.lower()
alert.accept()
time.sleep(0.3)

SAVE("editar_edad_alta")

assert "edad" in txt or "obligatorios" in txt


# ===========================================================
# 5️⃣ ELIMINAR – PRUEBAS DE LÍMITE
# ===========================================================

driver.find_element(By.XPATH, "//button[contains(text(),'Eliminar')]").click()
time.sleep(1)

SAVE("eliminar_primero")

tabla_txt_final = driver.find_element(By.ID, "tableBody").text
assert tabla_txt_final.strip() == ""


# ===========================================================
# FIN
# ===========================================================

print("\n====================================")
print(" TODAS LAS PRUEBAS DE LÍMITE LISTAS ✔")
print("====================================")

driver.quit()
