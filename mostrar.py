import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
import io

def ventana():
    # Crear ventana
    root = tk.Tk()

    # Crear frame para las etiquetas
    frame_labels = tk.Frame(root)
    frame_labels.pack(side="left")

    # Crear las etiquetas
    label1 = tk.Label(frame_labels, text="Nombre del Alumno", font=("Arial", 15))  # aquí puedes cambiar el tipo de letra y tamaño
    label1.pack()
    label2 = tk.Label(frame_labels, text="Número de cuenta", font=("Arial", 15))  # aquí puedes cambiar el tipo de letra y tamaño
    label2.pack()
    label3 = tk.Entry(frame_labels, font=("Arial", 15))  # aquí puedes cambiar el tipo de letra y tamaño
    label3.pack()

    frame_buttons = tk.Frame(root)
    frame_buttons.pack(side="right")
    button1 = tk.Button(frame_buttons, text="Enviar Justificante", font=("Arial", 15), command=enviar_justificante)  # aquí puedes cambiar el tipo de letra y tamaño
    button1.pack()
    button2 = tk.Button(frame_buttons, text="Informar de un problema", font=("Arial", 15), command=informar_de_un_problema)  # aquí puedes cambiar el tipo de letra y tamaño
    button2.pack()

    # Crear frame para la imagen
    frame_img = tk.Frame(root)
    frame_img.pack(side="right")

    # Crear canvas en el frame para la imagen
    canvas = tk.Canvas(frame_img, width=600, height=600) # puedes ajustar el tamaño como quieras
    canvas.pack()

    return root, label1, label2, label3, canvas

def mostrar_alumno(i, alumnos, label1, label3, canvas):
    nombre, cuenta, documento, fecha = alumnos[i]

    label1["text"] = nombre
    label3.delete(0, tk.END)
    label3.insert(0, str(fecha))

    documento = Image.open(io.BytesIO(documento))
    documento = documento.resize((600,600), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(documento)
    canvas.create_image(0,0, anchor = "nw", image=img)
    canvas.img = img  # Mantén la referencia de la imagen
    
def enviar_justificante():
    print('Enviara el justificante')
    
def informar_de_un_problema():
    print('informar de un problema')

def conectar():
    conn = sqlite3.connect('justificantes_en_linea.db')
    cursor = conn.cursor()
    cursor.execute('''ATTACH '/Users/miguelhernandez/Library/Mobile Documents/com~apple~CloudDocs/base de datos CCH/carpeta sin título/base_informacion.db' AS alumnos''')
    cursor.execute('''SELECT nombre, j.cuenta, documento, dias
                      FROM main.justificantes_pendientes AS j INNER JOIN alumnos.datos_personales AS a 
                      ON j.cuenta = a.cuenta''')              
    alumnos = cursor.fetchall()
    cursor.execute("DETACH DATABASE alumnos")
    conn.close()
    return alumnos

root, label1, label2, label3, canvas = ventana()

i = 0
alumnos = conectar()
mostrar_alumno(i,alumnos, label1, label3, canvas)

root.mainloop()

