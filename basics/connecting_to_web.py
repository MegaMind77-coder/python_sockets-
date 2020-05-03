import socket 

client_ip = ''


target_ip = socket.gethostbyname('www.google.com')
target_port = 80

client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.bind(('',1453))
client_socket.connect((target_ip,target_port))
