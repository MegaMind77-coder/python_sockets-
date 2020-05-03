import socket #for TCP sockets
from random import shuffle #for shuffling the questions from the json file
import threading
from _thread import * #the basic threading module of python
import time #for managing the time 
from threading import Lock #for creating the lock object required to lock a particular thread
import select
from questions import *

server_ip = 'localhost' #ipaddress on which server would function
server_port = 12345 #socket number on which server receives connections

client_sockets = [] #list to manage all the players, stores the socket object of all the players 
client_addresses = [] #list wouch contain the address tuples of the connected clients/players
player_scores = []

thread_lock = threading.Lock() #creating a global lock object


questions = qs['master']
shuffle(questions)

game_rules = '''\n\n
1.Every player would be sent a question.
2.After receiving the te question, you would have 10 second to press the buzzer.
3.The first person to press the buzzer would be able to answer a question(only 10 second would be given to answer), wherein you only need to type in te option number and press enter
4.If your answer is correct, you would be awarded wit 1 point else 0.5 points will be deducted from your score.
5.The question would be asked until one player attains a score of 5 and that person would be the winner.
6.Good Luck :)))
PS: you only need to press any key and press enter to buzz for a question.
\n\n
'''


max_points = 5
buzzer = 'off'

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except socket.error as err:
    print(f'unable to create socket object due to {err}')

try:
    server_socket.bind((server_ip, server_port))
except socket.error as err:
    print(f'unable to bind due too error: {err}')

server_socket.listen(3)
print('server is now live and open to connections')


def send_to_all(msg):
    global client_sockets
    encoded_msg = (msg).encode('ascii')
    for client in client_sockets:
        client.send(encoded_msg)

running_main_thread = True
question_number = 0

def send_scores():
    global player_scores
    score_msg = '\nPlayer Scores are'
    i = 0
    for x in player_scores:
        score_msg+='\nplayer '+str(i+1) +':'+str(x)
        i+=1
    send_to_all('prn'+score_msg)

def declare_winners(players):
   # score_sheet = "\n\n Score of Allpayers \n 1. "+str(player_scores[0])+"\n2. "+str(player_scores[1])+"\n3. "+str(player_scores[2])+"\n.............."
    send_to_all('prn'+'\nThe winners are: \n')
    
    for player in players:
        send_to_all('prn'+'the winner is player '+str(player+1))
        send_to_all('\n')
    send_to_all('prn'+'final score card')
    send_scores()



def buzzer_handler(client_socket, player_num):
    global buzzer
    global thread_lock
    global player_scores
    byte_msg = client_socket.recv(1024)
    if byte_msg.decode('ascii')=='bzz' and buzzer =='off':

        thread_lock.acquire()
        try:
            buzzer = 'pressed'
            print('player number '+str(player_num)+' has buzzed')
        finally:
            thread_lock.release()

        send_to_all('bzz')
        time.sleep(0.001)
        send_to_all('prn'+'player '+str(player_num)+' has pressed the buzzer')
        time.sleep(0.005)

        client_socket.send(('ans'+'you can type in your ans:').encode('ascii'))

       # client_socket.setblocking(0)
        player_ans = 'nill'
        ready = select.select([client_socket],[],[],10)
        
        if ready[0]:
            player_ans = client_socket.recv(1024).decode('ascii')[3:4]
        
        if player_ans == 'nill':
            thread_lock.acquire()
            try :
                buzzer = 'fail'
                time.sleep(0.001)
            finally:
                thread_lock.release()
            
            time.sleep(0.001)
            client_socket.send(('prn'+"\nsorry you ran out of time!!!!").encode('ascii'))
            send_to_all('prn'+"\nplayer ran out of time")

        else:    
            thread_lock.acquire()
            try:
                buzzer = 'evaluate'
                time.sleep(0.001)
            finally:
                thread_lock.release()
            
            time.sleep(0.001)

            if player_ans == questions[question_number]['answer']:
                time.sleep(0.1)
                send_to_all('prn'+'\nplayer '+str(player_num)+' has given the coorect ans')
                player_scores[player_num-1] += 1
                print(player_scores)
            
            else:
                time.sleep(0.1)
                send_to_all('prn'+'\nplayer '+str(player_num)+" has given the incorrect ans")
                player_scores[player_num-1] -= 0.5
                print(player_scores)
            

        send_to_all('prn'+'\nthe correct ans is '+questions[question_number]['answer'])
              

def main_thread():
    
    global running_main_thread
    global question_number
    global player_scores
    global buzzer
    global questions

    while running_main_thread:

        time.sleep(1)
        ques = questions[question_number]

        send_to_all('prn'+'Q : ' + ques['question'])
        time.sleep(0.001)
        send_to_all('can'+'\n' + ques['options'])
        send_to_all('prn' + 'player can press the buzzer now!!!!')
        time.sleep(10)

        if buzzer == 'off':
            send_to_all('prn'+'\nNone of you answered and you guys have lost your time')
            if question_number != len(questions)-1:
                send_to_all('prn'+'\nget ready for the next question')
                send_to_all('rst')
                time.sleep(3)
        
        elif buzzer == 'pressed':
            while buzzer!= 'evaluate':
                if(buzzer == 'fail'):
                    break
                time.sleep(1)
         
        if buzzer == 'evaluate':
            time.sleep(0.01)

            thread_lock.acquire()
            try:
                print('\nevaluation finished')
            finally:
                thread_lock.release()
                send_to_all('rst')            
            time.sleep(0.01)


        if buzzer == 'fail':
            time.sleep(0.01)
            thread_lock.acquire()
            try:
                print('\ndid not answer')
            finally:
                thread_lock.release()
                send_to_all('rst')

        idx = 0

        new_winners = []

        for score in player_scores:
            if score >= max_points:
                running_main_thread = False
                new_winners.append(idx)
            idx+=1

        questions_finished = False

        if question_number == len(questions)-1:
            running_main_thread = False
            questions_finished = True
            send_to_all('prn'+'\nquestions finished')
            send_to_all('prn'+"\ndeclaring winner")
            
            player = 0
            max_score = 0
            for x in range(len(player_scores)):
                if player_scores[x]>max_score:
                    max_score = player_scores[x]
                    player = x
            winners = []
            for x in range(len(player_scores)):
                if max_score == player_scores[x]:
                    winners.append(x)
            time.sleep(0.5) 
            declare_winners(winners)
            time.sleep(1)
            send_to_all('kll')

        if running_main_thread:
            time.sleep(0.5)
            send_scores()
            question_number+=1
            buzzer = 'off'
            send_to_all('prn'+'\nget ready for next question')
            time.sleep(2)
        
        elif running_main_thread == False and questions_finished == False:
            send_to_all('prn'+'\nmax score has been reached ' + 'declaring winners' )
            declare_winners(new_winners)
            time.sleep(1)
            send_to_all('kll')

def welcome_new_user(client_socket,player_num):
    global client_sockets
    global client_addresses
    global player_scores

    player_scores.append(0)
    client_socket.send(('prn'+'your current score is 0').encode('ascii'))
 #   player_numbers.append(str(len(client_sockets)))
    while True:
        buzzer_handler(client_socket, player_num)

waitingmsg = 'Hey there!Thanks for joining us, We are waiting for the other players to join pls bear with us'
player_msg = 'you are player'

while True:

    client_socket, client_addr = server_socket.accept()
    client_sockets.append(client_socket)
    client_addresses.append(client_addr)
    player_num = len(client_sockets)
    client_socket.send(('prn'+player_msg+' '+str(player_num)).encode('ascii'))
    start_new_thread(welcome_new_user, (client_socket,player_num))
    time.sleep(1)
    print(f'new player connected with details {client_socket.getpeername()}')
    if len(client_sockets)!= 3:
        send_to_all('prn'+waitingmsg)
    else:
        break


print(player_scores)

time.sleep(10)

send_to_all('prn'+'All players are now connected, Game is about to begin')

time.sleep(2)

send_to_all('prn'+game_rules)

time.sleep(10)

send_to_all('prn'+'starting with questions')

time.sleep(1)

main_thread()
