
import platform
import socket
import threading
import time

from ServerClient import ServerClient
from Logger import Logger


__author__ = 'Hendrik'


class Server:


    #constuctor voor server
    def __init__(self, port, Log):
        self.portnumber = port
        self.s = socket.socket()  #Socket aanmaken
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if platform.system() == "Windows":
            self.host = socket.gethostname()  #lokale host gebruiken op windows
        else:
            self.host = "0.0.0.0"
        self.listen_thread = threading.Thread(target=self.run)
        self.log = Log
        self.clients = list()#Lijst van alle verbonden clients
        self.alive =True

    def startServer(self):
        self.s.bind((self.host, self.portnumber)) #naar poort luisteren
        self.s.listen(5)#maximaal aantal clients die wachten
        self.listen_thread.start()#thread om te luisteren naar nieuwe verbindingen
        self.log.logevent("Server", "started port " + str(self.portnumber) + " Host: " + str(self.host), Logger.MESSAGE)

    def run(self):
        while self.alive:
            time.sleep(0.2)
            try:
                c, addr = self.s.accept()  #Connectie met client maken
                self.log.logevent("Server", "Got connection from: " + str(addr), Logger.MESSAGE) #log bericht aanmaken
                clientobj = ServerClient(c, str(addr))#client object aanmaken
                self.clients.append(clientobj)#toevoegen aan lijst met verbonden clients
            except:
                pass


    #berichten van alle clients ophalen
    def get_messages(self):
        messages = list()
        for client in self.clients:
                messages = messages + client.recieve_messages()
        return messages
    #server stoppen, alle stream sluiten
    def stop(self):
        self.alive = False
        for c in self.clients:
            c.stop()
        self.s.close()
