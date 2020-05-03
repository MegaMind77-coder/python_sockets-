import socket

headersize = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))


while True:
    full_msg = ''
    new = True
    msglen = 0
    while True:
        msg = s.recv(16)
        if new:
            print("new msg length:",msg[:headersize])
            msglen = int(msg[:headersize])
            new = False

        print(f"full message len: {msglen}")
        full_msg += msg.decode("utf-8")
        print(len(full_msg))

        if len(full_msg) - headersize == msglen:
            print("full msg received")
            print("full msg:" + full_msg[headersize:])
            new = True