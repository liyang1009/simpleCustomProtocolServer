import struct

'''parse the data conform the protocol specification
type:length:value '''

HEADER_SIZE = 8
class protocol:
	def __init__(self,conn):
		self.conn = conn	
	def get_data(self):
		if not self.conn.header:
			self.conn.header = self.conn.read_from_buffer(HEADER_SIZE)
			if self.conn.header:
				data_type = struct.unpack('!i', self.conn.header[:4])[0]
				data_len = struct.unpack('!i', self.conn.header[4:8])[0]
				data = self.conn.read_from_buffer(data_len)
				if data:
					self.conn.header = None 
					return data
			
	def set_data(self,data_type,data):
		sended_data = []
		data_len = len(data)
		val_len = struct.pack('!i', data_len)
		val_type = struct.pack('!i',data_type)
		sended_data.append(val_type)
		sended_data.append(val_len)
		sended_data.append(data)
		self.conn.write_to_buffer(''.join(sended_data))
		#parse the protocol and the return the data to the channel
		
		

