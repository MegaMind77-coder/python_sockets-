import socket 
import select 
import sys

server_port = 12345
server_ip = 'localhost'

try:
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
  print(f'an error occured while creating socket{err}')

try:
  client_socket.connect((server_ip, server_port))
except socket.error as err:
  print(f'error while connecting to server :{err}')

game_running = True
response_state = 0
timeout = 10
while game_running:
  
  type_of_inputs = select.select([sys.stdin, client_socket],[],[], )[0]
  for input_src in type_of_inputs:
    if input_src == client_socket:
      server_message = client_socket.recv(1024)
      server_message = server_message.decode('ascii')
      response_type = server_message[0:3]
    #  print(response_type)
      new_message = server_message[3:]
    #  print(new_message)
      if response_type == 'kll':
        game_running = False
      
      elif response_type == 'can':
        print(new_message)
        response_state = 1

      elif response_type == 'bzz':
        response_state = 0

      elif response_type == 'ans':
        response_state =2

      elif response_type == 'rst':
        response_state =  0
      
      elif response_type == 'prn':
        print('\n'+new_message)
    
    else:
      client_response = sys.stdin.readline()
      if response_state == 1:
          client_socket.send('bzz'.encode('ascii'))
      elif response_state == 2:
          client_response = 'ans'+client_response
          client_socket.send(client_response.encode('ascii'))

client_socket.close()