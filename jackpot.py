import listen
import threading
import time

listen.finish_missed_lotteries() # DELETE (?)
push_thread = threading.Thread(target=listen.try_push, args=("ticket",))
push_thread.daemon = True; push_thread.start()

while True:
    try:
        id = listen.create_lottery(_minutes=5)
        if id is not None:
            listen.await_jackpot(id)
            time.sleep(15)
            # Dodac time.sleep(x) zeby zgadzalo sie z animacja na frotenedzie
        
    except KeyboardInterrupt:
        break
