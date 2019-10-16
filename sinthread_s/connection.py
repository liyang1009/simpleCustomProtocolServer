import Queue
import collections
import select
from collections import deque
from event_loop import get_loop
from handler import Handler
from utils import _merge_prefix
BUFFER_SIZE = 4096
''' warpper the socket function  include support the read/write data buffer from the socket
'''
class Connection():
	def __init__(self,client_socket):
		self._read_buffer = collections.deque()
		self._read_buffer_size = 0
		self.socket = client_socket
		self.fd = client_socket.fileno()
		self.read_buffer = deque()
		self.write_buffer = Queue.Queue()
		self.header = None
	def begin(self):
		get_loop().addEvent(self.fd,select.EPOLLIN,self)
	def read(self):
		read_data = self.socket.recv(BUFFER_SIZE)
		if read_data <= 0:
			self.close()
			return 0
		#pdb.set_trace()
		self.read_buffer.append(read_data)
		self._read_buffer_size += len(read_data)
		#print(self._read_buffer_size)
		#here is execute the business logic
		get_loop().modifyEvent(self.socket,select.POLLOUT)
		handler = Handler(self)
		handler.execute()
		
	def read_from_buffer(self,size):
		return _merge_prefix(self.read_buffer,size)
			
	def write_to_buffer(self,buf):
		
		# write_data = self.write_package_handler(buf)
		#print(buf)
		self.write_buffer.put(buf)

	def handler_event(self,event):
		if event == select.POLLIN:
			self.read()
		elif event == select.POLLOUT:
			self.write_from_buffer()
		elif event==select.POLLERR:
			self.close()

			
	def write_from_buffer(self):
		get_loop().modifyEvent(self.socket,select.EPOLLIN)
		try:
			write_data = self.write_buffer.get_nowait()
		except Queue.Empty as e:
			pass	
		if write_data:
			try:
				write_status = self.socket.send(write_data)
				if write_status < 0:
					self.close()	
			except socket.error as e:
				self.close()

	def close(self):
		get_loop().delEvent(self.fd)
		self.socket.close()
		
