import socket
import sys
import re
import time
import threading

class Server:

    def __init__(self, masterIP, time, d, slavesfile, logfile):
        ip_port = re.split(":", masterIP)
        ip = ip_port[0] # the master's listening IP
        port = int(ip_port[1]) # the master's listening port
        self.slave_socket = socket.socket() # Creating socket
        self.slave_socket.bind((ip, port)) # Binding to given IP and port
        self.time = time
        self.d = d
        self.slaves = self._read_slaves_file(slavesfile)
        self.logfile = open(logfile, "w+")

    def run(self):
        self.slave_socket.listen(10) # Start listening up to 10 connections
        self._log("SERVER LISTENING AT "+self.ip+":"+str(self.port))
        while True:

           time.sleep(5) # updates clocks every 5 seconds

    # thread function used to receive clock time from a connected client
    def start_receiving_time(self):
        while True:
            # recieve clock time
            clock_time_string = self.slave_socket.recv(1024).decode()
            clock_time = parser.parse(clock_time_string)
            clock_time_diff = datetime.datetime.now() - clock_time

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
