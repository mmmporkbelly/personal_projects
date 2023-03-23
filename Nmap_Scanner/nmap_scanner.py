#!/usr/bin/python3
"""
Automating an nmap scanner
Seido Karasaki(yakitategohan on github)
v1 3/6/2023
"""

import nmap
import re
# Call nmap portscanner class

def valid_ip(ip):
    # Regex for IPv4
    regex = re.compile(r'^(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$')
    res = regex.findall(ip)
    if res:
        return True


scanner = nmap.PortScanner()


if __name__ == "__main__":
    print("Welcome, this is a simple nmap automation nmap tool")
    print("---------------------------------------------------")
    ip_addr = input('Please enter the IP address you would like to scan:\n')
    # While the IP is not valid, loop
    while not valid_ip(ip_addr):
        ip_addr= input('Please enter a valid IP address:\n')
    print(f'This the IP you would like to scan: {ip_addr}')
    response = input("""\nPlease enter the type of scan you would like to run
                    1)SYN ACK Scan
                    2)UDP Scan
                    3)Comprehensive Scan""")
    print(f'You have selected: {response}')
    if
