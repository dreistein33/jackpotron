import db
import json
import numpy as np
import requests
import time
import lot
import random
import simple_websocket
import threading

db_obj = db.Database()


class Lottery:
    def __init__(self, id: int, start_time: float, end_time: float, address: str, status: str, prize: float) -> None:
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


def to_frontend() -> None:
    """
    This function triggers the event on WebSocket Server that cause broadcasting the data from database to all connected clients.
    Returns: None
    """
    client = simple_websocket.Client("ws://localhost:4998/chuj")
    # event_data = {"event": "data"}
    # event_data_json = json.dumps(event_data)
    # client.send(event_data_json.encode())
    # data = client.receive()
    # print(data)

def get_needed_data() -> None:
    """Get timestamps and memos of active lotteries."""
    loteries = db_obj.get_table_data('loteria')
    if len(loteries) > 0:
        memos = [x['id'] for x in loteries]
        start_times = [x['starttime'] for x in loteries]
        end_times = [x['endtime'] for x in loteries]
        min_start_time = min(start_times)
        max_end_time = max(end_times)
        return memos, min_start_time, max_end_time


def get_fitable_txs() -> list:
    """
    Get txs that fit into given time frames.
    :return: List of all transactions that fit lotteries.
    """
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


def assembly_lottery_with_users(id: int) -> Lottery:
    """
    Return an lottery object assembled with all transactions in regard to it
    :param id: Id of lottery to be assembled.
    :return: Lottery object with fitting txs.
    """
    lottery = db_obj.get_table_data('loteria', {'id': id})[0]
    fitable_txs = db_obj.get_table_data('ticket')

    lottery_obj = Lottery(lottery['id'], lottery['starttime'], lottery['endtime'], lottery['wallet'], lottery['status'], lottery['prize'])

    for tx in fitable_txs:
        if int(tx['memo']) == lottery_obj.id:
            lottery_obj.users.append(tx)

    return lottery_obj


def get_winner_wage_based(id: int) -> str:
    """
    Draw winner based on shares of single user of the prizepool.
    :param id: Id of lottery.
    :return: Winner's wallet address, str
    """
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

    # The p parameter is a list of wages which are result of dividing shares by prizepool.
    # Example: user1 ($1), user2 ($2), prizepool ($3) | user1_wage = user1 / prizepool and so on.
    winner = np.random.choice(list(users_tickets.keys()), 1, p=[x/lot_obj.prize for x in users_tickets.values()])
    winner_str = str(winner[0])
    print(type(winner_str), winner_str)

    return winner_str


def try_push(name:str):
    """
    Check for new transactions, and if there are any, push it to DB.
    :param name: Name of table in DB (This shit pretty stoopid) !TOFIX
    """
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


def is_eligible(lot_obj: Lottery) -> bool:
    """
    Check if current jackpot state allows to roll.
    :param lot_obj: Lottery class object.
    :return: bool
    """
    if len(lot_obj.users) > 0 and lot_obj.prize > 0:
        return True
    return False


def finish_jackpot(id):
    """Define if lottery meet the requirements to draw the winner and execute."""
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


def await_jackpot(id):
    """Wait, execute. Simple as that."""
    lottery_obj = assembly_lottery_with_users(id)
    end_time = lottery_obj.end_time
    started = lottery_obj.status 

    current_time = time.time()
    if current_time < end_time and started:
        print(f"Awaiting new Jackpot Id #{id}")
        time.sleep(end_time-time.time())
        finish_jackpot(id)
    
    # Idk if I should delete this.
    elif current_time > end_time and started:
        finish_jackpot(id)


def finish_missed_lotteries():
    lotteries = db_obj.get_table_data('loteria')

    for lot in lotteries:
        missed = time.time() > lot['endtime'] and lot['status'] == 'started'

        if missed:
            finish_jackpot(lot['id'])
            print(f"!MISSED! Succesfully finished JACKPOT #{lot['id']}")


if __name__ == "__main__":
    to_frontend()