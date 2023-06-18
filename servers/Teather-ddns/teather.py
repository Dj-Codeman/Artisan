#!/usr/sbin/python3
# this is at home
version="1.0a"

import os
from requests import get

ip_addr = get('https://api.ipify.org').content.decode('utf8')
teather_addr = "teather_01.artisanhosting.net"

print(f"ip: {ip_addr}")

#! copying to the static host 
os.system(f"echo {ip_addr} > /tmp/ip_addr")

#! Sending update commands for the host
scp_send = f"scp -v /tmp/ip_addr root@{teather_addr}:/tmp/ip_addr"

os.system(scp_send)
