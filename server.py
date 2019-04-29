import socket
import sys
import re
import time
import threading
from socket import error as socket_error

class Server:

    def __init__(self, addr, time, d, slavesfile, logfile):
        ip_port = re.split(":", addr)
        # the master's listening ip
        self.ip = ip_port[0]
        # the master's listening port
        self.port = int(ip_port[1])
        # Creating socket that can both receive and send packages
        self.slave_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.slave_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # binding socket to given ip and port
        self.slave_socket.bind((self.ip, self.port))
        self.time = time
        self.d = d
        # getting slaves from file
        self.slaves = self._read_slaves_file(slavesfile)
        # opening logfile
        self.logfile = open(logfile, "w+")

    # stars the whole process
    def run(self):
        # listening up for a number of connections equals
        # to the number of slaves
        self.slave_socket.listen(len(self.slaves))
        self._log("SERVER LISTENING AT "+self.ip+":"+str(self.port))
        while True:
            # requesting to all slaves their times
            for slave in self.slaves:
                t = self._receive_time(slave)
                # updating slave time
                slave.time = t
            # removing those who don't respect the d tolerance and were
            # reachable (time != -1)
            f = lambda s: s.time != -1 and abs(s.time - self.time) < self.d
            filt_slaves = list(filter(f, self.slaves))
            # calculating difference for each time obtained, the appended 0
            # represents the master's time
            times = map(lambda s: s.time - self.time, filt_slaves)
            times.append(0)
            # calculating average
            avg = sum(times) / len(times)
            # updating master's time, only updates if the average is different
            # than zero
            if avg != 0:
                self._log("NEW AVERAGE OF "+str(avg)+" OBTAINED")
                self._log("OLD TIME IS "+str(self.time))
                self.time += avg
                self._log("UPDATED TIME TO "+str(self.time))

                # updating clients' time
                for slave in filt_slaves:
                    self._send_time(slave, self.time)
            else:
                self._log("NOTHING TO UPDATE")

            # waiting 5 seconds before next update
            time.sleep(5)

    # function used to receive clock time from a connected client
    def _receive_time(self, slave):
        # creating socket to connect to client
        soc = socket.socket()
        try:
            # attempting to open connection
            soc.connect((slave.ip, slave.port))
            # sending request
            soc.send("request_time")
            # receiving clock time
            time = int(soc.recv(1024).decode())
            slave.time = time
            self._log("RECEIVED FROM CLIENT "+slave.ip+":"+str(slave.port)
                     +" THE TIME "+str(slave.time))
            soc.close()
            return time
        except socket_error as serr:
            # if fails to connect to client, logs that the client is down
            self._log("CLIENT "+slave.ip+":"+str(slave.port)+" IS DOWN, REQUEST FAILED")
            soc.close()
            return -1

    # function used to send average to slaves
    def _send_time(self, slave, time):
        # creating socket  to connect to client
        soc = socket.socket()
        try:
            # attempting to open connection
            soc.connect((slave.ip, slave.port))
            # sending request to update time
            soc.send("update_time:"+str(time))
        except socket_error as serr:
            # if fails to connect to client, logs that the client is down
            self._log("CLIENT "+slave.ip+":"+str(slave.port)+" IS DOWN, UPDATE FAILED")
            return -1

    # reads the slaves file and returns a list with all ips and ports of
    # the slaves
    def _read_slaves_file(self, file_name):
        slaves = []
        file = open(file_name, "r")

        for line in file.readlines():
            ipPort = re.split(":", line)
            # the list is constituted of instances of the Slave class
            # with port, ip and time, being each instance's time
            # not yet defined
            slaves.append(Slave(ipPort[0], int(ipPort[1])))

        file.close()
        return slaves

    def _log(self, log):
        print "[MASTER]" + log
        self.logfile.write("[MASTER] " + log + "\n")

class Slave:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.time = -1
