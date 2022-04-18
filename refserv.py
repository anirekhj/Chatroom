import socket
from threading import Thread
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

# server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # port we want to use
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize list/set of all connected client's sockets
client_sockets = set()
# create a TCP socket
s = socket.socket()
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
state = 0
valid_clients = 0

def listen_for_client(cs):
    global valid_clients
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
       
        while(valid_clients < 3):
            try:
                msg = cs.recv(1024)
            except Exception as e:
                print(f"[!] Error: {e}")
                client_sockets.remove(cs)
            if state == 0:
                signature = msg[1:]
                try:
                    hashed = SHA256.new(msg[0:1])
                    key_file = f'{msg[0:1].decode()}-public.key'
                    pkey = RSA.import_key(open(key_file).read())

                    pkcs1_15.new(pkey).verify(hashed, signature)
                    print("Valid")
                except (ValueError, TypeError):
                        print("invalid")
                # and send the message
                cs.send(msg[0:1]+" has been authed successfully.".encode())
                valid_clients += 1
        
        # iterate over all connected sockets
        for client_socket in client_sockets:
            # and send the message
            client_socket.send("All parties have authed succussfully".encode())
        print(client_sockets)
        
        for client_socket in client_sockets:
            print(client_socket.recv(1024))
            client_socket.send(client_socket.recv(1024))


while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket,))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()