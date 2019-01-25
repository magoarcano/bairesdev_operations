# -*- coding: UTF-8 -*-
'''
Created on 24/1/2019

@author: arcano
'''
import socket
import logging

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 45454        # Port to listen on (non-privileged ports are > 1023)

def operate(operation):
    """ Compute arithmetic operation.
        Allowed operators: *, /, +, -
    
    :param operation: an string with simple arithmetical operation
    :returns: integer result
    
    TODO: Change temporal eval function for a safer method
    """
    try: 
        return str(eval(operation))
    except:
        return "INVALID"

if __name__ == '__main__':
    """
    Server. Writes results temporarily in file.
    TODO: Fix for files larger than buffer size
    """
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))
    server_socket.listen(10) # Acept until 10 incoming connections. Parameter optional in Python 3
    
    last =  ''
    while True: # Doesn't finish after one client
        client_socket, address = server_socket.accept()
        
        # Get and write results in another file
        data = client_socket.recv(8192)
        while (data):
            results = []
            print last
            logging.info("data: %s" % data)
            
            operations = data.split("\n")
            operations[0] = last + operations[0] # concatenates with last operations of previous segment
            
            last = operations.pop()
            
            for op in operations:
                if op:
                    result = operate(op) + "\n"
                    results.append(result)
            logging.info("results: %s" % results)
            client_socket.sendall("".join(results))
            data = client_socket.recv(8192)
        client_socket.close()
    
    server_socket.close()
    