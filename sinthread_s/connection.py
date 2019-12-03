#!/usr/bin/python
import Queue
import collections
import select
import pdb
import time
from collections import deque
from event_loop import get_loop
from handler import Handler
from utils import merge_prefix
from periodic_thread import *

BUFFER_SIZE = 4096
PING_TIMOUT_STEP  = 20

class Connection():
	'''the client warpper include socket all kinds of buffer and periodc ping'''
	def __init__(self,client_socket):
		self._read_buffer = collections.deque()
		self._read_buffer_size = 0
		self.socket = client_socket
		self.fd = client_socket.fileno()
		self.read_buffer = deque()
		self.write_buffer = Queue.Queue()
		self.header = None
		self.period = None
		self.last_active_time  = None

	def begin(self):
		get_loop().addEvent(self.fd,select.EPOLLIN,self)
		self.ping_timer()

	def read(self):
		read_data = self.socket.recv(BUFFER_SIZE)
		if read_data <= 0:
			self.close()
			return 0
		self.read_buffer.append(read_data)
		self._read_buffer_size += len(read_data)
		self.last_active_time = time.time()
		#here is the place where execute the business logic
		handler = Handler(self)
		handler.execute()

	def ping_timer(self):
		self.period = PeriodicThread(self.ping,PING_TIMOUT_STEP)	
		self.period.start()

	def ping(self):
		h = Handler(self)
		h.ping()

	def read_from_buffer(self,size):
		return merge_prefix(self.read_buffer,size)
			
	def write_to_buffer(self,buf):
		try:
			get_loop().modifyEvent(self.socket,select.POLLOUT)
			self.write_buffer.put(buf)
		except Exception as e:
			self.close()

	def handler_event(self,event):
		if event == select.POLLIN:
			self.read()
		elif event == select.POLLOUT:
			self.write_from_buffer()
		elif event==select.POLLERR:
			self.close()
		else:
			print(event)
			self.close()

	def write_from_buffer(self):
		get_loop().modifyEvent(self.socket,select.EPOLLIN)
		write_data = None
		try:
			write_data = self.write_buffer.get_nowait()
		except Queue.Empty as e:
			pass	
		if write_data:
			try:
				self.socket.sendall(write_data)
			except Exception as e:
				self.close()

	def close(self):
		get_loop().delEvent(self.fd)
		self.socket.close()
		self.period.cancel()
		print("the socket is close")
		
