#IMPORT LIBRARIES
import socket
import select
import sys
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
	print('Correct usage: script, IP address, port number\nExample: python3 server.py 192.168.0.1 8080')
	exit()

IP_address = str(sys.argv[1])   #IP adress
Port = int(sys.argv[2])         #port number

server.bind((IP_address, Port)) #bind server to IP adress and port
server.listen(100)              #listen to 100 active connections
list_of_clients = []            #list of clients connected
message_count = 1               #message count of responses (true|false)
error_flag = False              #activates if a response from a client is 'false'

#Creates a thread for each client connected
def clientthread(conn, addr):
	conn.sendall(b'Welcome to [EDD]Blockchain Project!') #Send Welcome message when connected
	global message_count       #import global variable message_count
	global error_flag          #import global variable error_flag

	while True:
			try:
				message = conn.recv(2048)  #receive message
				if message:
					if message.decode('utf-8') != 'true' and message.decode('utf-8') != 'false': #If message is a JSON
						print ('Received: '+message.decode('utf-8'))          #print message received
						message_to_send =message.decode('utf-8')              #prepare to broadcast
						message_count = 1                                     #start approve count on 1
						broadcast(message_to_send, conn)                      #broadcast to everybody but the sender
					else:                                                     #if message is not a JSON (true|false)
						new_message = message.decode('utf-8')
						if new_message == 'false':                            #if one client returns false, json is not good
							error_flag = True
						message_count += 1                                    #always updates number of responses received
						if message_count == len(list_of_clients):             #once every client has answered
							if error_flag == False:                           #if clients agree
								message_to_broadcast = 'true'                 #reply true to everybody
								broadcast_to_all(message_to_broadcast,conn)   #broadcast message to all
							else:                                             #if clients don't agree
								message_to_broadcast = 'false'                #reply false to everybody
								error_flag = False                            #reset error flag
								broadcast_to_all(message_to_broadcast,conn)   #broadcast message to all
							message_count = 1                                 #reset message count
				else:
					remove(conn)

			except:
				continue

#BROADCAST TO ALL CLIENTS
def broadcast_to_all(message, connection):
	for clients in list_of_clients:
		try:
			clients.sendall(message.encode('utf-8'))
		except:
			clients.close()
			remove(clients)

#BROADCAST TO ALL CLIENTS EXCEPT FOR THE SENDER
def broadcast(message, connection):
	for clients in list_of_clients:
		if clients!=connection:
			try:
				clients.sendall(message.encode('utf-8'))
			except:
				clients.close()
				remove(clients)

#REMOVE client
def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)


while True:
	conn, addr = server.accept()   #ACCEPTS CONNECTIONS
	list_of_clients.append(conn)   #KEEPS LIST OF CLIENTS UPDATED
	print (addr[0] + " connected") #PRINTS USER CONNECTED
	start_new_thread(clientthread,(conn,addr)) #CREATES INDIVIDUAL THREAD FOR EVERY CLIENT CONNECTED

conn.close()
server.close()