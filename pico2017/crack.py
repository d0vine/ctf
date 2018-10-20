with open('cracked.txt') as f:
    hash_pass = f.readlines()

hash_pass = {h: p for h,p in [tuple(l.strip().split(':')) for l in hash_pass]}

with open('logins_passwords.txt') as f:
    login_hash = f.readlines()

with open('cracked_pass.txt', 'w') as f:
    f.write('\n'.join([':'.join([l,hash_pass.get(h, '?')]) for l,h in [tuple(l.strip().split(':')) for l in login_hash]]))
