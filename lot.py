import requests
import pandas as pd
from tronpy import Tron
from tronpy.keys import PrivateKey
import db

# Stworzenie testowej loterii
# Wyswietlenie jej przez HTTP na stronie
# Stworzenie loterii manualnie -> automatycznie
# (revard),(time_to_end),(users_count)
# (address_in),(address_out)

adr = {'base58check_address': 'TKsK4ohrvsKJwVUkdy4ocTD32MAh1UparG', 'hex_address': '416c93d3155128df9322162e113afbc3f9c04a45fa', 'private_key': 'ee8548699d2501032a6bf2f70f553331739bcc837ae20752248e6af588d18b42', 'public_key': '7e535ed016db0a0fab9b84a17163c427d02eb291f5a3d993a009d9a5343f194c3b80dbdd593c26ec7ee3efd541d14e9d573737186139337fd7cbcc251cf498ba'}

adr_2 = {'base58check_address': 'THukdpn6g7WtTTc3iKUqorircWSfLaF1hR', 'hex_address': '415719bfc2a62c93a05926acb360e623282bb78283', 'private_key': 'afe0090e39ac67ccdc67eb100a72c6644ceb1196d567c8d601f47e2add399c67', 'public_key': 'd1c1ff02059ce3f97e31e1cdc0b82e103fb599182efc087a9a8b5112f306e82eed4deb26be19548a54dc44022cb9e06cbb53047fb0dac2427e867f6856a2808f'}

adr_3 = {'base58check_address': 'TAGpRpbCmgBa3fZWJHhDg6GAM41r3HqwGn', 'hex_address': '410354a4eebdcde44a0b573235fd536e3b73541a12', 'private_key': '9b9ee6332daf868d365f8f2ca68deadb6ba00d1034a1c49c723c1b4e6bf7ba7b', 'public_key': '4b24043846fdc1c867d7bb050a2bffc05e0f6de39b316696811dd43d537ea715f160b30aa88027818089cf13cc851cb2ac011dfff55edf5b18567f2fe5e92b81'}

adr_4 = {'base58check_address': 'TFYijyFLY44gb9SdK6HPbVDUqNk6nqtPWw', 'hex_address': '413d2f2e65aa05668fcb23aa27ed38a5bec0057f10', 'private_key': '9cc28dd0282ed199e43fd7a84998855eeb95ad16af01a1fb5c640c4e204b5717', 'public_key': '003ad2c7dbb92c0c04b6f031b732dba70897b27b9816be63bba6c3e03a539fab1c95c6dbed52e34c16fe1d1ad338fe41d69e9065b89664c923bbc61e85805523'}

def flatten_dict(d, prefix=''):
    """This functions flattens the dict if any value is either another dict or list"""

    flat_dict = {}
    for k, v in d.items():
        if isinstance(v, dict):
            flat_dict.update(flatten_dict(v, prefix=f"{prefix}{k}."))
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    flat_dict.update(flatten_dict(item, prefix=f"{prefix}{k}[{i}]."))
                else:
                    flat_dict[f"{prefix}{k}[{i}]"] = item
        else:
            flat_dict[f"{prefix}{k}"] = v
    return flat_dict


class Lottery:
    def __init__(self, id, start_time, end_time, address, status, prize, winner) -> None:
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.address = address
        self.status = status
        self.prize = prize
        self.users = []
        self.min_entry = self.prize // 10 if self.prize > 10 else 0
        self.winner = winner

    def __str__(self) -> str:
        return self.address
        
    def format_userlist(self):
        """
        Format self.users list if there any are any duplicates sum them to the address, count probability, etc.
        This is to get the data ready for the API.
        """
        if len(self.users) > 0:
            users_df = pd.DataFrame(self.users)
            # Sum amounts for repeating addresses.
            formatted_users = users_df.groupby("sender", as_index=False)["amount"].sum()
            # Calculate the probability of winning the lottery.
            formatted_users["probability"] = formatted_users["amount"] / self.prize 
            # Convert DataFrame to list of dicts and set self.users attribute to it
            fusers_list = formatted_users.to_dict('records')
            self.users = fusers_list


        

class Serializer:
    """This class will return an object of any record/records in any table of sqlite3 db"""
    def __init__(self, data):
        if isinstance(data, dict):
            self.__dict__ = data      


class Wallet:
    def __init__(self, address) -> None:
        self.address = address
        self.client = Tron(network="shasta")

        assert self.client.is_address(self.address), f"Couldn't find relation to given address in network.\nAddress: {self.address}"

    def set_pk(self, pk):
        self.pk = PrivateKey(bytes.fromhex(pk))
    
    def get_balance(self):
        return self.client.get_account_balance(self.address)
    
    def send_tx(self, receiver, amount, _memo=''):
        txn = (
            self.client.trx.transfer(self.address, receiver, 1000000 * int(amount))
            .memo(_memo)
            .build()
            .sign(self.pk)
        )
        print(txn.broadcast().wait())

    def get_txs(self):
        url = f"https://api.shasta.trongrid.io/v1/accounts/{self.address}/transactions"
        response = requests.get(url)
        try:
            response_json = response.json()
        except Exception:
            pass

        tx_list = []

        for tx in response_json['data']:
            # Zdefiniuj wybrane elementy transakcji ktore chcemy zwrocic
            tx_info = tx['raw_data']['contract'][0]['parameter']['value']

            if 'contract_address' not in tx_info.keys():

                sender =  tx_info['owner_address']
                sender = self.client.to_base58check_address(sender)
                receiver = tx_info['to_address']
                receiver = self.client.to_base58check_address(receiver)
                amount = tx_info['amount'] / 1_000_000
                tx_id = tx['txID']
                timestamp = tx['raw_data']['timestamp'] / 1000
                try:
                    memo = bytes.fromhex(tx['raw_data']['data']).decode('utf-8')
                except KeyError as e:
                    pass
                
                tx_dict = {}
                # Dodaj wartosci do list kluczy w tx_dict
                if sender != self.address:    
                    tx_dict['sender'] = sender
                    tx_dict['receiver'] = receiver
                    tx_dict['amount'] = amount
                    # tx_dict['tx_id'] = tx_id
                    tx_dict['timestamp'] = timestamp
                    tx_dict['memo'] = memo

                # Dodaj transakcje
                    tx_list.append(tx_dict)
                                            
        return tx_list
# Loteria nr 1 id L1 nagroda 100trx
# My mamy jeden glowny portfel
# Klikasz przycisk "Wez udzial"
# Dostajesz adres portfela na ktory masz wyslac srodki
# Wysylasz taka ilosc jak wymagana
# W memo wpisujesz id loteri
# Silnik po starcie loterii caly czas sprawdza czy:
# Pojawiaja sie nowe transakcje
# Sprawdza czy czas do konca loterii jeszcze istnieje
# Jesli nie istnieje
# To sprawdza czy minimalna ilosc uczestnikow/coinow zostala osiagnieta
# Jesli tak
# Losuj zwyciezce, wyslij, zakoncz loterie, przenies ja do historii
# Jesli nie, refund transakcji, przenies do historii/ zmien status

# PAY ATTENTIPON BO KURWA REFUNDUW NIE MA

# wallet = Wallet(adr_2['base58check_address'])
# wallet.set_pk(adr_2['private_key'])
# wallet.get_latestx()

# wallet = Wallet('TVKNNMGcCrsTxLczPK3bd85bEB2m3kNAZ6')
# print(wallet.get_txs())

# def create_table_objects(name):
#     """Return an Serializer object from record from db"""
#     table_data = db.get_table_data(name)
#     return {f"{name}": [Serializer(x).__dict__ for x in table_data]}


# print(wallet.client.generate_address())
# tx = wallet.send_tx(adr['base58check_address'], 100, "1")
# # print(tx)
# print(wallet.get_txs())
