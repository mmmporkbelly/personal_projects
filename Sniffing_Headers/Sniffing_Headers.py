"""
Sniff packets, grab the banners using pcapy and struct
Seido Karasaki(yakitatgohan on github)
v1 3/3/2023
"""

import pcapy
from struct import *

def capture(interface):
    # Make capture file. device, # of byte to capture per packet, promiscuous mode, timeout
    cap = pcapy.open_live(interface, 65536, 1, 0)
    while 1:
        (header, payload) = cap.next()
        # Layer 2 header is 14 bytes long
        layer2header = payload[:14]




if __name__ == "__main__":
    # Find all network interfaces, print them
    devs = pcapy.findalldevs()
    print(devs)

    # Let user choose which to sniff on
    interface = input("What would you like to sniff on?\n")
    try:
        capture(interface)
    except:
        print("Invalid interface")
