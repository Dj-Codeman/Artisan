import os
import fcntl, socket, struct
import mysql.connector
import requests
import json


from mysql.connector import Error
import smtplib, ssl

version = "1.0a"

#! Email stuff 
def send_email(message):

    port = 465  # For SSL
    password = "edOMOo,=,33" #! THIS NEEDS TO BE FUCKING ENCRYPTED
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("mail.ramfield.net", port, context=context) as server:
        server.login("artisan_bot@artisanhosting.net", password)

        sender_email = "artisan_bot@artisanhosting.net"
        receiver_email = "dwhitfield@ramfield.net"
    
        server.sendmail(sender_email, receiver_email, message)

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
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

#! mysql read 
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

#! mysql write 
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

#! finding an empty ip
def get_free_ip():
    for x in range(100, 201):
        ip = f"10.1.0.{x}"
        response = os.popen(f"ping -c 1 {ip} ").read()

        if ("Destination Host Unreachable") in response:
            # check if the ip is in the reserved file     
            with open("/etc/artisan.ip", "r") as reserved_ip_file:
                reserved_ip = reserved_ip_file.read().rstrip()
                if ip not in reserved_ip:
                    # os shell appened to the file
                    os.system(f"echo \"{ip}\" >> /etc/artisan.ip")
                    return ip

        
    send_email("IP POOL HAS BEEN EXAUSTED CONGRATULATIONS ON 100 CLIENTS")


def update_machine():
    # Selecting all machines 
    query = "SELECT * FROM machine_id"
    connection = create_server_connection("database.local", "artisan", "Artisan610!")

    machine_data = read_query(connection, query)

    for machine in machine_data:

        machine_id = machine[0]
        machine_type = machine[1]
        machine_mac = machine[2]
        machine_ip = machine[3]
        machine_clients = machine[4]

        print(f"""
            Machine id : {machine_id}
            Machine type : {machine_type}
            Machine mac : {machine_mac}
            Machine ip : {machine_ip}
            Machine clients : {machine_clients} \n\n """)

        if machine_ip == None:
            print(f"Assigning ip to {machine_id}")

            new_ip = get_free_ip()

            print(f"Machine {machine_id} to be assigned {new_ip}")

            query = f"UPDATE machine_id SET machine_ip = '{new_ip}' WHERE uuid = '{machine_id}'"
            execute_query(connection, query)

            update_record(machine_id, new_ip, machine_mac)
 
#!!!!!!! API LAND 

host="netting.local"
username="artisan"
password="Artisan610!"

def dhcp_login():
    login_req = requests.get(f"http://{host}:5380/api/user/login?user={username}&pass={password}&includeInfo=true")
    login_data = json.loads(login_req.text)

    dhcp_token = login_data["token"]
    return dhcp_token

def dhcp_logout(token):
    logout_req = requests.get(f" http://{host}:5380/api/user/logout?token={token}")
    print(logout_req.json)


def update_record(id,ip,mac_raw):
    token = dhcp_login()
    # mac = mac_raw.replace("-",":")
    mac = mac_raw

    static_req = requests.get(f"http://{host}:5380/api/dhcp/scopes/addReservedLease?token={token}&name=Home_Default&hardwareAddress={mac}&ipAddress={ip}&hostName={id}")
    print(static_req.text)

    dhcp_logout(token)


#* the main land
update_machine()
