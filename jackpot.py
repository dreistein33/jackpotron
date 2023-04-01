import listen
import threading


listen.finish_missed_lotteries() # DELETE (?)
push_thread = threading.Thread(target=listen.try_push, args=("ticket",))
push_thread.daemon = True; push_thread.start()

while True:
    try:
        id = listen.create_lottery(_minutes=15)
        if id is not None:
            listen.await_jackpot(id)
        
    except KeyboardInterrupt:
        break
