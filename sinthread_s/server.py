import socket
import select
import pdb
from connection import Connection
from protocol import protocol
from event_loop import  get_loop 


__CATA_LOG_SIZE = 1024
class server():
	'''the server for accept the new endpoint and have all connections'''
	def __init__(self,handler_map = None):
		self.connections = {}
		self.handler_map = handler_map
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def bind(self,server_address):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setblocking(0)
		self.socket.bind(server_address)
		self.socket.listen(__CATA_LOG_SIZE)
		get_loop().addEvent(self.socket.fileno(),select.EPOLLIN,self)

	def accept(self):	
		conn_socket,client_address = self.socket.accept() 	
		conn_socket.setblocking(0)
		client = Connection(conn_socket)
		self.connections[client.fd] = client
		client.begin()

	def handler_event(self,event):
		self.accept()
	
	def prodcast(self,msg_type,message):
		#pdb.set_trace()
		for fd in self.connections:
			conn = self.connections[fd]
			proto = protocol(conn)
			proto.set_data(msg_type,message)
			
		
	def remove_fd(self,fd):
		if fd in self.connections:
			del self.connections[fd]



