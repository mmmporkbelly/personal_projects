"""
Grabs banners with socket and regex modules
Part of Mastering Python - Networking and Security Udemy Course
Seido Karasaki(yakitategohan on github)
v1 3/2/2023
"""
import socket
import re

# Instance of a socket, AF_INET indicates it's an internet family, SOCK_STREAM indicates TCP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("www.microsoft.com", 80))

# Set get msg
http_get = b"GET / HTTP/1.1\nHost: www.microsoft.com\n\n"
data = ''

try:
    # Send get request, limit response to 1024 because we only care about the header
    sock.sendall(http_get)
    data = sock.recvfrom(1024)
    print("Getting banner")
except socket.error:
    print(f'Socket error: {socket.errno}')
finally:
    print("Closing connection")
    sock.close()

# Set byte data to str
strdata = data[0].decode("utf-8")

# Split data by lines
headers = strdata.split('\n')

# Use regex to get banner
for line in headers:
    if re.search('Server:', line):
        # line = line.replace("Server:", "")
        print(line)
