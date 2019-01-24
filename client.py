# -*- coding: UTF-8 -*-
'''
Created on 24/1/2019

@author: arcano
'''

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 45454        # The port used by the server

if __name__ == '__main__':
    s = socket.socket()
    s.connect((HOST, PORT))
    f = open ("head.txt", "r") # head.txt small temporary file for development
    l = f.read(1024)
    while (l):
        s.send(l)
        l = f.read(1024)
    s.close()
    
