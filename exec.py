import Queue
import threading
import time
from main import *

# daemon flag maintains the threads dependent to the thread they are started
# (this case, this thread)

slave_1 = threading.Thread(target=startAsClient, args = ("127.0.0.1:9000", 175, "test/logs/slave_log_1.txt"))
slave_1.daemon = True
slave_2 = threading.Thread(target=startAsClient, args = ("127.0.0.1:9001", 180, "test/logs/slave_log_2.txt"))
slave_2.daemon = True
slave_3 = threading.Thread(target=startAsClient, args = ("127.0.0.1:9002", 205, "test/logs/slave_log_3.txt"))
slave_3.daemon = True
master = threading.Thread(target=startAsServer, args = ("127.0.0.1:8080", 185, 15, "test/slaves.txt", "test/logs/master_log.txt"))
master.daemon = True

if __name__ == '__main__':
    try: # starts each thread
        slave_1.start()
        time.sleep(1) # waits a second between threads to wait for them to complete the starting process
        slave_2.start()
        time.sleep(1)
        slave_3.start()
        time.sleep(1)
        master.start()
        while True:
            time.sleep(100) # maintain this thread execution alive while others are alive
    except (KeyboardInterrupt, SystemExit): # handles keyboard interruption (a.k.a. ctrl+c)
        print("\nEXITING TEST")
