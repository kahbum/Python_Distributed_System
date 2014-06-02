from multiprocessing.connection import Client

class ConnectClient():
	address = None
	conn = None
	
	def __init__(self, ip, port):
		self.address = (ip, port)
		self.conn = Client(self.address)

	def __del__(self):
		self.conn.close()
	
	"""send and register a module in the server"""
	def register_module(self, process_file):
		f = open(process_file, "rb")
		l = f.read()
		self.conn.send([0, l])
		f.close()

	"""request the server to do a process previously sent in a module"""
	def request_process(self, args):
		self.conn.send([1, args[0]] + args[1:])
		answer = self.conn.recv()
		if isinstance(answer, Exception):
			raise answer
		return answer
 
