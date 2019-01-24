# -*- coding: UTF-8 -*-
'''
Created on 24/1/2019

@author: arcano
'''
import socket
from contextlib import closing
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
    return eval(operation)

class Server(object):
    def run(self):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind((HOST, PORT))
            s.listen(10) # Optional parameter in Python 3
            conn, addr = s.accept()
            with closing(conn):
                logging.info('Connected by %s, %s' % addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(str(operate(data)))
            

if __name__ == '__main__':
    """
    Server. By the moment return result of one operation
    """
    my_server = Server()
    my_server.run()
    
    