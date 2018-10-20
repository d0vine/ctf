#!/usr/bin/env python3
from socket import AF_INET
from socket import SOCK_STREAM
from socket import socket

primes = []
with open('primes.txt', 'r') as prime_file:
    for line in prime_file:
        primes.append(int(line))

task_addr = ("shell2017.picoctf.com", 27525)

s = socket(AF_INET, SOCK_STREAM)
s.connect(task_addr)
s.recv(4096)  # banner
lines = s.recv(4096).split(b'\n')
N = int(lines[1][2:])
e = int(lines[2][2:])

print("N = {}".format(N))
print("e = {}".format(e))

s.send(b'2\n')
for i in range(0,2):
    data = s.recv(4096)
    print(data)

signatures = []
last_p = 0

for p in primes:
    try:
        s.send('{}\n'.format(p).encode('ascii'))
        s.recv(1024)
        lines = s.recv(4096).split(b'\n')
        signatures.append(int(lines[0][1:]))
        last_p = p
    except Exception:
        break

print("last p: {}".format(last_p))

