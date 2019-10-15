import socket
import select
from connection import connection
from event_loop import get_loop

class server():
	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def bind(self,server_address):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setblocking(0)
		self.socket.bind(server_address)
		self.socket.listen(1024)
		get_loop().addEvent(self.socket.fileno(),select.EPOLLIN,self)

	def accept(self):	
		conn_socket,client_address = self.socket.accept() 	
		conn_socket.setblocking(0)
		client = connection(conn_socket)
		client.begin()

	def handler_event(self,event):
		self.accept()


