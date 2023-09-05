from PIL import Image, ImageDraw, ImageFont
import io
import sqlite3
import pandas as pd

def generar_fechas():
    import random
    from datetime import datetime
    # Fecha de inicio y fin
    start_date = datetime(2023, 1, 15)
    end_date = datetime(2023, 5, 19)
    # Total de fechas a generar
    total_fechas = 200
    # Lista para almacenar las fechas
    fechas = []
    while len(fechas) < total_fechas:
        # Generar una fecha aleatoria entre la fecha de inicio y fin
        random_date = start_date + (end_date - start_date) * random.random()
        # Si la fecha cae de lunes a viernes, agregarla a la lista
        if random_date.weekday() < 5:  # 0 es lunes y 6 es domingo
            fechas.append(random_date)
    meses = {"01": "enero","02": "febrero","03": "marzo","04": "abril","05": "mayo","06": "junio","07": "julio","08": "agosto","09": "septiembre","10": "octubre","11": "noviembre","12": "diciembre"}
    fechas2=[]
    # Imprimir las fechas con el nombre del mes correspondiente
    for fecha in fechas:
        numero_mes = fecha.strftime("%m")
        nombre_mes = meses.get(numero_mes)
        fecha_str = fecha.strftime("%d de ") + nombre_mes
        fechas2.append(fecha_str)
        
    return fechas2

fechas=generar_fechas()

alumnos = pd.read_excel('PRUEBAS.xlsx',usecols=[3])
alumnos = alumnos.drop(0)
columnas = alumnos.columns
alumnos = alumnos.rename(columns = {'Correo electrónico':'Correo'})
alumnos['Dias']=fechas
# Cargar la imagen
image = Image.open("justificante.jpg")

# Obtener las dimensiones de la imagen
width, height = image.size
# Crear un objeto ImageDraw
draw = ImageDraw.Draw(image)
# Definir el tipo de fuente y su tamaño
font = ImageFont.truetype("Arial.ttf", 40)


conn = sqlite3.connect('justificantes_en_linea.db')
cursor = conn.cursor()
cursor.execute('''ATTACH '/Users/miguelhernandez/Library/Mobile Documents/com~apple~CloudDocs/base de datos CCH/carpeta sin título/base_informacion.db' AS alumnos''')


# Generar 200 copias con los números del 1 al 200
for numero in range(200):
    # Copiar la imagen original
    imagen_copia = image.copy()
    # Crear un objeto ImageDraw para la copia
    draw_copia = ImageDraw.Draw(imagen_copia)
    # Obtener las dimensiones de la copia
    width_copia, height_copia = imagen_copia.size
    # Calcular la posición para el número en el centro
    numero_texto = str(numero)
    numero_texto_width, numero_texto_height = draw.textsize(numero_texto, font=font)
    numero_posicion = ((width_copia - numero_texto_width) // 2, (height_copia - numero_texto_height) // 2)
    # Dibujar el número en la copia con el color verde
    draw_copia.text(numero_posicion, numero_texto, font=font, fill="#100")
    # Convertir la imagen en bytes
    buffer = io.BytesIO()
    imagen_copia.save(buffer, format="JPEG")
    datos_bytes = buffer.getvalue()
    cuenta = None
    correo = alumnos.loc[numero+1]['Correo']
    cursor.execute('''SELECT cuenta FROM alumnos.datos_academicos WHERE correo_institucional = ? ''',(correo,))
    resultado=cursor.fetchone()
    if resultado:
        cuenta = resultado[0]
    dias = alumnos.loc[numero+1]['Dias']
    cursor.execute(''' INSERT INTO justificantes_pendientes
                       (correo,cuenta,dias,documento) VALUES (?,?,?,?) ''',(correo,cuenta,dias,datos_bytes))
conn.commit()
cursor.execute("DETACH DATABASE alumnos")
conn.close()