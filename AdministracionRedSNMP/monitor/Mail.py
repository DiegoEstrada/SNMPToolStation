from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail
import logging

##Cuidado con loggin, se debeeria hacer referencia a el a traves de Views, quien es quien casi
## siempre lo invoca views pero lo crea Invoker, aunque si se agrega views como modulo 
## puede haber el problema de dependencias circulares que pasaba antes de crear este archivo

def sendEmail(email,subject,message,imageName):

    #subject = 'Evidencia 3 '
    #message = 'Equipo 10 Grupo 4CM3' 
    email_from = settings.EMAIL_HOST_USER
    recipient_list = []
    recipient_list.append(str(email))

    
    emailObj = EmailMessage(
            subject=subject,
            body=message,
            from_email=email_from,
            to=recipient_list,
            #['bcc@example.com'], What is a Bcc django said A list or tuple of addresses used in the “Bcc” header when sending the email.
            reply_to=['lupe.gg1996@gmail.com'],
            #headers={'Message-ID': 'foo'},
        )

    img = str(settings.STATICFILES_DIRS[0])+"/"+imageName
    img_data = open(img, "rb").read()


    emailObj.attach(imageName, img_data, 'image/png')

    res = emailObj.send()
    
    #res = send_mail(subject,message,email_from,recipient_list,)

    if res:
        print("Correo Electronico enviado a "+email)
        logging.info("Correo Electronico enviado a "+email)
    else: 
        print("Ocurrió un error al enviar el correo elcronico a "+email)
        logging.info("Ocurrió un error al enviar el correo elcronico a "+email)
    
    return  