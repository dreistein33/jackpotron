import db
import numpy as np
import requests
import time
import lot
import random
import threading

db_obj = db.Database()


class Lottery:
    def __init__(self, id, start_time, end_time, address, status, prize) -> None:
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.address = address
        self.status = status
        self.prize = prize
        self.min_entry = self.prize // 10
        self.users = []

    def __str__(self) -> str:
        return self.address
    
    def __setattr__(self, __name: str, __value: str) -> None:
        if __name == "winner":
            self.__dict__[__name] = __value
            db_obj.edit_value('loteria', {'winner': __value, 'status': 'ended'}, ('id', self.id))
        else:
            self.__dict__[__name] = __value


def get_needed_data():
    loteries = db_obj.get_table_data('loteria')
    if len(loteries) > 0:
        memos = [x['id'] for x in loteries]
        start_times = [x['starttime'] for x in loteries]
        end_times = [x['endtime'] for x in loteries]
        min_start_time = min(start_times)
        max_end_time = max(end_times)
        return memos, min_start_time, max_end_time


def get_fitable_txs():
    wallet = lot.Wallet(lot.adr['base58check_address'])
    try:
        memos, start, end = get_needed_data()
    except Exception as e:
        return []
    txs = wallet.get_txs()
    fitable = []
    if len(txs) > 0:
        for items in txs:
            if items['timestamp'] >= start and items['timestamp'] <= end:
                if int(items['memo']) in memos:
                    fitable.append(items)

    return fitable


def assembly_lottery_with_users(id):
    """Return an lottery object assembled with all transactions in regard to it"""
    lottery = db_obj.get_table_data('loteria', {'id': id})[0]
    fitable_txs = db_obj.get_table_data('ticket')

    lottery_obj = Lottery(lottery['id'], lottery['starttime'], lottery['endtime'], lottery['wallet'], lottery['status'], lottery['prize'])

    for tx in fitable_txs:
        if int(tx['memo']) == lottery_obj.id:
            lottery_obj.users.append(tx)

    return lottery_obj


def is_profit(lot_obj: Lottery) -> bool:
    if len(lot_obj.users) > 0 and lot_obj.prize > 0:
        pool_sum = sum([x['amount'] for x in lot_obj.users])
        if pool_sum > lot_obj.prize:
            return True
    return False


def get_winner_wage_based(id):
    lot_obj = assembly_lottery_with_users(id)
    users_tickets = {}
    users = lot_obj.users
    for user in users:
        # Calculate the amout of tickets for every sender
        # 1 TRX = 1 Ticket
        try:
            users_tickets[user['sender']] += user['amount']
        except KeyError:
            users_tickets[user['sender']] = user['amount']

    winner = np.random.choice(list(users_tickets.keys()), 1, p=[x/lot_obj.prize for x in users_tickets.values()])
    winner_str = str(winner[0])
    print(type(winner_str), winner_str)

    return winner_str


def get_winner(id):
    lottery_obj = assembly_lottery_with_users(id)
    participants = list(set([x['sender'] for x in lottery_obj.users]))
    winner = random.choice(participants)

    return winner


def try_push(name):
    while True:
        if len(get_fitable_txs()) > 0:
            for items in get_fitable_txs():
                if not db_obj.is_pushed(name, ('timestamp', items['timestamp'])):
                    items['loteria_id'] = int(items['memo'])
                    # Add new transaction record to database.
                    db_obj.generic_create_record(name, items)
                    lot_obj = assembly_lottery_with_users(items['loteria_id'])
                    # Update prize to matching jackpot lottery to database.
                    new_prize = lot_obj.prize + items['amount']
                    db_obj.edit_value('loteria', {'prize': new_prize}, ('id', items['loteria_id']))
                    print(f"Succesfully pushed tx")
        time.sleep(10)


def finish_lottery(id):
    lottery_obj = assembly_lottery_with_users(id)
        
    # assert winner != lottery_obj.address, "If this happened, you fucked up"

    if lottery_obj.status == 'started' and time.time() >= lottery_obj.end_time:
        if len(lottery_obj.users) == 0:
            print("No participants! Closing the lottery.")
            lottery_obj.winner = None
            return
                
        wallet = lot.Wallet(lot.adr['base58check_address'])
        wallet.set_pk(lot.adr['private_key'])

        profitable = is_profit(lottery_obj)
        if profitable:
            winner = get_winner(id)
            lottery_obj.winner = winner
            wallet.send_tx(winner, lottery_obj.prize)
        else:
            lottery_obj.winner = None
            for items in lottery_obj.users:
                wallet.send_tx(items['sender'], items['amount'])
                print(f"Sending back {items['amount']}TRX to {items['sender']}")


def is_eligible(lot_obj: Lottery) -> bool:
    """Check if current jackpot state allows to roll."""
    if len(lot_obj.users) > 0 and lot_obj.prize > 0:
        return True
    return False


def finish_jackpot(id):
    lottery_obj = assembly_lottery_with_users(id)
        
    # assert winner != lottery_obj.address, "If this happened, you fucked up"

    if lottery_obj.status == 'started' and time.time() >= lottery_obj.end_time:
        if len(lottery_obj.users) == 0:
            print("No participants! Closing the lottery.")
            lottery_obj.winner = None
            return
                
        wallet = lot.Wallet(lot.adr['base58check_address'])
        wallet.set_pk(lot.adr['private_key'])

        eligible = is_eligible(lottery_obj)
        if eligible:
            winner = get_winner_wage_based(id)
            lottery_obj.winner = winner
            wallet.send_tx(winner, lottery_obj.prize)
        else:
            lottery_obj.winner = None


def await_roll(id):
    """This function will run as a separate thread and wait to end the lottery"""
    lottery_obj = assembly_lottery_with_users(id)
    
    lottery_end_time = lottery_obj.end_time
    
    if time.time() < lottery_end_time and lottery_obj.status == 'started':

        print(f"Awaiting ID {id}")
        time.sleep(lottery_end_time - time.time())

        finish_lottery(id)

    elif time.time() > lottery_end_time and lottery_obj.status == 'started':
        finish_lottery(id)
        print(f"LOTTERY ID {lottery_obj.id} NOT FINALIZED")


def await_jackpot(id):
    lottery_obj = assembly_lottery_with_users(id)
    end_time = lottery_obj.end_time
    started = lottery_obj.status = "started"

    current_time = time.time()
    if current_time < end_time and started:
        print(f"Awaiting new Jackpot Id #{id}")
        time.sleep(end_time-time.time())
        finish_jackpot(id)
    
    elif current_time > end_time and started:
        finish_jackpot(id)


def finish_missed_lotteries():
    lotteries = db_obj.get_table_data('loteria')

    for lot in lotteries:
        missed = time.time() > lot['endtime'] and lot['status'] == 'started'

        if missed:
            finish_jackpot(lot['id'])
            print(f"Succesfully finished JACKPOT #{lot['id']}")



if __name__ == '__main__':
    processed_lotteries = set()
    
    push_thread = threading.Thread(target=try_push, args=("ticket",))
    push_thread.daemon = True
    push_thread.start()

    is_running = True

    while is_running:
        try:
            lotteries_to_await = requests.get("http://localhost:5000/lotteries").json()

            for items in lotteries_to_await:
                # Check if time to await is not exceeding the threading.TIMEOUT_MAX value
                eligible = items['endtime'] - time.time() < threading.TIMEOUT_MAX
                # If not stop executing this method.
                if items['id'] not in processed_lotteries and eligible:
                    await_thread = threading.Thread(target=await_roll, args=(items['id'],))
                    await_thread.daemon = True; await_thread.start()

                    processed_lotteries.add(items['id'])
            time.sleep(10)

        except KeyboardInterrupt:
            del db_obj
            is_running = False
   