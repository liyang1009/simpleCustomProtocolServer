import select

class EventLoop():

	def __init__(self):
		self.poll = select.epoll()
		self.event_handler = {}
	def addEvent(self,fd,event,handler):
		self.poll.register(fd,event)
		self.event_handler[fd] = handler
		
	def delEvent(self,fd):
		self.server.remove_fd(fd)
		self.poll.unregister(fd)

	#run the event hanler indefinite	
	def run_event_loop(self):
		while True:
			for fileno,event in self.poll.poll():
				handler = self.event_handler[fileno]
				if handler:
					handler.handler_event(event)
	
	def modifyEvent(self,fd,event):
		self.poll.modify(fd,event)
	
	def start_server(self,server):
		self.server = server 
		self.run_event_loop()
		
eventloop = EventLoop()	
def get_loop():
	global eventloop
	return eventloop	
