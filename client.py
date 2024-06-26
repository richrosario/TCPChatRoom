import socket
import threading

# Choosing Nickname
nickname = input("Choose a nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',55551))

# Listening to Server and Sending Nickname
def receive():
	while True:
		try:
			message = client.recv(1024).decode('ascii')
			if message == 'NICK':
				client.send(nickname.encode('ascii'))
			else:
				print(message)
		except:
			print("An error occured!")
			client.close()
			break

# Sending Messages To Server
def write():
	while True:
		message = f'{nickname}: {input("")}'
		client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()