import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    yield driver
    driver.quit()


def test_pruebas_limite(driver):

    wait = WebDriverWait(driver, 10)

    if not os.path.exists("screenshots_limite"):
        os.makedirs("screenshots_limite")

    SAVE = lambda name: driver.save_screenshot(f"screenshots_limite/{name}.png")

    driver.get("file:///C:/Users/crist/Downloads/ITLA/III/index.html")

    wait.until(EC.presence_of_element_located((By.ID, "username"))).clear()
    driver.find_element(By.ID, "password").clear()

    driver.find_element(By.ID, "username").send_keys("")
    driver.find_element(By.ID, "password").send_keys("")
    driver.find_element(By.TAG_NAME, "button").click()

    time.sleep(1)
    SAVE("login_vacio")

    error_msg = driver.find_element(By.ID, "loginError").text
    assert error_msg.strip() != "", "ERROR: Login vacío sin mensaje"

    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "password").clear()

    driver.find_element(By.ID, "username").send_keys("a")
    driver.find_element(By.ID, "password").send_keys("1")
    driver.find_element(By.TAG_NAME, "button").click()

    time.sleep(1)
    SAVE("login_usuario_corto")

    error_msg = driver.find_element(By.ID, "loginError").text
    assert error_msg.strip() != "", "ERROR: Usuario corto sin mensaje"

    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "password").clear()

    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("1" * 100)
    driver.find_element(By.TAG_NAME, "button").click()

    time.sleep(1)
    SAVE("login_password_larga")

    error_msg = driver.find_element(By.ID, "loginError").text
    assert error_msg.strip() != "", "ERROR: Pass larga sin mensaje"

    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.TAG_NAME, "button").click()

    wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys("Prueba Limite")
    driver.find_element(By.ID, "email").send_keys("limite@correo.com")
    driver.find_element(By.ID, "age").send_keys("0")
    driver.find_element(By.XPATH, "//button[contains(text(),'Guardar')]").click()

    time.sleep(1)
    alert = driver.switch_to.alert
    txt = alert.text.lower()
    alert.accept()

    time.sleep(0.3)
    SAVE("crear_edad_cero")

    assert "edad" in txt or "obligatorios" in txt

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

    assert "correo" in txt or "email" in txt

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

    driver.find_element(By.XPATH, "//button[contains(text(),'Editar')]").click()
    time.sleep(1)

    name_input = driver.find_element(By.ID, "name")
    old = name_input.get_attribute("value")

    name_input.clear()
    name_input.send_keys(old[:-1] + "X")

    driver.find_element(By.XPATH, "//button[contains(text(),'Guardar')]").click()
    time.sleep(1)

    SAVE("editar_un_caracter")

    tabla_txt = driver.find_element(By.ID, "tableBody").text
    assert "X" in tabla_txt

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

    driver.find_element(By.XPATH, "//button[contains(text(),'Eliminar')]").click()
    time.sleep(1)

    SAVE("eliminar_primero")

    tabla_txt_final = driver.find_element(By.ID, "tableBody").text
    assert tabla_txt_final.strip() == ""

    print(" TODAS LAS PRUEBAS DE LÍMITE LISTAS ")
