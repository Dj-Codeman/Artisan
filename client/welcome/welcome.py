#! /usr/bin/python3

# A Custom Welcome message that will integrate with other infrastructure 
version = "2.1"
# getting system data
import platform,socket,psutil,os
svmem = psutil.virtual_memory()
uname = platform.uname()
artisan_version = os.popen("artisan --version-cli").read().rstrip()

system_version = uname.release
system_hostname = socket.gethostname()
system_cpu_usage = f"{psutil.cpu_percent(2)}%"
system_mem_usage = f"{svmem.percent}%"


welcome_text = f"""
                  _    _                         _    _              _    _
     /\          | |  (_)                       | |  | |            | |  (_)
    /  \    _ __ | |_  _  ___   __ _  _ __      | |__| |  ___   ___ | |_  _  _ __    __ _
   / /\ \  | '__|| __|| |/ __| / _` || '_ \     |  __  | / _ \ / __|| __|| || '_ \  / _` |
  / ____ \ | |   | |_ | |\__ \| (_| || | | |    | |  | || (_) |\__ \| |_ | || | | || (_| |
 /_/    \_\|_|    \__||_||___/ \__,_||_| |_|    |_|  |_| \___/ |___/ \__||_||_| |_| \__, |
                                                                                     __/ |
                                                                                    |___/   

Your machine at a glance:

Os Version   : Debian {system_version}
Artisan Mgmt : {artisan_version}
Hostname     : {system_hostname}
Cpu Usage    : {system_cpu_usage}
Mem Usage    : {system_mem_usage}


Welcome!

This server is hosted by Artisan Hosting. If you have any questions or need help,
please don't hesitate to contact me at dwhitfield@artisanhosting.net or shoot me a text at 414-578-0988.
"""

print(welcome_text)