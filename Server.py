import threading
from multiprocessing.connection import Listener
import os
import imp
import sys
import types

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
    
    def register_module(self, content):
        """register a module sent by the client"""
        f = open(process_directory+self.process_file, "wb")
        f.write(content)
        f.close()

        self.process_module = imp.load_source(self.process_file[:-3], process_directory+self.process_file)

    def do_process(self, args):
        """process a method previously sent in a module by the client"""
        try:
            self.conn.send(self.run_method(self.process_module, args[0], args[1:]))
        except Exception, e:
            self.conn.send(e)

    def run_method(self, module, method_name, args=None):
        """execute a method from a module"""
        method = getattr(module, method_name)

        return method(*args)

    def run(self):
        """main method to manage client requests"""
        try:
            while True:

                args = self.conn.recv()

                if args[0] == 0:
                    self.register_module(args[1])
                elif args[0] == 1:
                    self.do_process(args[1:])

        except EOFError:
            print "connection closed from " + repr(self.id)
        except Exception, e:
            raise e

class Server():
    address = None
    threads = []

    def __init__(self, ip = 'localhost', port = 7000):
        self.address = (ip, port)

    def start_serve(self):
        """start the server"""
        while True:
            listener = Listener(self.address)

            conn = listener.accept()

            process = ClientModuleConnect(listener.last_accepted, conn)
            process.start()
            
            listener.close()
        

if __name__ == '__main__':
    ip = 'localhost'
    port = 7000
    if len(sys.argv) == 2:
        ip = sys.argv[1]
    elif len(sys.argv) == 3 and sys.argv[2].isdigit():
        ip = sys.argv[1]
        port = int(sys.argv[2])
    elif len(sys.argv) > 3:
        print "Invalid arguments."
        exit()
    server = Server(ip, port)
    server.start_serve()