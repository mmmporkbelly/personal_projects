"""
Mimics a network client
Part of Mastering Python - Networking and Security Udemy Course
Seido Karasaki(yakitategohan on github)
v1 3/1/2023
"""
import socket

host = 'localhost'

# Instance of a socket, AF_INET indicates it's an internet family, SOCK_STREAM indicates TCP)
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to localhost on port 5555
addr = (host, 5555)
mysock.connect(addr)

# Now can send messages
try:
    # Make sure message is bytestring
    msg = b"Hi this is a test\n"
    mysock.sendall(msg)

# Print error
except socket.errno as e:
    print("Socket error", e)

# Close sock
finally:
    mysock.close()

# Netcat and listen to port 5555 to get message