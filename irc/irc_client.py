"""
Python IRC module that targets Root-Me services
Author : Quatrecentquatre-404
Date : 13/02/2022
"""
import socket
import random
import string

# Constants
global HOST, PORT, CHANNEL, BOT, BUFFER_SIZE
HOSTNAME = "irc.root-me.org"
SERVERNAME = "root-me.org"
PORT = 6667
CHANNEL = "#root-me_challenge"
BOT = "Candy"
BUFFER_SIZE = 2 ** 18

# Variables
global username, client
username = 'A' + ''.join([random.choice(string.hexdigits) for _ in range(7)])
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOSTNAME, PORT))


def authenticate():
    print("[+] Authentication ...")
    print("[+] Username : {} ...".format(username))
    client.send(("NICK {}\r\n".format(username)).encode())
    client.send(("USER {} {} {} {} :{}\r\n".format(
        username, HOSTNAME, SERVERNAME, username, username)).encode())
    while True:
        data = client.recv(BUFFER_SIZE)
        for line in data.splitlines():
            if line.startswith(b":irc.hackerzvoice.net 376"):
                print("[+] Authenticated !")
                print("[+] Joining channel {} ...".format(CHANNEL))
                client.send(("JOIN {}\r\n".format(CHANNEL)).encode())
                print("[+] Channel joinned !")
                return


def handle_ping(message: bytes):
    print("[+] Handling ping ...")
    dest = message.decode()[len("PING :"):]
    client.send(("PONG {}\r\n".format(dest)).encode())
    print("[+] Pong {} ...".format(dest))


def disconnect():
    print("[+] Leaving ...")
    client.send("QUIT :bye\r\n".encode())
    client.close()


def get_challenge(challenge_id: int) -> str:
    print("[+] Getting challenge ...")

    while True:
        client.send(("PRIVMSG {} :!ep{}\r\n".format(BOT, challenge_id)).encode())
        data = client.recv(BUFFER_SIZE)
        if len(data) == 0:
            break
        if data.startswith(b"PING :"):
            handle_ping(data)
            continue
        if b"PRIVMSG" in data and b"Candy!" in data:
            print(data.decode())
            return data.decode()[len(":{}!{}@{} PRIVMSG {} :".format(BOT, BOT, SERVERNAME, username)):]


def submit(challenge_id: str, answer: str):
    print("[+] Submitting answer ...")
    client.send(("PRIVMSG {} :!ep{} -rep {}\r\n".format(BOT, challenge_id, answer)).encode())
    print("[+] Answer submitted !")
    while True:
        data = client.recv(BUFFER_SIZE)
        if len(data) == 0:
            break
        if data.startswith(b"PING :"):
            handle_ping(data)
            continue
        if b"PRIVMSG" in data:
            return data.decode()[len(":{}!{}@{} PRIVMSG {} :".format(BOT, BOT, SERVERNAME, username)):]
