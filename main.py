# Author: Captcha
from appJar import gui
import socket
import os





hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


if (ip_address != '192.168.0.113'):
    exit()
print(f"Hostname: {hostname}")
os.system('cls')









