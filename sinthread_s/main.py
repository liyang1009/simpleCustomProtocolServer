from server import server
from event_loop import  get_loop 

def main():
	ss = server()
	server_address = ("0.0.0.0",50000)
	ss.bind(server_address)
	get_loop().run_event_loop()

if __name__ == "__main__":
	main()
