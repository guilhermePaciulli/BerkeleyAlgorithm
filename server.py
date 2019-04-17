import socket
import sys
import re
import time
import threading
from socket import error as socket_error

class Server:

    def __init__(self, addr, time, d, slavesfile, logfile):
        ip_port = re.split(":", addr)
        self.ip = ip_port[0] # the master's listening IP
        self.port = int(ip_port[1]) # the master's listening port
        # Creating socket that can both receive and send packages
        self.slave_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.slave_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.slave_socket.bind((self.ip, self.port)) # Binding to given IP and port
        self.time = time
        self.d = d
        self.slaves = self._read_slaves_file(slavesfile)
        self.logfile = open(logfile, "w+")

    def run(self):
        self.slave_socket.listen(10) # Start listening up to 10 connections
        self._log("SERVER LISTENING AT "+self.ip+":"+str(self.port))
        while True:
            # requesting to all slaves their times
            for slave in self.slaves:
                t = self._receive_time(slave.ip, slave.port)
                # updating slave time
                slave.time = t
            # removing those who don't respect the d tolerance and were
            # obtained (time != -1)
            f = lambda s: s.time != -1 and abs(self.time - s.time) < self.d
            filt_slaves = list(filter(f, self.slaves))
            # calculating difference for each time obtained
            filt_slaves = map(lambda s: self.time - s.time, filt_slaves)
            # getting the times in a list
            list_times = map(lambda s: filt_slaves.time)
            # calculating average, the + 1 represents the master's time
            avg = sum(list_times) / (len(list_times) + 1)
            # updating master's time
            self.time += avg
            self._log("UPDATED TIME AVERAGE TO "+str(avg))

            for slave in filt_slaves:
                self._send_time(slave.ip, slave.port, avg)

            time.sleep(5) # updates clocks every 5 seconds

    # function used to receive clock time from a connected client
    def _receive_time(self, ip, port):
        soc = socket.socket() # create socket  to connect to client
        try:
            soc.connect((ip, port)) # attempt to open connection
            soc.send("request_time") # send request
            time = int(soc.recv(1024).decode()) # receive clock time
            self._log("RECEIVED FROM CLIENT "+ slave.ip+":"+str(slave.port)
                     +" THE TIME "+str(slave.time))
            return time
        except socket_error as serr:
            # if fails logs that the client is down
            self._log("CLIENT "+ip+":"+str(port)+" IS DOWN, REQUEST FAILED")
            return -1

    def _send_time(self, ip, port, avg):
        soc = socket.socket() # create socket  to connect to client
        try:
            soc.connect((ip, port)) # attempt to open connection
            soc.send("update_time:"+str(avg)) # send request to update time
        except socket_error as serr:
            # if fails logs that the client is down
            self._log("CLIENT "+ip+":"+str(port)+" IS DOWN, UPDATE FAILED")
            return -1

    # reads the slaves file and returns a list with all ips and ports of
    # the slaves
    def _read_slaves_file(self, file_name):
        slaves = []
        file = open(file_name, "r")

        for line in file.readlines():
            ipPort = re.split(":", line)
            # the list is instances of the Slave class with port, ip and time
            # the time is not yet defined
            slaves.append(Slave(ipPort[0], int(ipPort[1])))

        file.close()
        return slaves

    def _log(self, log):
        print log
        self.logfile.write(log + "\n")

class Slave:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.time = -1
