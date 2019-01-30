# -*- coding: UTF-8 -*-
'''
Client for arithmetical operations
Take a file with mathematical expressions, one per line, send it to server in order to receive results.
Save response in a file
'''

import socket
import logging
import timeit
import os

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 45454        # The port used by the server
BUFFER_SIZE = 8192


if __name__ == '__main__':
    tic=timeit.default_timer()
    s = socket.socket()
    s.connect((HOST, PORT))
    
    pid = os.fork()
    if not pid: # Subprocess sends data
        fin = open ("operations.txt", "r") # head.txt small temporary file for development
        data = fin.read(BUFFER_SIZE)
        while (data):
            s.sendall(data)
            data = fin.read(BUFFER_SIZE)
        fin.close()
    else: # Parent process receives results
        fout = open('results.txt','w')
        results = s.recv(BUFFER_SIZE)
        while (results):
            fout.write(results)
            results = s.recv(BUFFER_SIZE)
        logging.info("Saving in file results.txt")
        fout.close()    
        toc=timeit.default_timer()
        dif = toc - tic
        logging.info("TIEMPO: " + str(dif))
        
