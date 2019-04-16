import socket
import sys
import re

class Client:

    def __init__(self, addr, time, logfile):
        ip_port = re.split(":", addr)
        ip = ip_port[0] # the slaves's listening IP
        port = int(ip_port[1]) # the slaves's listening port
        # Creating socket that can both receive and send packages
        self.master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.master_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.master_socket.bind((ip, port)) # Binding to given IP and port
        self.time = time
        self.logfile = open(logfile, "w+")

    def run(self):
        self.master_socket.listen(1) # Start listening to master
        while True:
            c, addr = self.master_socket.accept() # accepts master's connection
            msg = c.recv(1024).decode() # decodes message
            if msg == "request_time": # if master is requesting for time
                c.send(str(self.time)) # sends time
                self._log("TIME OF "+str(self.time)+" SENT TO MASTER")
            c.close()

    def _log(self, log):
        print log
        self.logfile.write(log)
