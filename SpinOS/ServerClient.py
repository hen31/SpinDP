import threading
from Command import COMMAND

__author__ = 'Hendrik'


class ServerClient:
    def __init__(self, client_socket, adress):
        self.client_socket = client_socket
        self.adress = adress
        self.messages = list()
        self.mutex = threading.Semaphore(1)
        self.alive = True
        self.listen_thread = threading.Thread(target=self.run)
        self.listen_thread.start()

    def run(self):
        while self.alive:
            for l in self.client_socket.makefile('r'):
                l = l.replace("\n", "")
                self.mutex.acquire()
                self.messages.append(COMMAND.decode_message(l))
                self.mutex.release()

    def send_message(self, message):
        self.client_socket.send(message)

    def recieve_messages(self):
        self.mutex.acquire()
        messagescopy = self.messages[:]
        self.messages = []
        self.mutex.release()
        return messagescopy

    def stop(self):
        self.alive = False