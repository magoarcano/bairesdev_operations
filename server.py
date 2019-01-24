# -*- coding: UTF-8 -*-
'''
Created on 24/1/2019

@author: arcano
'''
import socket
from contextlib import closing
import logging
import sys

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 45454        # Port to listen on (non-privileged ports are > 1023)

def operate(operation):
    """ Compute arithmetic operation.
        Allowed operators: *, /, +, -
    
    :param operation: an string with simple arithmetical operation
    :returns: integer result
    
    TODO: Change temporal eval function for a safer method
    """
    print operation
    logging.info(operation)
    return str(eval(operation))


if __name__ == '__main__':
    """
    Server. Writes results temporarily in file.
    TODO: Fix for files larger than buffer size
    """
    
    server_socket = socket.socket()
    server_socket.bind((HOST,PORT))
    server_socket.listen(10) # Acept until 10 incoming connections. Parameter optional in Python 3
    i=1
    while True: # Doesn't finish after one client
        conn, address = server_socket.accept()
        
        f = open('results'+ str(i)+".txt",'w')
        i=i+1
        # Get and write results in another file
        l = conn.recv(1024)
        while (l):
            logging.info(l)
            for op in l.split("\n"):
                if op:
                    f.write(operate(op) + "\n")
            l = conn.recv(1024)
        f.close()
    
    
        conn.close()
    server_socket.close()
    