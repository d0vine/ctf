#!/usr/bin/env python
import socket
import re

rgx1 = "'[a-zA-Z]' character '[0-9]+' times"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('34.206.4.227', 41123))

content = ""
while True:
    buf = s.recv(4096)
    content += buf
    if len(buf) < 4096:
        break

print(content)
print()
m = re.search(rgx1, content, re.MULTILINE)

print(m.group(1))
