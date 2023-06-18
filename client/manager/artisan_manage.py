#!/usr/bin/python3

import os, sys
import fcntl, socket, struct
import mysql.connector
import random,string
# import csv
import zipfile
import requests

from mysql.connector import Error
import smtplib
from email.message import EmailMessage

version = "2.1"

try:
    arg = sys.argv[1]
except IndexError:
    print('-')
else:
    if arg == "--version-cli":
        print(version)
        sys.exit(0)

    if arg == "--version":
        print(f"Version {version}")
        sys.exit(0)
    
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
        # print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

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
        print(f"Error: '{err}'")\

# ! Pulling mac addr
def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
    return '-'.join('%02x' % b for b in info[18:24])

# ! pulling ip addr
def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    # print(get_ip())


# ! Generating the uuid
def uuid_gen():
    first = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    second = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    uuid = f"{first}-{second}"
    return uuid

def initialize():
    # first we see if the system has been initialized
    sanatize_cid()
    if os.path.isfile("/etc/artisan.mid"):
        with open("/etc/artisan.mid", 'r') as file:
            uuid = file.read().rstrip()
        update_uuid(uuid)

    else:
        uuid = uuid_gen()
        # registering the uuid with the database
        register_uuid(uuid)

# ! Sanatizing the client id file 
def sanatize_cid():
    cid = "/etc/artisan.cid"
    cid_t = "/tmp/artisan.cid"
    # os.rename("/etc/artisan.cid", "/etc/artisan.cid.old")
    # os.rename(f"{cid_t}", f"{cid}")


# ! resolving clinet data
def resolve_client(cid):
    connection = create_server_connection("database.local", "artisan", "Artisan610!") # ! this needs to be encrypted and read from a file
    query = f"SELECT * FROM client_id WHERE client_id = '{cid}'"

    client_data = read_query(connection, query)
    return client_data
    
# ! Registering and updating the machine 
def register_uuid(uuid):
    # determining the type of system with the num of cores
    num_cores = os.cpu_count()
    
    if num_cores > 1 :
        machine_type = "Big"
    else :
        machine_type = "Little"

    # get system mac address 
    mac_addr = getHwAddr("ens18")

    # insert this into the db 
    connection = create_server_connection("database.local", "artisan", "Artisan610!") # ! this needs to be encrypted and read from a file

    # * Query to initially register the machine
    query = f""" INSERT INTO machine_id ( uuid, machine_type, machine_mac ) 
                VALUES ( '{uuid}', '{machine_type}', '{mac_addr}' ); """

    # updating the cursor and attempting the write
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        connection.commit()
        message = f"Machine registered, mac: {mac_addr}"
        print(message)
        send_email(message)
    except Error as err:
        message = f"Could not register Machine mac: {mac_addr}, Error: '{err}'"
        print(message)
        send_email(message)

    # writtig the registration file to the system    
    registration_file = open("/etc/artisan.mid", "w")
    registration_file.write(f"{uuid}")
    registration_file.close()

def update_uuid(uuid):

    # mysql prep 
    connection = create_server_connection("database.local", "artisan", "Artisan610!") # ! this needs to be encrypted and read from a file

    query = f"SELECT * FROM machine_id WHERE uuid = '{uuid}';"
    cursor = connection.cursor()
    result = None
    
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except Error as err:
        message = f"Could not update Machine, Error: '{err}'"
        send_email(message)

    for data in result:

        machine_id = data[0]
        machine_type = data[1]

        print(f"Machine : {machine_id} Type : {machine_type} Action : Updating \n")

        current_mac = getHwAddr("ens18")
        # current_mac = getHwAddr("enp0s31f6")
        stored_mac = data[2]

        if current_mac != stored_mac:
            send_email(f"HEY! floating mac addr on machine {machine_id} ! Site might be unavailable")
            sys.exit(111)

        current_ip = get_ip()    
        stored_ip = data[3]

        if current_ip != stored_ip:
            print(f"Machine {machine_id}: New ip assigned updating \n")
            os.system("dhclient -v -r") # * releasing the old ip
            os.system("dhclient -v") # * requesting the new one
            send_email(f"Machine: {machine_id} has applied the assinged ip {stored_ip}")


        #! Managing the Client info 
        new_client = data[4]

        with open("/etc/artisan.cid", 'r') as file:
            local_client = file.read().rstrip()
            if len(local_client) == 0:
                local_client = None
                
        # ? if both empty or same
        #! setting the len to 1 if there empty
        if new_client == None:
                new_client = ','

        if local_client == None:
                local_client = ','

        if new_client == local_client and local_client == None:
                print(f"Machine {machine_id}: No clients currently registered \n")
                sys.exit(0)

        elif new_client == local_client:
                print(f"Machine {machine_id}: No client updates ... \n")
                sys.exit(0)

        elif new_client != local_client and len(new_client) > len(local_client):
            print(f"Machine {machine_id}: Updating client list (adding)\n")
            updated_client = new_client.replace(f"{local_client}","")
            
            # read comma delm list
            for client in updated_client.split(','): # ! REPLACING A CLIENT OUT RIGHT WILL NOT WORK
                print(f"Machine {machine_id}: Resolving client: {client}\n")
                client_data = resolve_client(client)
                
                for data in client_data:
                    client_id = data[0]
                    client_fn = data[1]
                    client_ln = data[2]
                    client_pn = data[3]
                    client_ip = data[4]
                    client_hs = data[5]

                    username = f"{client_fn[0]}{client_ln}-{client_id}"
                    
                    # making the new wordpress instance
                    # * assembeling username
                  
                    print(f"Machine {machine_id}: Provisioning : {username} \n")
                   
                    # * updating the ip on db 
                    query = f"UPDATE client_id SET client_ip = '{stored_ip}' WHERE client_id = '{client_id}'"
                    execute_query(connection, query)
                   
                    # * Downloading the latest wordpress zip
                    print(f"Machine {machine_id}: Downloading Lastest WP \n")
                    wp_url = "https://wordpress.org/latest.zip"
                    req = requests.get(wp_url, allow_redirects=True)
                    open('/tmp/wp.zip', 'wb').write(req.content)
                    
                    # Getting right with apache2 
                    web_folder = f"/var/www/wordpress_{username}"
                    a2_conf = f"/etc/apache2/sites-available/wordpress_{username}.conf"
                   
                    # ! adding the webfolder and permissions 
                    if os.path.exists(web_folder) == False:
                        print(f"Machine {machine_id}: Installing Lastest WP \n")
                        with zipfile.ZipFile("/tmp/wp.zip", 'r') as zip_ref:
                            zip_ref.extractall(f"{web_folder}")
                        os.system(f"chown -Rv webman:server {web_folder}")
                    
                    # ! Creating the apache conf 
                    print(f"Machine {machine_id}: Apache I've Come To BARGIN ! \n")
                    # with open("/var/scripts/apache2.stub") as infile, open(f"{a2_conf}", 'w') as outfile:
                    with open("/var/scripts/apache2.stub") as infile, open(f"/tmp/apache.tmp", 'w') as outfile: 
                       for line in infile:
                           outfile.write(line.replace("PN", f'{client_pn}'))

                    with open("/tmp/apache.tmp") as infile, open(f"{a2_conf}", 'w') as outfile:
                       for line in infile:
                           outfile.write(line.replace("/var/www/wordpress_demo-0000", f'{web_folder}/wordpress'))
                   
                    # ! allowing the firewall rule
                    print(f"Machine {machine_id}: Applying firewall rules for {username} \n")
                    os.system(f"ufw allow {client_pn}/tcp > /dev/null")
                    
                    # ! adding the port to the apache ports file 
                    with open("/etc/apache2/ports.conf", 'a') as config:
                        config.write(f"Listen {client_pn.rstrip()}\n")
                    
                    # ! ENABELING THE SITE 
                    print(f"Machine {machine_id}: Enabeling {username}'s site ! \n")
                    os.system(f"a2ensite wordpress_{username}.conf > /dev/null")
                    os.system(f"systemctl reload apache2")
                    print(f"Machine {machine_id}: {username} is home now ! \n")
                    
                    # ! home the client
                    query = f"UPDATE client_id SET client_hs = 'TRUE' WHERE client_id = '{client_id}';"
                    execute_query(connection, query)
                    
                    # ! Adding to the cid
                    sanatize_cid()
                    with open("/etc/artisan.cid") as input:
                        # Read non-empty lines from input file
                        lines = [line for line in input if line.strip()]
                    with open("/etc/artisan.cid", "w") as output:
                        for line in lines:
                            output.write(line.rstrip())
                        output.write(f",{client_id}")

                    print(f"Machine {machine_id}: Done adding : {username} ! Changes may take up to 60 seconds to propogate \n")
                    send_email(f"NOTICE: user {username} has been registered on {machine_id} with port num {client_pn}")
                   
                    # ! Need to make the db still
                    if client_hs:
                        print(f"Machine {machine_id}: Health check {username}")
                    sys.exit(0)
            
        elif new_client != local_client and len(new_client) < len(local_client):
            print(f"Machine {machine_id}: Updating client list (suspending)\n")
            updated_client = local_client.replace(f"{new_client}", '')
            
            for client in updated_client.split(','):
                print(f"Machine {machine_id}: Resolving client: {client}\n")
                client_data = resolve_client(client)

                for data in client_data:

                    client_id = data[0]
                    client_fn = data[1]
                    client_ln = data[2]
                    client_pn = data[3]
                    client_hs = data[5]

                    username = f"{client_fn[0]}{client_ln}-{client_id}"

                    print(f"Machine {machine_id}: De-provisioning : {username} \n")
                    # suspending the apache site
                    os.system(f"a2dissite wordpress_{username}.conf > /dev/null")
                    
                    with open("/etc/apache2/ports.conf") as infile, open(f"/tmp/ports.tmp", 'w') as outfile: 
                        for line in infile:
                            outfile.write(line.replace(f"Listen {client_pn}\n", ''))
                    
                    # ! delete old and copy new
                    os.remove("/etc/apache2/ports.conf")
                    os.rename("/tmp/ports.tmp", "/etc/apache2/ports.conf")
                    os.system(f"systemctl reload apache2")
                    
                    print(f"Machine {machine_id}: Reverting firewall \n")
                    os.system(f"ufw delete allow {client_pn}/tcp > /dev/null")
                    
                    print(f"Machine {machine_id}: Making {username} homeless \n")
                   
                    query = f"UPDATE client_id SET client_ip = '10.1.0.000', client_hs = 'False' WHERE client_id = '{client_id}';"
                    execute_query(connection, query)
                    
                    # ! updating the cid file
                    with open("/etc/artisan.cid") as infile, open(f"/tmp/artisan.cid", 'w') as outfile: 
                        for line in infile:
                            outfile.write(line.replace(f",{client_id.rstrip()}", ''))
                   
                    # ! delete old and copy new
                    os.remove("/etc/artisan.cid")
                    os.rename("/tmp/artisan.cid", "/etc/artisan.cid")
                    sys.exit(0)

initialize()
