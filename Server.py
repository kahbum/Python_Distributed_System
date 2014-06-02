import threading
from multiprocessing.connection import Listener
import os
import imp


process_directory = "process_files/"

class ClientModuleConnect(threading.Thread):
    id = None
    conn = None
    global process_directory
    process_file = None
    process_module = None

    def __init__(self, id, conn):
        if(not os.path.isdir(process_directory)):
            os.mkdir(process_directory)
        self.id = id
        self.conn = conn
        self.process_file = "proc_file"+repr(id)+".py"
        threading.Thread.__init__(self)
        print "connection accepted from " + repr(self.id)

    def __del__(self):
        os.remove(process_directory+self.process_file)
        os.remove(process_directory+self.process_file+"c")
        self.conn.close()
    
    """register a module sent by the client"""
    def register_module(self, content):
        f = open(process_directory+self.process_file, "wb")
        f.write(content)
        f.close()

        self.process_module = imp.load_source(self.process_file[:-3], process_directory+self.process_file)
        # print dir(self.process_module)

    """process a method previously sent in a module by the client"""
    def do_process(self, args):
        # if args[0] not in dir(self.process_module):
        #     self.conn.send("Metodo " + args[0] + " nao encontrado.")
        #     return
        try:
            self.conn.send(self.run_method(self.process_module, args[0], args[1:]))
        except Exception, e:
            self.conn.send(e)

    """execute a method from a module"""
    def run_method(self, module, method_name, args=None):

        method = getattr(module, method_name)

        # print method.__name__
        # print args
        # if len(args) < 1:
        #   return method()
        return method(*args)

    """main method to manage client requests"""
    def run(self):
        try:
            while True:

                args = self.conn.recv()

                if args[0] == 0:
                    self.register_module(args[1])
                elif args[0] == 1:
                    self.do_process(args[1:])

                # try:
                #   l = conn.recv_bytes(1024)
                #   while(l):
                #       f.write(l)
                #       l = conn.recv_bytes(1024)
                #   f.close()
                # except EOFError:
                #   pass

                # self.conn.close()
        except EOFError:
            print "connection closed from " + repr(self.id)
        except Exception, e:
            raise e

class Server():
    address = None

    def __init__(self, ip, port):
        self.address = (ip, port)     # family is deduced to be 'AF_INET'

    """start the server"""
    def start_serve(self):
        threads = []
        while True:
            listener = Listener(self.address)

            conn = listener.accept()

            process = ClientModuleConnect(listener.last_accepted, conn)
            process.start()
            
            listener.close()
        

if __name__ == '__main__':
    server = Server('localhost', 6000)
    server.start_serve()
