import socket
import thread

class P2P_file_share():
	def __init__(self):
		self.serverSoc = None
		self.serverStatus = 0
		self.buffsize = 1024
		self.allClients = {}
		self.counter = 0

	def handleSetServer(self):
		if self.serverSoc != None:
			self.serverSoc.close()
			self.serverSoc = None
			self.serverStatus = 0
			print('insi')

		server_ip = raw_input('Server IP\n')
		server_port = int(raw_input('Server Port\n'))
		serveraddr = (server_ip,server_port)
		print(serveraddr)
		try:
			self.serverSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.serverSoc.bind(serveraddr)
			self.serverSoc.listen(5)
			print("Server listening on %s:%s" % serveraddr)
			thread.start_new_thread(self.listenClients,())
			self.serverStatus = 1
			self.name = ''
			if self.name == '':
				self.name = "%s:%s" % serveraddr
		except:
			print("Error setting up server")

	def listenClients(self):
		while 1:
			print('in')
			clientsoc, clientaddr = self.serverSoc.accept()
			print("Client connected from %s:%s" % clientaddr)
			self.addClient(clientsoc, clientaddr)
			thread.start_new_thread(self.handleClientMessages, (clientsoc, clientaddr))
		self.serverSoc.close()

	def handleAddClient(self):
		if self.serverStatus == 0:
			print("Set server address first")
			return

		client_ip = raw_input('Client IP\n')
		client_port = int(raw_input('Client Port\n'))
		clientaddr = (client_ip,client_port)
		try:
		    clientsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		    clientsoc.connect(clientaddr)
		    print("Connected to client on %s:%s" % clientaddr)
		    self.addClient(clientsoc, clientaddr)
		    thread.start_new_thread(self.handleClientMessages, (clientsoc, clientaddr))
		except:
		    print("Error connecting to client")

	def handleClientMessages(self, clientsoc, clientaddr):
		while 1:
			try:
				filename = open('fil','w')
				data = clientsoc.recv(self.buffsize)

				while True:
					filename.write(data)
					data = clientsoc.recv(self.buffsize)
					if not data: break
				filename.close()
			except:
				break
		self.removeClient(clientsoc, clientaddr)
		clientsoc.close()
		print("Client disconnected from %s:%s" % clientaddr)

	def handleSendChat(self):
		if self.serverStatus == 0:
			print("Set server address first")
			return
		for client in self.allClients.keys():
			filename = raw_input('Enter Filename\n')
			fil = open(filename)
			dat = fil.read(self.buffsize)
			while dat:
				client.send(dat)
				dat = fil.read(self.buffsize)
			client.close

	def addClient(self, clientsoc, clientaddr):
		self.allClients[clientsoc]=self.counter
		self.counter += 1


	def removeClient(self, clientsoc, clientaddr):
		print self.allClients
		del self.allClients[clientsoc]
		print self.allClients

def main():  
	start=P2P_file_share()

	while 1:
		print('Menu')
		print('1. Server')
		print('2. Client')
		print('3. Make Transaction')

		num = int(raw_input('Selection\n'))

		if num == 1:
			start.handleSetServer()
		elif num == 2:
			start.handleAddClient()
		elif num == 3:
			start.handleSendChat()
		else:
			print('Input error')
	
if __name__ == '__main__':
	main()  
