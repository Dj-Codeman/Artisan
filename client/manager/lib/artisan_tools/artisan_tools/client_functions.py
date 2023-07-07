#!/usr/bin/python3
# import random,string
import os,sys
import zipfile
import requests
import artisan_tools.machine_functions as artisan

# ! Artisan Tools Version
version = "3.00"

#! Global things
connection = artisan.create_server_connection("database.local", "artisan", artisan.decrypt_creds("database"))

if os.path.exists("/etc/artisan.mid"):
    with open("/etc/artisan.mid", 'r') as file:
        machine_id = file.read().rstrip()

def resolve_client(cid):
    query = f"SELECT * FROM client_id WHERE client_id = '{cid}'"
    client_data = artisan.read_query(connection, query)
    return client_data

def download_wp():
    wp_url = "https://wordpress.org/latest.zip"
    req = requests.get(wp_url, allow_redirects=True)
    open('/tmp/wp.zip', 'wb').write(req.content)

def configure_apache(username, pn):

    # Getting right with apache2 
    print(f"Machine {machine_id}: Provisioning : {username} \n")
    web_folder = f"/var/www/wordpress_{username}"
    a2_conf = f"/etc/apache2/sites-available/wordpress_{username}.conf"

    # * Unzipping wp to the right folder
    with zipfile.ZipFile("/tmp/wp.zip", 'r') as zip_ref:
        zip_ref.extractall(f"{web_folder}")
        os.system(f"chown -Rv webman:server {web_folder}")

    # ! adding the webfolder and permissions 
    if os.path.exists(web_folder) == False:
        print(f"Machine {machine_id}: Installing Lastest WP \n")
        with zipfile.ZipFile("/tmp/wp.zip", 'r') as zip_ref:
            zip_ref.extractall(f"{web_folder}")
        os.system(f"chown -Rv webman:server {web_folder}")

    # ! Creating the apache conf 
    print(f"Machine {machine_id}: Apache I've Come To BARGIN ! \n")
    with open("/usr/local/bin/Artisan/static/apache2.stub") as infile, open(f"/tmp/apache.tmp", 'w') as outfile: 
       for line in infile:
           outfile.write(line.replace("PN", f'{pn}'))

    with open("/tmp/apache.tmp") as infile, open(f"{a2_conf}", 'w') as outfile:
       for line in infile:
           outfile.write(line.replace("/var/www/wordpress_demo-0000", f'{web_folder}/wordpress'))

    os.system(f"a2ensite wordpress_{username}.conf > /dev/null")

def configure_firewall(username, pn):
    # ! allowing the firewall rule
    print(f"Machine {machine_id}: Applying firewall rules for {username} \n")
    os.system(f"ufw allow {pn}/tcp > /dev/null")
    
    # ! adding the port to the apache ports file 
    with open("/etc/apache2/ports.conf", 'a') as config:
        config.write(f"Listen {pn.rstrip()}\n")

def finish_adding_user(username, cid, pn):
    print(f"Machine {machine_id}: Enabeling {username}'s site ! \n")
    os.system(f"systemctl reload apache2")

    query = f"UPDATE client_id SET client_hs = 'TRUE' WHERE client_id = '{cid}';"
    artisan.write_query(connection, query)
    print(f"Machine {machine_id}: {username} is home now ! \n")

    with open("/etc/artisan.cid") as input:
        # Read non-empty lines from input file
        lines = [line for line in input if line.strip()]
    
    with open("/etc/artisan.cid", "w") as output:
        for line in lines:
            output.write(line.rstrip())
        output.write(f"{cid},")



def add_clients(array):
    for client in array:
        print(f"Machine {machine_id}: Resolving client: {client}\n")
        client_data = resolve_client(client)

        # * Reading the magical client data array
        for data in client_data:
            client_id = data[0]
            client_fn = data[1]
            client_ln = data[2]
            client_pn = data[3]
            client_ip = data[4]
            client_hs = data[5]

            # * Orentating user info
            username = f"{client_fn[0]}{client_ln}-{client_id}"
            print(f"Machine {machine_id}: Provisioning : {username} \n")

            query = f"UPDATE client_id SET client_ip = '{artisan.get_ip()}' WHERE client_ip = '{client_ip}'"
            artisan.write_query(connection, query)

            # Downloading wordpress
            print(f"Machine {machine_id}: Downloading Lastest WP \n")
            
            download_wp()
            configure_apache(username, client_pn)
            configure_firewall(username, client_pn)
            finish_adding_user(username, client_id, client_pn)

            print(f"Machine {machine_id}: Done adding : {username} ! Changes may take up to 60 seconds to propogate \n")
            artisan.send_email(f"NOTICE: user {username} has been registered on {machine_id} with port num {client_pn}")




def sus_clients(array):
    for client in array:
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
            artisan.write_query(connection, query)
                    
            # ! updating the cid file
            with open("/etc/artisan.cid") as infile, open(f"/tmp/artisan.cid", 'w') as outfile: 
                for line in infile:
                    outfile.write(line.replace(f"{client_id.rstrip()},", ''))
                   
            # ! delete old and copy new
            os.remove("/etc/artisan.cid")
            os.rename("/tmp/artisan.cid", "/etc/artisan.cid")
            sys.exit(0)