import socket

host_name = socket.gethostname()
ip_add = socket.gethostbyname(host_name)
print host_name
print ip_add
