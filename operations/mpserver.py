# -*- coding: UTF-8 -*-
'''
Created on 26/1/2019

@author: arcano

Implements server with multiprocessing Process
'''

import socket
from sympy import S
from multiprocessing import Pipe, Process, cpu_count

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 45454        # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 8192
PROCESSORS = cpu_count()

class OperationProcess(Process):
    def __init__(self, operations, conn, segment):
        """
        :param operations: list of arithmetic operations
        :param conn: pipe connection
        """
        super(OperationProcess, self).__init__()
        self.operations = operations
        self.conn = conn
        self.segment = segment
        
    def run(self):
        result_list = [self.operate(op) for op in operations if op != '' ]
        msg = "".join(result_list)
        self.conn.send(msg)
        self.conn.close()
        
    @staticmethod
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


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))
    server_socket.listen(10) # Accept until 10 incoming connections. Parameter optional in Python 3
    children = [None] * PROCESSORS
#     while True:
    client_socket, address = server_socket.accept()
    last =  ''
    data = client_socket.recv(BUFFER_SIZE)
    
    i = 0
    while (data):
        """
        TODO: START PRIMERO TODOS JUNTOS
        LUEGO JOINS DE A UNO. QUIZA AL RECIBIR INFO DESDE LAS PIPES 
        """
        i = i % PROCESSORS # 
        process = children[i]
        if process:
            p, parent_conn, child_conn = process
            results = parent_conn.recv()
            p.join()
            client_socket.sendall(results)
            # close pipes
            parent_conn.close()
            child_conn.close()
            children[i] = None
        
        operations = data.split("\n") # Better than splitlines to detect cropped operations
        operations[0] = last + operations[0] # concatenates with last operations of previous segment
        last = operations.pop()
        
        parent_conn, child_conn = Pipe()
        p = OperationProcess(operations, child_conn, i)
        children[i] = [p, parent_conn, child_conn]
        p.start()
        i += 1
        if len(data) < BUFFER_SIZE:# and children == [None] * PROCESSORS:
            break
        data = client_socket.recv(BUFFER_SIZE)
        
    empty = [None] * PROCESSORS
    while children != empty:
        i = i % PROCESSORS # 
        process = children[i]
        if process:
            p, parent_conn, child_conn = process
            results = parent_conn.recv()
            p.join()
            client_socket.sendall(results)
            # close pipes
            parent_conn.close()
            child_conn.close()
            children[i] = None
        i += 1
    
    client_socket.close()
    server_socket.close()
    #endwhile
    

