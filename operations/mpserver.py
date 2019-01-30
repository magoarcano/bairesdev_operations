# -*- coding: UTF-8 -*-
'''
Implementation of multiprocesses server.
Receives data from clent using sockets. Returns result of operations of that data.
'''


from multiprocessing import Pipe, Process, cpu_count
import socket
import logging

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
        result_list = [self._operate(op) for op in self.operations if op != '' ]
        msg = "".join(result_list)
        self.conn.send(msg)
        self.conn.close()
        
    @staticmethod
    def _operate(expression):
        """ Fast evaluation of simple arithmetic expression.
        :param expression: an string with simple arithmetical operation
        :returns: truncated integer result or "INVALID" for empty or not well defined expressions
        """
        onlysumrest = []
        operator = ""
        try:
            # First resolve * and /
            for factor in expression.split():
                if operator == '/':
                    onlysumrest[-1] = float(onlysumrest[-1]) / float(factor)
                    operator = ''
                elif operator == '*':
                    onlysumrest[-1] = float(onlysumrest[-1]) * float(factor)
                    operator = ''
                elif factor in ('/', '*'):
                    operator = factor
                else:
                    onlysumrest.append(factor)
            # Resolve + and -
            result = float(onlysumrest[0])
            for factor in onlysumrest:
                if operator == '+':
                    result += float(factor)
                    operator = ''
                elif operator == '-':
                    result -= float(factor)
                    operator = ''
                elif factor in ('+', '-'):
                    operator = factor
            return str(int(result)) + "\n"
        except:
            logging.warning("Invalid line: %s" % "".join(expression))
            return "INVALID\n"
                 

def server_process(client_socket):
    last =  ''
    i = 0
    data = client_socket.recv(BUFFER_SIZE)
    while (data):
        i = i % PROCESSORS
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
        if len(data) < BUFFER_SIZE:
            break
        data = client_socket.recv(BUFFER_SIZE)
    # continue sending remaining data from children    
    empty = [None] * PROCESSORS
    while children != empty:
        i = i % PROCESSORS 
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

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))
    server_socket.listen(10) # Accept until 10 incoming connections. Parameter is optional in Python 3
    children = [None] * PROCESSORS
#     while True:
    client_socket, address = server_socket.accept()
    server_process(client_socket)
    
    server_socket.close()
    #endwhile
    

