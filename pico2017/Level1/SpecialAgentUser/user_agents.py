#!/usr/bin/env python3
from scapy.all import rdpcap
from scapy.all import TCP
from scapy.all import Raw

pcap = rdpcap('data.pcap')
user_agents = set()

packets = [packet for packet in pcap if TCP in packet and Raw in packet]

for packet in packets:
    if b'User-Agent' in bytes(packet[TCP][Raw]):
        request = bytes(packet[TCP][Raw]).decode('ascii').split('\n')
        for line in request:
            if line.startswith('User-Agent'):
                user_agents.add(line.split(': ')[1].strip())
        
for agent in user_agents:
    print(agent)
