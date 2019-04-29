import Queue
import threading
import time
from main import *

slave_1 = threading.Thread(target=startAsClient, args = ("127.0.0.1:9000", 175, "test/logs/slave_log_1.txt"))
slave_2 = threading.Thread(target=startAsClient, args = ("127.0.0.1:9001", 180, "test/logs/slave_log_2.txt"))
slave_3 = threading.Thread(target=startAsClient, args = ("127.0.0.1:9002", 205, "test/logs/slave_log_3.txt"))
master = threading.Thread(target=startAsServer, args = ("127.0.0.1:8080", 185, 15, "test/slaves.txt", "test/logs/master_log.txt"))

if __name__ == '__main__':
    slave_1.start()
    time.sleep(1)
    slave_2.start()
    time.sleep(1)
    slave_3.start()
    time.sleep(1)
    master.start()
