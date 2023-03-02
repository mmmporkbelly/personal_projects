"""
Mimics a network server
Part of Mastering Python - Networking and Security Udemy Course
Seido Karasaki(yakitategohan on github)
v1 3/1/2023
"""
import socket

# Size of packet expected
size = 512
host = ''
port = 9898

# Instance of a socket, AF_INET indicates it's an internet family, SOCK_STREAM indicates TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to ip/port, allow up to 5 connections
sock.bind((host, port))
sock.listen(5)

# Save client connection and addr of remote end - c is client socket
c, addr = sock.accept()

# Again, expect up to 512
data = c.recv(size)

# If connection, append to file
if data:
    f = open("storage.date", "w")
    print(f'Connection from: {addr[0]}')
    # Write data, make sure to decode to UTF-8 since it will come as bytes
    f.write(f"{addr[0]}: {data.decode('utf-8')}")
    f.close()
sock.close()

