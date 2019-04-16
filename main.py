from server import *
from client import *
import sys


def startAsServer(addr, time, d, slavesfile, logfile):
    Server(addr, time, d, slavesfile, logfile).run()

def startAsClient(addr, time, logfile):
    Client(addr, time, logfile).run()

if __name__ == '__main__':
    if sys.argv[1] == "-m": # reads arguments to master
        addr = sys.argv[2]
        time = int(sys.argv[3])
        d = int(sys.argv[4])
        slavesfile = sys.argv[5]
        logfile = sys.argv[6]

        startAsServer(addr, time, d, slavesfile, logfile)
    elif sys.argv[1] == "-s": # reads arguments to slave
        addr = sys.argv[2]
        time = int(sys.argv[3])
        logfile = sys.argv[4]
        startAsClient(addr, time, logfile)
    else:
        print "ARGUMENTS ERROR"
