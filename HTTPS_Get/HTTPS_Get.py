"""
Send HTTPS get request using ssl and socket modules.
Seido Karasaki(yakitategohan on github)
v1 3/3/2023
"""
import ssl
import socket
import sslcontext

# Create TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wrap in TLS/SSL
ssock = ssl.wrap_socket(s)

try:
    # Connect to google via port 443
    ssock.connect(("www.google.com", 443))

    # Print encryption and hash methods used
    print(ssock.cipher())

except:
    print("Error connecting to addr")

try:
    # Write a get request
    ssock.write(b"Get / HTTP/1.1 \r\n")
    ssock.write(b"Host: www.google.com\n\n")
except Exception as e:
    print(f"Write error: {e}")

data = bytearray()
try:
    data =ssock.read()
except Exception as e:
    print(f"Read error: {e}")

print(data.decode("utf-8"))