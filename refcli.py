import socket
import os
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
import string



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
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")
# prompt the client for a name
name = input("Enter your name: ")
if name not in ["A","B","C"]:
    print("Incorrect User Name")
    s.send("ERR: Incorrect User Name provided by the client".encode())
    quit()

key_file = f'{name}-private.key'
prkey = RSA.import_key(open(key_file).read())

hashed = SHA256.new(name.encode())

signer = pkcs1_15.new(prkey)
sig = signer.sign(hashed)

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
    # input message we want to send to the server
    if state == 0: #auth
        name_byte = bytes(name, 'utf-8')
        con = name_byte + sig
        s.send(con)
        if s.recv(1024).decode() == "All parties have authed succussfully":
            state = 1
        else:
            state = 4 #waiting
    if state == 1: #key exchange
        randi = name.join(random.choices(string.ascii_letters + string.digits + "-" + "_", k = 14))
        s.send(randi.encode())
        state = 4
    if state == 2: #message exchange
        to_send =  input()
        # a way to exit the program
        if to_send.lower() == 'q':
            break
        # add the datetime, name & the color of the sender
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
        # finally, send the message
        s.send(to_send.encode())
    else:
        continue
# close the socket
s.close()

random_key = os.urandom(16)
print(random_key.decode("utf-16"))
# A to B: {Na}Kb, {H(Na)}Ka^-1
# A to C: {Na}Kc, {H(Na)}Ka^-1
# B to C: {Nb}Kc, {H(Nb)}Kb^-1
# B to A: {Nb}Ka, {H(Nb)}Kb^-1
# C to A: {Nc}Ka, {H(Nc)}Kc^-1
# C to B: {Nc}Kb, {H(Nc)}Kc^-1
randi = ''.join(random.choices(string.ascii_letters + string.digits + "-" + "_", k = 14)) + "="
k = Fernet.generate_key()
fernet = Fernet(k)
f = fernet.encrypt(test.encode())
print("length of k: ", len(k))
print(k)
print("symetric cipher: ", f)