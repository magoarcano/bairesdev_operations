# -*- coding: UTF-8 -*-
'''
Created on 24/1/2019

@author: arcano
'''

import socket
import logging
import os
from sympy import S

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 45454        # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 8192


def operate(operation):
    """ Compute arithmetic operation.
    :param operation: an string with simple arithmetical operation
    :returns: integer result
    """
    try:
        s = S(operation)
        return str(int(s.evalf())) + "\n"
    except:
        return "INVALID EXPRESSION"

def child(pipeout, operations):
    """ Compute a group of arithmetic operations """
    result_list = [operate(op) for op in operations if op != '' ]
    msg = "".join(result_list)
    msg = msg.encode()
    os.write(pipeout, msg)

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))
    server_socket.listen(10) # Acept until 10 incoming connections. Parameter optional in Python 3
    
    while True:
        client_socket, address = server_socket.accept()
        last =  ''
        data = client_socket.recv(BUFFER_SIZE)
        
        while (data):
            print last
            logging.info("data: %s" % data)
            
            operations = data.split("\n")
            operations[0] = last + operations[0] # concatenates with last operations of previous segment
            last = operations.pop()
            
            pipein, pipeout = os.pipe()
            if os.fork() == 0:
                child(pipeout, operations)
            else:
                results = os.read(pipein, BUFFER_SIZE)
            
                logging.info("results: %s" % results)
                client_socket.sendall(results)
            data = client_socket.recv(BUFFER_SIZE)
        client_socket.close()
    
    server_socket.close()
    