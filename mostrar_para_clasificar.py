import io
import sqlite3
from PIL import Image, ImageTk
from tkinter import Tk, Label, Canvas, Button, Entry, StringVar
from tkinter import font as tkFont
from renderizado_doc import *

def obtener_alumnos():
    conn = sqlite3.connect('justificantes_en_linea.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM por_enviar')
    alumnos = cursor.fetchall()
    conn.close()
    for alumno in alumnos:
        obtener_documento(alumno)

def conectar():
    conn = sqlite3.connect('justificantes_en_linea.db')
    cursor = conn.cursor()
    cursor.execute("ATTACH '/Users/miguelhernandez/Library/Mobile Documents/com~apple~CloudDocs/base de datos CCH/carpeta sin título/base_informacion.db' AS alumnos")
    cursor.execute('''SELECT nombre,a.cuenta,documento,dias
                   FROM justificantes_pendientes p INNER JOIN alumnos.datos_personales a
                   ON a.cuenta=p.cuenta''')
    data = cursor.fetchall()
    cursor.execute('DETACH DATABASE alumnos')
    conn.close()
    return data

def mostrar_alumno(i, alumnos, label1, label3, canvas):
    global entry_text  # acceder a la variable global
    nombre, cuenta, documento, fecha = alumnos[i]
    n = nombre.split()
    modificar_nombre = lambda n: ' '.join(n[:2]) + '\n' + ' '.join(n[2:]) if len(n) >= 4 else ' '.join(n[:1]) + '\n' + ' '.join(n[1:])
    nombre = modificar_nombre(n)
    label1["text"] = nombre
    entry_text.set(str(fecha))  # establecer el valor de fecha
    documento = Image.open(io.BytesIO(documento))
    documento = documento.resize((600,600), Image.LANCZOS)
    img = ImageTk.PhotoImage(documento)
    canvas.create_image(0,0, anchor = "nw", image=img)
    canvas.image = img  # keep a reference to the image
    
    return cuenta,fecha
    
def clas_enviar(i, cuenta, dias, clas):
    conn = sqlite3.connect('justificantes_en_linea.db')
    cursor = conn.cursor()
    if clas == 0:
        cursor.execute("INSERT INTO por_enviar VALUES (?,?)",(cuenta,dias))
        conn.commit()
        cursor.execute("DELETE FROM justificantes_pendientes WHERE cuenta = ? ", (cuenta,))
        conn.commit()
    elif clas == 1:
        cursor.execute("INSERT INTO problema_documento VALUES (?)",(cuenta,))
        conn.commit()
        cursor.execute("DELETE FROM justificantes_pendientes WHERE cuenta = ? ", (cuenta,))
        conn.commit()
    conn.close()
    i[0] = (i[0] + 1) % len(alumnos)  # incrementa el índice aquí
    
def enviar_justificante(i, alumnos, label1, label3, canvas):
    cuenta, fecha = mostrar_alumno(i[0], alumnos, label1, label3, canvas)
    clas_enviar(i,cuenta,fecha,0)

def informar_problema(i, alumnos, label1, label3, canvas):
    cuenta, fecha = mostrar_alumno(i[0], alumnos, label1, label3, canvas)
    clas_enviar(i,cuenta,fecha,1)  # sólo pasa los argumentos necesarios

alumnos = conectar()

i = [0]

window = Tk()
label1_font = tkFont.Font(weight="bold",size = 15)  # crea un objeto de fuente en negrita
label1 = Label(window, text="", width=50, height=2, font=label1_font)
label1.grid(row=1, column=0)

entry_text = StringVar()

label3 = Entry(window, textvariable=entry_text, width=30)
label3.grid(row=2, column=0)

canvas = Canvas(window, width = 600, height = 600)
canvas.grid(row=4, column=0)

next_button = Button(window, text="Enviar \n Justificante", command=lambda: enviar_justificante(i, alumnos, label1, label3, canvas))
next_button.grid(row=2, column=1)

prev_button = Button(window, text="Informar \n de un problema", command=lambda: informar_problema(i, alumnos, label1, label3, canvas))
prev_button.grid(row=3, column=1)

mostrar_alumno(i[0], alumnos, label1, label3, canvas)
window.mainloop()

