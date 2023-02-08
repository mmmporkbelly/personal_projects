"""
A network scanner using the scapy module
Returns all devices within given IP address via ARP packets
yakitategohan(Seido Karasaki on github)
v1 2/6/2023
"""

import scapy.all as scapy
import argparse


# Add functionality to include IP when running program
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range.")
    options = parser.parse_args()
    ip = str(options.target).split('/')
    ip = ip[0].split('.')
    for num in ip:
        if not 0 <= int(num) <= 255:
            raise ValueError('Please enter valid IPv4 address')
    return options


def scan(ip):
    # Instantiate ARP frame obj as arp_request
    arp_request = scapy.ARP(pdst=ip)

    # Instantiate Ethernet frame obj as broadcast, set MAC address as broadcast
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')

    # Combine both frames
    arp_request_broadcast = broadcast / arp_request

    # send request, returns two lists
    answered, unanswered = scapy.srp(arp_request_broadcast, timeout=1)

    # store each client into dict
    client_list = []
    for element in answered:
        client_dict = {'IP Address': element[1].psrc, 'MAC Address': element[1].hwsrc}
        client_list.append(client_dict)
    return client_list


def print_result(result_list):
    print('IP\t\t\tMac Address\n-------------------------------------------------------------')
    for client in result_list:
        print(f'{client["IP Address"]}\t\t{client["MAC Address"]}')


arguments = get_arguments()
scan_result = scan(arguments.target)
print_result(scan_result)
