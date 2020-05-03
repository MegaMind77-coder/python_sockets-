import socket

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print(f'failed to create socket with {err}')

client_socket.bind(('',1234))

server_port = 12347

client_socket.connect(('localhost',server_port))

msg = client_socket.recv(1024)
raw_msg = msg.decode('utf-8')
print(raw_msg)
client_socket.close()