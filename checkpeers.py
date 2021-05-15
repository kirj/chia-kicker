#! /usr/bin/python3

import subprocess
import shlex
import re
import socket
import random

port = 8444

whitelist = ['127.0.0.1', '4.4.4.4']

chia = "chia" # local installation
# chia = "docker exec -it chia-node venv/bin/chia" # docker

def checkPort(ip):
    try:
        sock = socket.create_connection( (ip, port), 2)
        sock.close()
        print(f" {ip}:{port} ok")
        return True
    except Exception as e: 
        print(f" {ip}:{port} {e}")
        return False

def kickEm(ip, hash):
    if ip in whitelist:
        return
    # kick every nth?
    onein = 10
    if (random.randint(1, onein) == onein):
        print(f"* {ip} {hash} lost")
        eschash = shlex.quote(hash)
        print ( subprocess.check_output(f"{chia} show -r {eschash}", shell=True, encoding='UTF-8')) 
        return True
    return False
    

if 0:  # test some ips
    checkPort("127.0.0.1")  # maybe open
    checkPort("10.10.10.1") # unreachable
    checkPort("8.8.8.8")   # maybe closed

conn = subprocess.check_output(f"{chia} show -c", shell=True, encoding='UTF-8')

open = 0
close = 0
kicked = 0

for c in conn.split("\n"):

    # get the ip from lines like:
    # FULL_NODE 5.9.50.158                             49752/8444  5dad6841... May 14 16:32:38      0.1|1.8    
    # note: this RE won't work for ipv6 addreses or hostnames:
    m = re.match(".+NODE +([0-9.]+) +\d+/\d+ +(.+)\.\.\..*", c)
    if (m):
        ip = m.group(1)
        hash = m.group(2)
        if checkPort(ip):
            open += 1
        else:
            close += 1
            if kickEm(ip, hash):
                kicked += 1

print(f"found {open} open host and {close} closed hosts. Kicked {kicked}")            
        
        
    
