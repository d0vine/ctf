#!/usr/bin/env python3
import errno
import os
import re

from scapy.all import rdpcap
from scapy.all import Raw
from scapy.all import TCP

webserver_port = 8080
out_dir = "dumped"

print("[ ] Reading pcap...")
pcap = rdpcap('data.pcap')
print("[+] pcap read!")

FIN = 0x01
PSH = 0x08
ACK = 0x10

regex = r"GET /images/[a-z0-9]+"
images = {}
current_filename = ""

print("[ ] Looking for images in the pcap file...")

for packet in pcap:
    if TCP in packet and Raw in packet:  # HTTP is TCP-only
        if current_filename and packet[TCP].sport == webserver_port:
            if b"HTTP" not in bytes(packet[TCP][Raw]):
                if packet[TCP].flags == PSH | ACK or packet[TCP].flags == ACK:
                    images[current_filename][-1] += bytes(packet[TCP][Raw])
                if packet[TCP].flags == FIN | ACK:
                    current_filename = ""
        else:
            try:
                potential_req_string = bytes(packet[TCP][Raw]).decode('ascii')
                match = re.match(
                    r"GET /\w/(.*) (.*)",
                    potential_req_string
                )
                if match:
                    filename = match.groups()[0]
                    if filename not in images:
                        images[filename] = [b""]
                        current_filename = filename
                    else:
                        images[filename].append(b"")
                        current_filename = filename
            except UnicodeError:
                pass   # *shrug*

print("[+] Done processing pcap!")
print("[ ] Processing images...")

for filename, file_list in images.items():
    for session_id in range(0, len(file_list)):
        full_out_dir = "{}/{}".format(out_dir, session_id + 1)
        try:
            os.makedirs(full_out_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        file_path = "{}/{}".format(full_out_dir, filename)
        with open(file_path, 'wb') as outfile:
            outfile.write(file_list[session_id])

print("[+] All done!")
