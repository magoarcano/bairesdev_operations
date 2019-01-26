# -*- coding: UTF-8 -*-
'''
Created on 24/1/2019

@author: arcano
'''

import socket
import logging

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 45454        # The port used by the server
BUFFER_SIZE = 8192

if __name__ == '__main__':
    s = socket.socket()
    s.connect((HOST, PORT))
    fin = open ("head.txt", "r") # head.txt small temporary file for development
    data = fin.read(BUFFER_SIZE)
    while (data):
        s.send(data)
        data = fin.read(BUFFER_SIZE)
        
    fout = open('results.txt','w')
    
    results = s.recv(BUFFER_SIZE)
    while (results):
#         logging.info("Results: %s" % results)
        fout.write(results)
        print results
        print "-------"
#         if len(results) < BUFFER_SIZE:
#             break
        results = s.recv(BUFFER_SIZE)
    logging.info("Saving in file results.txt")
    fout.close()    
    s.close()
    
