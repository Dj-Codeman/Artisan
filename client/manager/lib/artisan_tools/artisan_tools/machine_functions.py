#!/usr/bin/python3
import os,sys
import mysql.connector
from mysql.connector import Error
import fcntl, socket, struct
from email.message import EmailMessage
import smtplib

# ! password magic

def decrypt_creds(name):
    # test if encore is installed and die other wise
    if os.path.isfile("/usr/local/bin/encore") == False:
        sys.exit(1)

    # * getting the name and pw
    if name == "database":
        os.system("encore --read artisan database > /dev/null")
        with open("/tmp/database.pw", 'r') as file:
            password = file.read().rstrip()
        os.system("rm /tmp/database.pw > /dev/null")
        return password
    
    elif name == "email":
        os.system("encore --read artisan email > /dev/null")
        with open("/tmp/email.pw", 'r') as file:
            password = file.read().rstrip()
        os.system("rm /tmp/database.pw > /dev/null")
        return password
    
# ! Emailing tools
def send_email(message):

    port = 465  # For SSL
    password = decrypt_creds("email")
    
    msg = EmailMessage()
    msg['Subject'] = "Artisan Manager Bot"
    msg['From'] = "artisan_bot@artisanhosting.net"
    msg['To'] = "dwhitfield@ramfield.net"
    msg.set_content(message)

    with smtplib.SMTP_SSL("mail.ramfield.net", port ) as server:
        server.login("artisan_bot@artisanhosting.net", password)
        server.send_message(msg)

# ! mysql connecting func
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database="Artisan_Map"
        )
        print(">") # * this function is called in client seen spaces. This indicates the connection suceeded without disclosing too much
    except Error as err:
        print("!")
        send_email(f"Client {host_name} could not connect to the database wuth the following error: '{err}'")

    return connection

#! mysql read and write
def write_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

# ! Networking stuff
def get_mac_addr(): # consider hardcoding mac for specific vm
    i = "ens18"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(i, 'utf-8')[:15]))
    # ! write fucking notes or better code for this shit
    return '-'.join('%02x' % b for b in info[18:24])

def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('10.1.0.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

