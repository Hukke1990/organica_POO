import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def enviar_email_compra(correo_comprador, datos_compra):
    # Configuración del correo
    mi_correo = 'gastonbordet@gmail.com'
    mi_contraseña = 'theclassic1990'

    # Crear mensaje
    msg = MIMEMultipart()
    msg['From'] = mi_correo
    msg['To'] = correo_comprador
    msg['Subject'] = 'Detalles de tu compra'

    # Agregar los datos de la compra al mensaje
    cuerpo_mensaje = 'Hola,\n\nAquí están los detalles de tu compra:\n' + datos_compra
    msg.attach(MIMEText(cuerpo_mensaje, 'plain'))

    # Iniciar servidor y enviar correo
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(mi_correo, mi_contraseña)
    text = msg.as_string()
    server.sendmail(mi_correo, correo_comprador, text)
    server.quit()


# Ejemplo de uso
enviar_email_compra('correo_del_comprador@ejemplo.com', 'datos_de_compra')
