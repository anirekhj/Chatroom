import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
#from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA

# init colors
init()

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
          Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
          Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
          Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
          ]

# choose a random color for the client
client_color = random.choice(colors)

# server's IP address
# if the server is not on this machine,
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002  # server's port
separator_token = "<SEP>"  # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

# prompt the client for a name
name = input("Enter your name: ")
prkey = RSA.import_key(open('A-private.key').read())

hashed = SHA256.new("A".encode())
print(hashed)

signer = pkcs1_15.new(prkey)
sig = signer.sign(hashed)
#print("++"+sig+"++")

state = 0


def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)


# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

while True:
    if state == 0:
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        to_send = f"{name}{separator_token}{sig}"
        name_byte = bytes(name, 'utf-8')
        print(name_byte)
        print(len(name_byte))
        con = name_byte+sig
        print(con)
        print(len(con))
        #to_send = name.encode() + b' ' + str(state).encode() + b' ' + sig
        #to_send = {"name": name.encode(), "state": str(state).encode(), "sig": sig}
        #to_send = [name, auth, sig]
        # finally, send the message
        s.send(con)
        #s.send(to_send.encode())
        #to_send = [sig]

        state = 1
    elif state == 1:
        #s.send(sig)
        state = 2

    else:

        # input message we want to send to the server
        to_send = input()
        # a way to exit the program
        if to_send.lower() == 'q':
            break
        # add the datetime, name & the color of the sender
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
        # finally, send the message
        s.send(to_send.encode())

# close the socket
s.close()
