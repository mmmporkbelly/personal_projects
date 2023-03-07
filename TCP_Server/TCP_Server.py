"""
A TCP Server using the socket module
Seido Karasaki(yakitategohan on github)
v1 3/6/2023
"""

import socket

# Make socket obj. AF_INET = IPv4, SOCK_STREAM = TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get hostname
host = socket.gethostname()
port = 1234

# Bind host to socket
server_socket.bind((host,port))

# Specify how many connections you allow
server_socket.listen(5)

while True:
    clientsocket, address = server_socket.accept()
    print(f'Received connection from {str(address)}')
    message = 'Thank you for connecting to the server\r\n'

    #Send message
    clientsocket.send(message.encode('ascii'))

    # Close connection
    clientsocket.close()
