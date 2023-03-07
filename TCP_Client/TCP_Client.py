#!/usr/bin/python
"""
A TCP Client using the socket module
Seido Karasaki(yakitategohan on github)
v1 3/6/2023
"""

import socket

# Make socket obj. AF_INET = IPv4, SOCK_STREAM = TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Change host IP and port if you want
host = socket.gethostname()
port = 1234

# Bind host to socket
client_socket.connect((host,port))

# Don't accept any more data than:
message = client_socket.recv(1024)
client_socket.close()

# Print msg
print(message.decode('ascii'))
