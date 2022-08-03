import socket
import sqlite3
from _thread import start_new_thread
import network
from datetime import datetime
from time import time
from math import floor
import ssl

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(certfile='cert.crt', keyfile='private.key')


def threaded(conn:socket):
    key_user = network.recv_msg_dict(conn)
    print(key_user, datetime.fromtimestamp(floor(time())))
    with open('key.txt', 'a') as file:
        file.write(str(key_user) + str(datetime.fromtimestamp(floor(time()))) + '\n')

#ToDo: Do a db for computers and key


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind(('', 4107))
    s.listen(1)
    while True:
        with ctx.wrap_socket(s, server_side=True) as ssock:
            print('Listen...')
            conn, addr = ssock.accept()
            print('Connected by ', addr[0], ':', addr[1])
            start_new_thread(threaded, (conn,))
