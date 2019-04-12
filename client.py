import struct
import socket
def create_packet(data_type,data):
        sended_data = []
        data_len = len(data)
        val_len = struct.pack('!i', data_len)
        val_type = struct.pack('!i',data_type)
        sended_data.append(val_type)
        sended_data.append(val_len)
        sended_data.append(data)
        print sended_data
        return ''.join(sended_data)

def client_start():
	HOST = '192.168.3.40'    # The remote host
	PORT = 8888              # The same port as used by the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	while True:
		data = s.recv(8)
		if len(data) <=0:
			break
		val_type = struct.unpack('!i', data[:4])[0]
		val_num = struct.unpack('!i', data[4:8])[0]
		print val_num;
		val = s.recv(val_num)
		if len(val) <=0:
			break
		print val
		input_data = input("<<")
		s.sendall(create_packet(1,input_data))
	s.close()
client_start()
