from event_loop import  get_loop 
from server import server

def main():
	ss = server()
	server_address = ("",50000)
	ss.bind(server_address)
	get_loop().start_server(ss)

if __name__ == "__main__":
	main()
