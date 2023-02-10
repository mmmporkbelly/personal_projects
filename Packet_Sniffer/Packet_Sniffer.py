"""
A packet sniffer using scapy. Written to expand my own knowledge on cybersecurity.


This tool may be used for legal purposes only.  Users take full responsibility
for any actions performed using this tool.  If these terms are not acceptable to
you, then do not use this tool.

Seido Karasaki(yakitategohan on github)
v1 2/10/2023
"""

import scapy.all as scapy
from scapy.layers import http


# iface can be checked by ifconfig, ex: eth0 or lan0
# can filter with iface= for interface, filter= for protocols or ports, like port 80
def sniff():
    scapy.sniff(store=False, prn=process_sniffed_packet)


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    # Check packet has http layer
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ['username', 'user', 'login', 'password', 'pass']
        for keyword in keywords:
            if keyword in load:
                return load


def process_sniffed_packet(packet):
    # Check packet has http layer
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print(f'\t HTTP Request >> {url.decode()}')
        login_info = get_login_info(packet)
        if login_info:
            print(f'\n\t Possible username/password > {login_info.decode()}\n')


sniff()
