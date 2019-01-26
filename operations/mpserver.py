# -*- coding: UTF-8 -*-
'''
Created on 26/1/2019

@author: arcano

Implements server with multiprocessing Process
'''

import socket
import os
from sympy import S
from multiprocessing import Pipe, Process, cpu_count

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 45454        # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 8192
PROCESSORS = cpu_count()


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

def child(operations, conn):
    """ Compute a group of arithmetic operations
    """
    result_list = [operate(op) for op in operations if op != '' ]
    msg = "".join(result_list)
#     msg = msg.encode()
    conn.send(msg)
    conn.close()

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))
    server_socket.listen(10) # Accept until 10 incoming connections. Parameter optional in Python 3
    children = []
#     while True:
    client_socket, address = server_socket.accept()
    last =  ''
    data = client_socket.recv(BUFFER_SIZE)
    while (data):
        operations = data.split("\n") # Better than splitlines to detect cropped operations
        operations[0] = last + operations[0] # concatenates with last operations of previous segment
        last = operations.pop()
    
        parent_conn, child_conn = Pipe()
        p = Process(target=child, args=(operations, child_conn) )
        children.append({p.pid: [parent_conn, child_conn]})
        p.start()
        results = parent_conn.recv()
        p.join()
        client_socket.sendall(results)
        if len(data) < BUFFER_SIZE:
            break
        data = client_socket.recv(BUFFER_SIZE)
    client_socket.close()
    #endwhile
    server_socket.close()

