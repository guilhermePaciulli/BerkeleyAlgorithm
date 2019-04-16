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
            times = []

            for slave in self.slaves:
                t = self._receive_time(slave[0], slave[1])
                if t != -1:
                    self._log("RECEIVED FROM CLIENT "+ slave[0]+":"+str(slave[1])+" THE TIME "+str(t))
                    times.append(t)
            # removing those who don't respect the d tolerance
            filtered_times = list(filter(lambda tim: abs(self.time - tim) < self.d, times))
            if len(filtered_times) > 0: # no connections, no time update
                # calculating difference for each time obtained
                filtered_times = map(lambda tim: self.time - tim, filtered_times)
                avg = sum(filtered_times) / len(filtered_times) # calculating average
                self._log("UPDATED TIME AVERAGE TO "+str(avg))
            else:
                self._log("TIME UPDATE WAS IMPOSSIBLE DUE TO LACK OF VALID CLIENTS")

            time.sleep(5) # updates clocks every 5 seconds

    # function used to receive clock time from a connected client
    def _receive_time(self, ip, port):
        soc = socket.socket() # create socket  to connect to client
        try:
            soc.connect((ip, port)) # attempt to open connection
            soc.send("request_time") # send request
            time = int(soc.recv(1024).decode()) # receive clock time
            return time
        except socket_error as serr:
            # if fails logs that the client is down
            self._log("CLIENT "+ip+":"+str(port)+" IS DOWN")
            return -1

    # reads the slaves file and returns a list with all ips and ports of
    # the slaves
    def _read_slaves_file(self, file_name):
        slaves = []
        file = open(file_name, "r")

        for line in file.readlines():
            ipPort = re.split(":", line)
            # the list is a list of lists, each list has the first argument as
            # the IP and the second the port
            slaves.append([ipPort[0], int(ipPort[1])])

        file.close()
        print slaves
        return slaves

    def _log(self, log):
        print log
        self.logfile.write(log)
