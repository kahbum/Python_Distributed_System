Pytho_Distributed_System
========================

Basic server and client for a distributed system made in Python

To start using just follow the steps ahead:

    1 - Start a Server passing an IP and a Port as argument. Eg.: python Server 127.0.0.1 7000.
    2 - Create a ConnectClient object on your client application, using the Server IP and Port as constructor parameters.
    3 - Now you have to send to the server a Python file with the functions/methods you will use. To do this, use the method 'register_module' using your ConnectClient object. Note: At the moment, the file must contain only functions.
    4 - Finally, to use a function/method, call the method 'request_process' using your ConnectClient object. The only parameter is a list that must contain, as first item, a string with the name of the function to be used. The other itens of the list are the function parameters.

Note:

    1 - The 'request_process' method will return an object of the same return type of your function/method.
    2 - If any called function raises an exception, the exception will be raised to your client application, as if it was running on your computer.

For some examples of use, see 'example_application.py' and the 'test_functions.py' files.
