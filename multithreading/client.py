import socket

from _thread import *
import threading

if __name__ == "__main__":
    server_ip = 'localhost'

    port = 12345 

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((server_ip,port))

    raw_msg = 'HI SERVER'

    while True:
        client_socket.send(raw_msg.encode('utf-8'))

        server_msg = client_socket.recv(1024)
        server_msg = server_msg.decode('utf-8')

        print('message received from server : '+server_msg)

        ans = input('hey you wanna continue(y/n)?')

        if ans == 'y':
            continue
        else:
            break
    
    client_socket.close()

