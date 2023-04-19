from lot import *
import sys

address = adr['base58check_address']

id = int(sys.argv[1])  # Convert id to an integer
num_repetitions = int(sys.argv[2])

w1 = Wallet(adr_2['base58check_address'])
w2 = Wallet(adr_3['base58check_address'])
w3 = Wallet(adr_4['base58check_address'])

w1.set_pk(adr_2['private_key'])
w2.set_pk(adr_3['private_key'])
w3.set_pk(adr_4['private_key'])

for i in range(num_repetitions):
    current_id = id + i
    curid = str(current_id)
    print(curid)   # Add id and i together
    print(w1.send_tx(address, 1, curid))
    print(w2.send_tx(address, 1, curid)) 
    print(w3.send_tx(address, 1, curid))

# pierwszy arg to id obecne
# drugi arg to multipler nie wiem czemu powyzej 9 nie dziala prawidlowo
# dajac np python send.py 69 3 wyslane beda transakcje na loterie o nr 69,70,71
