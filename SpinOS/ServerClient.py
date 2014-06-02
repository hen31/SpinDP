import threading
import time
from Command import COMMAND

__author__ = 'Hendrik'


class ServerClient:
    UNKNOWN = 0
    ANDROID_DASHBOARD = 1
    ANDROID_CONTROLLER = 2
    GAMEPAD_CONTROLLER = 3

    def __init__(self, client_socket, adress):
        self.client_socket = client_socket
        self.adress = adress
        self.messages = list()
        self.mutex = threading.Semaphore(1)
        self.alive = True
        self.type = ServerClient.UNKNOWN
        self.listen_thread = threading.Thread(target=self.run)
        self.listen_thread.start()

    def run(self):
        while self.alive:
            time.sleep(0.2)
            f = self.client_socket.makefile()
            #print("file made")
            l = f.readline()
            l = l.replace("\n", "")
            command_recieved = COMMAND.decode_message(l)
            self.mutex.acquire()
            self.messages.append([self] + command_recieved)
            self.mutex.release()
            self.send_message(COMMAND.encode_message(COMMAND.RECIEVED, [command_recieved[0]]))

    def send_message(self, message):
        try:
            self.client_socket.send(message)
        except:
            a=0

    def recieve_messages(self):
        self.mutex.acquire()
        messagescopy = self.messages[:]
        self.messages = []
        self.mutex.release()
        return messagescopy

    def stop(self):
        self.alive = False