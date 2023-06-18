import socket,os
import smtplib
from email.message import EmailMessage

#! Email stuff 
def send_email(message):

    port = 465  # For SSL
    password = "edOMOo,=,33" #! THIS NEEDS TO BE FUCKING ENCRYPTED v3 goal
    
    # Create a secure SSL context
    # context = ssl.create_default_context()

    msg = EmailMessage()
    msg['Subject'] = "Artisan Manager Bot"
    msg['From'] = "artisan_bot@artisanhosting.net"
    msg['To'] = "dwhitfield@ramfield.net"
    msg.set_content(message)

    with smtplib.SMTP_SSL("mail.ramfield.net", port ) as server:
        server.login("artisan_bot@artisanhosting.net", password)
        server.send_message(msg)


installed_version = os.popen("artisan --version-cli").read().rstrip()
hostname = socket.gethostname()
send_email(f"System {hostname} has installed version {installed_version} !")
