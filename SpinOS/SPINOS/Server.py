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
        self.Log = Log
        self.clients = list()

    def startServer(self):
        self.s.bind((self.host, self.portnumber))  # Bind to the port
        self.s.listen(5)
        self.listen_thread.start()
        self.Log.logevent("Server", "started port " + str(self.portnumber) + " Host: " + str(self.host), Logger.MESSAGE)

    def run(self):
        while True:
            c, addr = self.s.accept()  # Establish connection with client.
            self.Log.logevent("Server", "Got connection from: " + str(addr), Logger.MESSAGE)
            clientObj = ServerClient(c, str(addr))
            self.clients.append(clientObj)

    def get_messages(self):
        messages = list()
        for client in self.clients:
                messages = messages + client.recieve_messages()
        return messages