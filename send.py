from lot import *
import sys
# python send.py 69
address = adr['base58check_address']

id = sys.argv[1]

w1 = Wallet(adr_2['base58check_address'])
w2 = Wallet(adr_3['base58check_address'])
w3 = Wallet(adr_4['base58check_address'])

w1.set_pk(adr_2['private_key'])
w2.set_pk(adr_3['private_key'])
w3.set_pk(adr_4['private_key'])

print(w1.send_tx(address, 3, id))
print(w2.send_tx(address, 5, id))
print(w3.send_tx(address, 2, id))

