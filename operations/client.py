# -*- coding: UTF-8 -*-
'''
Client for arithmetical operations
Take a file with mathematical expressions, one per line, send it to server in order to receive results.
Save and destination files are hardcoded for demonstration purposes 
'''

import socket
import logging
import timeit
import os
import sys

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 45454        # The port used by the server
BUFFER_SIZE = 8192
logging.basicConfig(level=logging.INFO)
from multiprocessing import Pipe


if __name__ == '__main__':
    """ After connecting to host, splits in two processes for sending and receiving file data.
    The two processes communicates with through a pipe, in case there is error in one of them.
    
    Default parameters
    >>> python client operations.txt results.txt
    """
    try:
        source = sys.argv[1]
    except IndexError:
        source = 'operations.txt'
    try:
        destination = sys.argv[2]
    except IndexError:
        destination = 'results.txt'
    except IOError as e:
        logging.error(e)
        sys.exit(1)
        
    tic=timeit.default_timer()
    s = socket.socket()
    s.connect((HOST, PORT))
    pipein, pipeout = Pipe()
    pid = os.fork()
    if not pid: # Subprocess sends data
        try:
            fin = open (source, "r")
        except Exception as e:
            pipein.send('error')
            logging.error(e)
            os._exit(1)
        pipein.send('ok')
        logging.info("Sending data from %s to the server", source)
        data = fin.read(BUFFER_SIZE)
        while (data):
            s.sendall(data)
            data = fin.read(BUFFER_SIZE)
        fin.close()
        logging.info("Finished sending file data")
    else: # Parent process receives results
        if pipeout.recv() == 'error': 
            os._exit(1) # Exits if there is an error in the other subprocess
        try:
            fout = open(destination,'w')
        except Exception as e:
            logging.error(e)
            os._exit(1)
        results = s.recv(BUFFER_SIZE)
        logging.info("Receiving file data")
        while (results):
            fout.write(results)
            results = s.recv(BUFFER_SIZE)
        logging.info("Receiving data finished. Saving in file %s", destination)
        fout.close()    
        toc=timeit.default_timer()
        dif = toc - tic
        logging.info("TOTAL EXECUTION TIME: %s", dif)
        
