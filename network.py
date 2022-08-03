import json

def send_msg(s, msg: str, checksum: str):
    """
    Envoie de message entre le client et le serveur
    :param s: est le socket
    :param msg: est le message envoyé entre le client et le serveur via le socket
    :param checksum: est la somme de contrôle du message
    """
    size_msg = len(msg)
    s.send(size_msg.to_bytes(4, byteorder="big"))
    s.send(msg.encode())
    size_checksum = len(checksum)
    s.send(size_checksum.to_bytes(16, byteorder='big'))
    s.send(checksum.encode())


def recv_msg(conn):
    """
    reception du message envoyer par le client
    :param conn est la connexion entre le serveur et le client:
    :return: retourne une liste du message et de son checksum
    """
    len_msg_bytes = conn.recv(4)
    size_msg = int.from_bytes(len_msg_bytes, byteorder='big')
    msg = conn.recv(size_msg).decode()
    len_checksum_bytes = conn.recv(16)
    size_checksum = int.from_bytes(len_checksum_bytes, byteorder='big')
    checksum = conn.recv(size_checksum).decode()
    return [msg, checksum]


def send_msg_dict(s, msg):
    """
    envoie un message au format dictionnaire (client-serveur) via un socket
    :param s est le socket:
    :param msg est le message en format de dictionnaire envoyé entre le client et le serveur via le socket:
    :param checksum est la somme de contrôle du message:
    :return:
    """
    msg_byte = json.dumps(msg).encode('utf-8')
    size_msg = len(msg_byte)
    s.send(size_msg.to_bytes(4, byteorder='big'))
    s.send(msg_byte)


def recv_msg_dict(conn):
    """
    reception du message sous format dictionnaire du client
    :param conn: est la connexion entre le client et le serveur
    :return:  retourne une liste du message et de son checksum
    """
    len_msg_bytes = conn.recv(4)
    size_msg = int.from_bytes(len_msg_bytes, byteorder='big')
    msg = conn.recv(size_msg)
    msg2 = json.loads(msg.decode())
    return msg2

