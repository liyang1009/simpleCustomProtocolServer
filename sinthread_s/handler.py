import time
from protocol import protocol
from event_loop import get_loop
class Handler():

	def __init__(self,conn):
		self.protocol = protocol(conn)

	def execute(self):
		'''this function operate the business logic'''
		data  = self.protocol.get_data()
		if data is not None and "hello" in data:
			write_data = "egg"	
			get_loop().server.prodcast(1,write_data)
		else:
			self.protocol.set_data(1,"hello icezhou")
	
	def ping(self):
			'''ping for connection alive'''
			print("the period is running")
			current_time = time.time()
			print(current_time,self.protocol.conn.last_active_time)
			if current_time - self.protocol.conn.last_active_time > 120:
				print("pong timeout")
				self.protocol.conn.close()
			self.protocol.set_data(2,"ping")

