import socket
import sys
import re

class Client:

    def __init__(self, addr, time, logfile):
        ip_port = re.split(":", addr)
        # the slaves's listening ip
        ip = ip_port[0]
        # the slaves's listening port
        port = int(ip_port[1])
        # creating socket that can both receive and send packages
        self.master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.master_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # binding to given ip and port
        self.master_socket.bind((ip, port))
        self.time = time
        # opening logfile
        self.logfile = open(logfile, "w+")

    # starts slave's time update
    def run(self):
        # listening to master
        self.master_socket.listen(1)
        while True:
            # accepts master's connection
            c, addr = self.master_socket.accept()
            # receives and decodes message
            msg = c.recv(1024).decode()
            # if master is requesting for time
            if msg == "request_time":
                # sends current time
                c.send(str(self.time))
                self._log("TIME OF "+str(self.time)+" SENT TO MASTER")
            else: # if not
                # master is providing average to update this slave instance
                # and so, we split the message in order to get the time
                avg = int(re.split(":", msg)[1])
                # updating time in user
                self.time += avg
                # self._log("TIME UPDATED TO "+str(self.time))
                self._log("UPDATE RECEIVED "+str(avg))
            # closes connection to master
            c.close()

    # logs both to command prompt and to logfile
    def _log(self, log):
        print log
        self.logfile.write(log + "\n")
