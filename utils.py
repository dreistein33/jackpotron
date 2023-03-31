import db
import time
import lot
import datetime
import random


def create_lottery(_minutes, _hours=0, _days=0):
    _db = db.Database()
    start_time = time.time()
    end_time = datetime.datetime.fromtimestamp(start_time) + datetime.timedelta(days=_days, minutes=_minutes, hours=_hours) 
    wallet = 'TKsK4ohrvsKJwVUkdy4ocTD32MAh1UparG'
    # Check if any other lottery is started
    lotteries_started = _db.get_table_data('loteria', {'status': "'started'"})
    print(lotteries_started, " Started lotteries!")
    # Create lottery if none are active
    if len(lotteries_started) == 0:
        _db.generic_create_record('loteria', {'starttime': start_time, 'endtime': end_time.timestamp(), 'wallet': wallet, 'status': 'started', 'prize': 0, 'winner': None})
        id = _db.get_table_data("loteria")[-1]['id']
        return id
    # Return id of lottery if any running
    elif len(lotteries_started) == 1:
        id = _db.get_table_data("loteria")[-1]["id"]
        return id


def get_needed_data(db_obj):
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


def assembly_lottery_with_users(db, id):
    """Return an lottery object assembled with all transactions in regard to it"""
    lottery = db.get_table_data('loteria', {'id': id})[0]
    fitable_txs = db.get_table_data('ticket')

    lottery_obj = lot.Lottery(lottery['id'], lottery['starttime'], lottery['endtime'], lottery['wallet'], lottery['status'], lottery['prize'], lottery['winner'])

    for tx in fitable_txs:
        if int(tx['memo']) == lottery_obj.id:
            lottery_obj.users.append(tx)

    return lottery_obj


def get_winner(id):
    lottery_obj = assembly_lottery_with_users(id)
    participants = list(set([x['sender'] for x in lottery_obj.users]))
    winner = random.choice(participants)

    return winner


def try_push(name):
    while True:
        if len(get_fitable_txs()) > 0:
            for items in get_fitable_txs():
                if not db.dbase.is_pushed(name, ('timestamp', items['timestamp'])):
                    items['loteria_id'] = int(items['memo'])
                    db.dbase.generic_create_record(name, items)
                    print(f"Succesfully pushed tx")
        time.sleep(10)


def await_roll(id):
    """This function will run as a separate thread and wait to end the lottery"""
    lottery_obj = assembly_lottery_with_users(id)

    lottery_end_time = lottery_obj.end_time
    if time.time() < lottery_end_time:
        print(f"Awaiting ID {id}")
        
        time.sleep(lottery_end_time - time.time())
        lottery_obj = assembly_lottery_with_users(id)
        
        if len(lottery_obj.users) == 0:
            return
        else:
            winner = get_winner(id)

        # assert winner != lottery_obj.address, "If this happened, you fucked up"

        if lottery_obj.status == 'started':
            if time.time() >= lottery_obj.end_time:
                lottery_obj.winner = winner
                wallet = lot.Wallet(lot.adr['base58check_address'])
                wallet.set_pk(lot.adr['private_key'])

                wallet.send_tx(winner, lottery_obj.prize)


        
            


    

