import pickle 
import socket

headersize = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1273))
s.listen(5)

while True:
    clientSocket, address = s.accept()
    # clientSocket is the socket object of the client
    print(f"New Connection established : Client {address}")
    d = {1:"hey",2:"there"}
    msg = pickle.dumps(d)
    msg = bytes(f"{len(msg):<{headersize}}","utf-8") + msg
    clientSocket.send(msg)
