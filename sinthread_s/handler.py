from protocol import protocol
'''this class process the data by protocol parse main purpose can be inherit 
so can process diffent logic
'''
class Handler():
	def __init__(self,conn):
		self.protocol = protocol(conn)
	def execute(self):
		data = self.protocol.get_data()
		print(data)
		self.protocol.set_data(1,"hello icezhou")
	
