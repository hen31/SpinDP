import socket
import threading
from Logger import Logger
from SPINOS.ServerClient import ServerClient


__author__ = 'Hendrik'


class Server:
    portnumber = 10


    def __init__(self, port, Log):
        self.portnumber = port
        self.s = socket.socket()  # Create a socket object
        self.host = socket.gethostname()  # Get local machine name
        self.listen_thread = threading.Thread(target=self.run)
        self.log = Log
        self.clients = list()#list of all connected clients

    def startServer(self):
        self.s.bind((self.host, self.portnumber))  # Bind to the port
        self.s.listen(5)#max number of waiting clients
        self.listen_thread.start()#thread to listen to new clients
        self.log.logevent("Server", "started port " + str(self.portnumber) + " Host: " + str(self.host), Logger.MESSAGE)

    def run(self):
        while True:
            c, addr = self.s.accept()  # Establish connection with client.
            self.log.logevent("Server", "Got connection from: " + str(addr), Logger.MESSAGE)
            clientobj = ServerClient(c, str(addr))#create client object
            self.clients.append(clientobj)

    def get_messages(self):
        messages = list()
        for client in self.clients:
                messages = messages + client.recieve_messages()
        return messages