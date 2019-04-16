from server import *
from client import *
import sys


def startAsServer(masterIP, time, d, slavesfile, logfile):
    Server(masterIP, time, d, slavesfile, logfile).run()

def startAsClient():
    client.run()

if __name__ == '__main__':
    if sys.argv[1] == "-m": # reads arguments to master
        masterIP = sys.argv[2]
        time = int(sys.argv[3])
        d = int(sys.argv[4])
        slavesfile = sys.argv[5]
        logfile = sys.argv[6]

        startAsServer(masterIP, time, d, slavesfile, logfile)
    elif sys.argv[2] == "-s": # reads arguments to slave
        startAsClient()
    else:
        print "ARGUMENTS ERROR"
