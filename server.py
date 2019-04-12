import socket
import struct
import threading

client_connections = [];

def server_start():	
	HOST, PORT = '', 8888
	listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	listen_socket.bind((HOST, PORT))
	listen_socket.listen(1024)
	print 'Serving Server on port %s ...' % PORT

	threading.threading(target = handler_writeable,client_connections )
	while True:
	    client_connection, client_address = listen_socket.accept()
	   	#client_connections.append(client_connection)
		task = threading.Thread(target=handler_connection, args=(client_connection,))
		task.start()

def broad_cast(data_type,data,client_connection):
	for conn in client_connections:
		if conn == client_connection:
			continue
		conn.sendall(create_packet(data_type,data))

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


def handler_connection(client_connection):
	read_data = [];
	try:
		client_connection.sendall(create_packet(1,"monitor"))
	except Exception as e:
		client_connection.close()
		return
	
	while True:
		request = client_connection.recv(8)
		if len(request) <= 0:
			break;
		val_type = struct.unpack('!i', request[:4])[0]
		val_len = struct.unpack('!i', request[4:8])[0]
		data =  client_connection.recv(val_len)
		if len(request) <= 0:
			break;
		if data.find("ping") > -1:
			data = "pong"
		
		try:
			handler_packet(client_connection,val_type,data)
		except Exception as e:
			break;
		#broad_cast(val_type,data,client_connection)
	client_connection.close()
	#client_connections.remove(client_connection)

def handler_packet(client_connection,val_type=1,data):
	client_connection.sendall(create_packet(val_type,data))


def handler_writeable():
	while True:
			conn = client_connections.pop():
			while packt = queue.pop:
				try:
					conn.sendall(packt)
				except Exception as e:
					conn.close()
					break
if __name__ == "__main__":
	server_start()
