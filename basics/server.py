import socket 

PORT = 12347
SERVER_IP = 'localhost'

try:
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('socket has been created successfully')
except socket.error as err:
    print(f'failed to create socket with error {err}')


server_socket.bind((SERVER_IP,PORT))

server_socket.listen()

client_sockets = []
client_ips = []

while True:
    client_socket, client_ip = server_socket.accept()
    if client_ip not in client_ips :
        client_sockets.append(client_socket)
        client_ips.append(client_ip)
        msg = 'hello'
        client_socket.send(msg.encode('utf-8'))
        client_socket.close()

    if len(client_sockets) == 2:
        break

