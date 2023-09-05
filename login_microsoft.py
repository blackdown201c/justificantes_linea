from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time
import requests
import sqlite3
import pandas as pd
import imghdr

def iniciar_sesion():
    from contrasenas import o_usuario, o_contrasena
    usuario = o_usuario
    contraseña = o_contrasena
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=4765445b-32c6-49b0-83e6-1d93765276ca&redirect_uri=https%3A%2F%2Fwww.office.com%2Flandingv2&response_type=code%20id_token&scope=openid%20profile%20https%3A%2F%2Fwww.office.com%2Fv2%2FOfficeHome.All&response_mode=form_post&nonce=638252268234377921.M2E0OThiYTctMTUzNC00ZTQ3LTlkZDctMDQwY2JjMmZkOTEwODhmYTdmZDgtZDc4ZS00ZDkyLTg0NGYtYjU1MDhhMDNmMjNh&ui_locales=es-419&mkt=es-419&client-request-id=216440ee-a97c-41b6-b494-3f3cf693bcb3&state=5zKWXGKwX5WnoCN1x0ANiXsrvQz_sFdRoYR3rp12geosJ29l3t5tx101IRtqmeov49QiUhCrhaa87Mgn_tAY8_wtT79hCRKaHeyMW4ZJsQZVMHdtURx8LRhbW6_nYx3sfHrs_3pO1qbUqaNzVfs0xFVxgDR8iFyUGaaNCNHcYf6mgK9dxXCMbN4ajVH2tb1iB4hGpwK3lqdgtdwn16bSM3gMeKWjIRW2zkAeAuc3cUOyNG20VDdXQ3WgEBOXYdLq9ZkdOfk_k9SShcU_Xrj3SSvoPzImbhTHT1g3ilxXVFw&x-client-SKU=ID_NET6_0&x-client-ver=6.30.1.0"
    driver = webdriver.Chrome()
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'i0116'))).send_keys(usuario)
    WebDriverWait(driver, 10,(NoSuchElementException,StaleElementReferenceException,)).until(EC.presence_of_element_located((By.ID, 'idSIButton9'))).click()
    time.sleep(3)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'i0118'))).send_keys(contraseña)
    WebDriverWait(driver, 10, (NoSuchElementException,StaleElementReferenceException,)).until(EC.presence_of_element_located((By.ID, 'idSIButton9'))).click()
    return driver  

def obtener_documentos(indice,fila):
    try:
        cuenta = None
        img_url = fila['Documento']
        driver.get(img_url)
        cookies = driver.get_cookies()
        cookie_dict = {c['name']: c['value'] for c in cookies}
        response = requests.get(img_url, cookies=cookie_dict, stream=True)
        img_data = response.content
        # Verificar si img_data es una imagen
        if imghdr.what(None, img_data) is not None:
            cursor.execute('''SELECT cuenta FROM alumnos.datos_academicos 
                           WHERE correo_institucional = ? ''',(fila['Correo'],))
            resultado = cursor.fetchall()
            
            if resultado:
                cuenta = resultado[0][0]
                
            cursor.execute('''INSERT INTO justificantes_pendientes
                               (correo,cuenta,dias,documento) VALUES (?,?,?,?)''',
                               (fila['Correo'], cuenta, fila['Dias'], img_data))
            conn.commit() 

        else:
            cursor.execute( '''INSERT INTO problema_documento
                               cuenta VALUES ?''',(cuenta,) )
            conn.commit() 

            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

alumnos = pd.read_excel('PRUEBAS3.xlsx',usecols=[0,3,19,28])

nombres=[];nombres2=['ID','Correo','Dias','Documento'];
for i in range(4):nombres.append(alumnos.columns[i]);alumnos.rename(columns={nombres[i]: nombres2[i]}, inplace=True)

driver = iniciar_sesion()

conn = sqlite3.connect('justificantes_en_linea.db')
cursor = conn.cursor()
cursor.execute("BEGIN TRANSACTION")
cursor.execute("ATTACH DATABASE '/Users/miguelhernandez/Library/Mobile Documents/com~apple~CloudDocs/base de datos CCH/carpeta sin título/base_informacion.db' AS alumnos")

for indice, fila in alumnos.iterrows():
    obtener_documentos(indice,fila)
    
conn.commit()
cursor.execute("DETACH DATABASE alumnos")
conn.close()
driver.close()




