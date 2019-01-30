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

logging.basicConfig(filename='server.log', level=logging.DEBUG)

class OperationProcess(Process):
    """ Implementation of subprocess in charge of solving the mathematical expressions
    """
    def __init__(self, operations, conn):
        """
        :param operations: list of arithmetic expressions to calculate
        :param conn: pipe connection
        """
        super(OperationProcess, self).__init__()
        self.operations = operations
        self.conn = conn
        
    def run(self):
        """ Evaluates each operation and return results through the pipe
        """
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
            # First solve * and /
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
            # Solve + and -
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
            return "%d\n" % result
        except:
            logging.warning("Invalid line: %s", expression)
            return "INVALID\n"
                 

def server_process(client_socket):
    """ Gets data from socket, fixes truncated operations and send that batch of
    operations to a new OperationProcess.
    Receives results in order from the pool. As soon does it, creates the next subprocess.
    Subprocesses are managed in a fixed size array, equal to number of CPUs in the system
    """
    
    logging.info("Number of processors: %d", PROCESSORS)
    children = [None] * PROCESSORS # Fixed pool of processes with their pipes.
    last =  '' # Auxiliar for fixing truncated operations
    i = 0
    data = client_socket.recv(BUFFER_SIZE) # first batch of data
    while (data):
        i = i % PROCESSORS # counter moves cyclic along subprocesses
        process = children[i]
        if process: # If there is already a process working in the array
            p, parent_conn, child_conn = process # Get process and related pipe
            results = parent_conn.recv() # waits and get results
            p.join() # Kill subprocess
            client_socket.sendall(results) # Send data to sockets
            # close pipes
            parent_conn.close()
            child_conn.close()
            children[i] = None # Room available
        
        operations = data.split("\n") # This is Better than splitlines to detect truncated operations
        # Fix truncated operations prefixing with last one of previous batch
        operations[0] = last + operations[0]
        last = operations.pop()
        
        # New process is created only when there is room available in children
        parent_conn, child_conn = Pipe() # creates pipe for subprocess
        p = OperationProcess(operations, child_conn) # creates subprocess
        children[i] = [p, parent_conn, child_conn] # Put subprocess in array.
        p.start()
        i += 1
        if len(data) < BUFFER_SIZE:
            break
        data = client_socket.recv(BUFFER_SIZE)
    # Continue sending data from remaining subprocesses    
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
    while True:
        client_socket, address = server_socket.accept()
        server_process(client_socket)
    server_socket.close()
    

