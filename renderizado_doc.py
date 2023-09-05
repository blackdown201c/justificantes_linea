nimport sqlite3
import datetime
from docxtpl import DocxTemplate

def busqueda(cuenta):
    try:           
        conn = sqlite3.connect('/Users/miguelhernandez/Library/Mobile Documents/com~apple~CloudDocs/base de datos CCH/carpeta sin título/base_informacion.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT p.cuenta,p.nombre,p.CURP,a.correo_institucional,a.grupo
                           FROM datos_academicos a INNER JOIN datos_personales p
                           ON a.cuenta = p.cuenta
                           WHERE a.cuenta = ?
                       ''',(cuenta,))
        inf = cursor.fetchone()
        columnas = [column[0] for column in cursor.description]
        conn.close()

        if inf is None:
            return None
        else:
            alumno = dict(zip(columnas, inf))
            return alumno

    except sqlite3.Error as e:
        print(f"Ocurrió el siguiente error con SQLite3 : {e}")
        return None 

def fecha():
    today = datetime.date.today()
    mes_nombres = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
                   7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
    fecha = f"Ciudad de México, a {today.day} de {mes_nombres[today.month]} de {today.year}"
    return fecha

def registro(alumno):
    today = datetime.date.today()
    fecha = today.strftime("%d/%m/%Y") 
    conn = sqlite3.connect('/Users/miguelhernandez/Library/Mobile Documents/com~apple~CloudDocs/base de datos CCH/carpeta sin título/base_informacion.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNT(cuenta) FROM justificantes ''')
    numero = str(int(cursor.fetchone()[0]) + 1).zfill(4)
    cursor.execute('''INSERT INTO justificantes(cuenta,dias,motivo,fechat,numero)
                      VALUES (?,?,?,?,?) ''', (alumno['cuenta'],alumno['Dias'],
                      alumno['Motivo'],fecha, numero))
    conn.commit()
    conn.close()
    alumno.update({'ID':numero})
    return alumno

def word(datos):
    doc = DocxTemplate('Template.docx')
    context = {'ID': datos['ID'], 'Cuenta': datos['cuenta'], 
               'Nombre': datos['nombre'],'grupo': datos['grupo'], 
               'Dias': datos['Dias'],'MOTIVO': datos['Motivo'],
               'fecha':fecha()}
    doc.render(context)
    doc.save('justificante.docx')

# Ejemplo de uso
ruta_archivo_pdf = "/Users/miguelhernandez/Desktop/justificante.pdf"

conn = sqlite3.connect('justificantes_en_linea.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM por_enviar LIMIT 1;')
resultado=cursor.fetchone()
conn.close()

def obtener_documento(resultado):
    cuenta, dias = resultado
    alumno = busqueda(cuenta)
    alumno['Dias'] = dias; alumno['Motivo']='Salud'
    alumno = registro(alumno)
    word(alumno)