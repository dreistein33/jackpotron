# MOZE KIEDYS COS Z TEGO WYCIAGNE XD


def is_profit(lot_obj: Lottery) -> bool:
    """
    Define if given lottery is profit.
    :param lot_obj: Object of Lottery class.
    :return: Profit or no??
    """
    if len(lot_obj.users) > 0 and lot_obj.prize > 0:
        pool_sum = sum([x['amount'] for x in lot_obj.users])
        if pool_sum > lot_obj.prize:
            return True
    return False


def get_winner(id: int):
    lottery_obj = assembly_lottery_with_users(id)
    participants = list(set([x['sender'] for x in lottery_obj.users]))
    winner = random.choice(participants)

    return winner


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


if __name__ == '__main__2':
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