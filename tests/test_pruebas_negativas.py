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

def test_pruebas_negativas(driver):
    wait = WebDriverWait(driver, 10)

    # Crear carpeta de screenshots
    if not os.path.exists("screenshots_negativas"):
        os.makedirs("screenshots_negativas")

    driver.get("file:///C:/Users/crist/Downloads/ITLA/III/index.html")

    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys("wrong")
    driver.find_element(By.ID, "password").send_keys("incorrect")
    driver.find_element(By.TAG_NAME, "button").click()

    time.sleep(1)
    driver.save_screenshot("screenshots_negativas/login_incorrecto.png")

    error_msg = driver.find_element(By.ID, "loginError").text
    assert "incorrectas" in error_msg.lower(), "ERROR: No se mostró mensaje de credenciales incorrectas"

    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.TAG_NAME, "button").click()

    wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Guardar')]"))).click()

    time.sleep(0.5)

    alert = driver.switch_to.alert
    alert_text = alert.text
    assert "obligatorios" in alert_text.lower(), "ERROR: No aparece mensaje de campos obligatorios"
    alert.accept()
    time.sleep(0.3)

    driver.save_screenshot("screenshots_negativas/crear_vacio.png")

    wait.until(EC.presence_of_element_located((By.ID, "name"))).send_keys("Editar Negativo")
    driver.find_element(By.ID, "email").send_keys("editar@correo.com")
    driver.find_element(By.ID, "age").send_keys("25")
    driver.find_element(By.XPATH, "//button[contains(text(),'Guardar')]").click()

    time.sleep(1)

    driver.find_element(By.XPATH, "//button[contains(text(),'Editar')]").click()
    time.sleep(1)

    driver.find_element(By.ID, "name").clear()
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "age").clear()

    driver.find_element(By.XPATH, "//button[contains(text(),'Guardar')]").click()

    time.sleep(0.5)
    alert = driver.switch_to.alert
    alert_text = alert.text
    assert "obligatorios" in alert_text.lower(), "ERROR: No aparece mensaje de campos obligatorios al editar"

    alert.accept()
    time.sleep(0.3)

    driver.save_screenshot("screenshots_negativas/editar_vacio.png")

    driver.find_element(By.XPATH, "//button[contains(text(),'Eliminar')]").click()
    time.sleep(1)

    try:
        delete_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Eliminar')]")
        delete_btn.click()
    except:
        driver.save_screenshot("screenshots_negativas/eliminar_inexistente.png")
        print("No hay registros — prueba negativa correcta.")

    print(" TODAS LAS PRUEBAS NEGATIVAS LISTAS ")
