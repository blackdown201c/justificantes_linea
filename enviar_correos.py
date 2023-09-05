import win32com.client as win32

# Crear el objeto Outlook
outlook = win32.Dispatch('Outlook.Application')

# Crear un nuevo correo electrónico
mail = outlook.CreateItem(0)

# Agregar la dirección de correo principal
mail.To = 'email@example.com'  # Dirección de correo del destinatario

# Agregar la dirección de correo en copia oculta (BCC)
mail.BCC = 'bcc@example.com'  # Dirección de correo del destinatario en copia oculta

# Definir el asunto y el cuerpo del correo
mail.Subject = 'Asunto del correo'
mail.Body = 'Cuerpo del correo'

# Adjuntar un archivo
attachment  = "C:\\ruta\\al\\archivo.docx"  # Ruta al archivo que deseas adjuntar
mail.Attachments.Add(attachment)

# Enviar el correo
mail.Send()

