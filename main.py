import socket
from threading import Thread

# server's IP address
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

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


def listen_for_client(cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024)
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            signature = msg[1:]
            if True:

                #print(hashed)

                try:
                    #pkcs1_15.new(RSA.import_key(open(f"{client_name}-public.key").read())).verify(hashed, signed_hash)
                    prkey = RSA.import_key(open('A-private.key').read())

                    hashed = SHA256.new("A".encode())
                    #print(hashed)

                    signer = pkcs1_15.new(prkey)
                    sig = signer.sign(hashed)
                    hashed = SHA256.new("A".encode())
                    pkey = RSA.import_key(open('A-public.key').read())

                    pkcs1_15.new(pkey).verify(hashed, signature)
                    print("Valid")
                except (ValueError, TypeError):
                    print("invalid")
        for client_socket in client_sockets:
            # and send the message
            #client_socket.send(msg.encode())
            None

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
