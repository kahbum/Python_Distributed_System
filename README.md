Pytho_Distributed_System
========================

Basic server and client for a distributed system made in Python

To start using just follow the steps ahead:

    1 - Start a Server setting an IP and Port on Server.py __main__.
    2 - Create a ConnectClient object on your client application, using the Server IP and Port as constructor parameters.
    3 - Now you have to send to the server a Python file with the functions/methods you will use. To do this use the method register_module from the ConnectClient class. Note: At the moment, the function must contain only functions.
    4 - Finally, to use a function/method, use the method 'request_process' from ConnectClient . The only parameter is a list that must contain, as first item, a string with the name of the function to be used. The other itens of the list are the function parameters.
