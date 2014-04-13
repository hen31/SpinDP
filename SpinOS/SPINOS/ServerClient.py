import threading

__author__ = 'Hendrik'


class ServerClient:

    def __init__(self, client_socket, adress):
        self.client_socket = client_socket
        self.adress = adress
        self.messages = list()
        self.mutex = threading.Semaphore(1)
        self.listen_thread = threading.Thread(target=self.run)
        self.listen_thread.start()

    def run(self):
        while True:
            for l in self.client_socket.makefile('r'):
                self.mutex.acquire()
                self.messages.append(l)
                self.mutex.release()


    def send_message(self, message):
        self.client_socket.send(message)

    def recieve_messages(self):
        self.mutex.acquire()
        messagescopy = self.messages[:]
        self.messages = []
        self.mutex.release()
        return messagescopy