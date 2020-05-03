import socket 

from _thread import *
import threading

print_lock = threading.Lock()

def newThread(client_socket):
    while True:

        msg = client_socket.recv(1024)
        raw_msg = msg.decode('utf-8')
        if not raw_msg:
            print('BYE')

            print_lock.release()
            break
        raw_msg = raw_msg[::-1]
        
        server_msg = raw_msg
        server_msg = server_msg.encode('utf-8')
        client_socket.send(server_msg)
    
    client_socket.close()   


if __name__ == "__main__":
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))

    server_socket.listen(5)
    print(f'server is live on port {port}')
    
    while True:
        client_socket, client_ip = server_socket.accept()

        print_lock.acquire()

        print('Connected to :', client_ip[0], ':', client_ip[1]) 

        start_new_thread(newThread,(client_socket,))

    server_socket.close()
        
    pass