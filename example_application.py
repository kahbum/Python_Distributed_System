from Client import *

if __name__ == '__main__':

    client = ConnectClient('localhost', 7000)

    client.register_module("test_functions.py")

    print "cube 3 >> " + repr(client.request_process(['cube', 3]))
    print "quad 7 >> " + repr(client.request_process(['quad', 7]))
    print "test2 >> " + repr(client.request_process(['test2']))
    print "ten_times 7 >> " + repr(client.request_process(['ten_times', 7]))
    print "mult 7 8 >> " + repr(client.request_process(['mult', 7, 8]))
    print "test1 >> " + repr(client.request_process(['test1', ]))
    print "hello >> " + repr(client.request_process(['hello', 'world']))
    print "cube 4 >> " + repr(client.request_process(['cube', 4]))
    print "cube 5 >> " + repr(client.request_process(['cube', 5]))
    print "cube 6 >> " + repr(client.request_process(['cube', 6]))