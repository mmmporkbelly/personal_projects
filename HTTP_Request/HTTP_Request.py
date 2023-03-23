"""
A simple HTTP get request
Seido Karasaki(yakitategohan on github)
v1 3/2/2023
"""

import http.client

h = http.client.HTTPConnection("www.google.com")
h.request("GET", "/")
data = h.getresponse()
# Prints the server response code, i.e. 200, and headers
print(data.code)
print(data.headers)
text = data.readlines()
# Decode text from bytes
for line in text:
    print(line.decode("utf-8"))
