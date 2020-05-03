import socket 
import pickle

headersize = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1273))


while True:
    full_msg = b''
    new = True
    msglen = 0
    while True:
        msg = s.recv(16)
        if new:
            print("new msg length:",msg[:headersize])
            msglen = int(msg[:headersize])
            new = False

        print(f"full message len: {msglen}")
        full_msg += msg
        print(len(full_msg))

        if len(full_msg) - headersize == msglen:
            print("full msg received")
            print("full msg:" )
            print(pickle.loads(full_msg[headersize:]))
            new = True
            full_msg = b''