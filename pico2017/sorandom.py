#!/usr/bin/python -u
import random,string

encflag = ""
random.seed("random")
flag = "BNZQ:8o149b15764q471k2533971t6w78liec"
toguess = string.ascii_lowercase + string.ascii_uppercase

for c in flag:
  if c.isupper() or c.islower():
    num = random.randrange(0,26)
    for letter in toguess:
      if c == chr((ord(letter)-ord('a')+num)%26 + ord('a')):
        encflag += letter
        break
      if c == chr((ord(letter)-ord('A')+num)%26 + ord('A')):
        encflag += letter
        break

  elif c.isdigit():
    num = random.randrange(0,10)
    for digit in string.digits:
      if c == chr((ord(digit)-ord('0')+num)%10 + ord('0')):
        encflag += digit
        break
  else:
    encflag += c
print "Unguessably Randomized Flag: "+encflag
