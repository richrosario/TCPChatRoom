import socket
import threading

#Our goal here is to create a simple TCP chat room

# Connection Data
host = '127.0.0.1' #local host
port = 55551

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port)) #Bind the server to the local host
server.listen()

# Lists For Clients and Their Nicknames
clients = []  
nicknames = [] 

# Sending Messages To All Connected Clients
def broadcast(message):
	for client in clients:
		client.send(message)

# Handling Messages From Clients
def handle(client):
	while True:
		try: #try to recieve a message from the client, and then broadcast it to all clients
			message = client.recv(1024)
			broadcast(message)
		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()
			nickname = nicknames[index]
			broadcast(f'{nickname} left the chat!'.encode(ascii))
			nicknames.rmeove(nickname)
			break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")
receive()