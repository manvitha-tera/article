import smtplib, ssl
import datetime as dt
import time
from django.core.mail import send_mail
def send_mail(message):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "sushanth.singh333@gmail.com"
    receiver_email = "manvitha@wesecureapp.com"

    password = "sushanth@123"

    # message = 'Subject: {}\n\n{}'.format("Reset Password Link", 'http://127.0.0.1:8000/registration/password_reset/')
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo()
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        print(message)
        server.sendmail(sender_email, receiver_email, message)
        print("sent")
    except Exception as e:
        print(e)
    finally:
        server.quit()