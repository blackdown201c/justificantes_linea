from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def info_medico(cedula):
        
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=chrome_options)
    # Inicializa el driver
    driver.get("https://www.cedulaprofesional.sep.gob.mx/cedula/presidencia/indexAvanzada.action")
    
    # Abre el menú desplegable "Búsqueda"
    menu_busqueda = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Búsqueda')]"))
    )
    menu_busqueda.click()
    
    # Hace clic en el enlace "Cédula" que activa la función findBasica()
    link_cedula = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Cédula')]"))
    )
    link_cedula.click()
    
    # Inserta '2088793' en el campo de cédula
    campo_cedula = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "idCedula"))
    )
    campo_cedula.send_keys('1880130')
    
    # Presiona el botón "Consultar" usando el ID específico
    boton_consultar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "dijit_form_Button_1"))
    )
    boton_consultar.click()
    
    nombre_element = WebDriverWait(driver, 21).until(
        EC.presence_of_element_located((By.ID, "detalleNombre"))
    )
    
'''
# Aquí capturamos la pantalla
screenshot_path = "screenshot.png"
driver.save_screenshot(screenshot_path)
print(f"Captura de pantalla guardada en: {screenshot_path}")

driver.quit()

os.system(f"open {screenshot_path}")
'''
