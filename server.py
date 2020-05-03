import socket

headersize = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
    clientSocket, address = s.accept()
    # clientSocket is the socket object of the client
    print(f"New Connection established : Client {address}")
    msg =  "welcome to the hood!"
    msg = f"{len(msg):<{headersize}}" + msg

    clientSocket.send(bytes(msg, "utf-8"))