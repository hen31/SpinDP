import threading
from SPINOS import Server
from SPINOS import Logger

__author__ = 'Hendrik'


class SpinOS:
#cam = SimpleCV.Camera(prop_set={"width": 300, "height": 300})

#img = cam.getImage()
    def __init__(self):
        print("SpinOS 0.1")
        print("Group 5 IDP 2014 NHL")
        self.logger = Logger.Logger(Logger.Logger.MESSAGE)
        self.running = True
        self.mode = "manual"
        self.server = Server.Server(15, self.logger)
        self.server.startServer()
        self.main_thread = threading.Thread(target=self.run)
        self.main_thread.start()


    def run(self):
        while self.running:
            message_list = self.server.get_messages()
            for message in message_list:
                self.logger.logevent("SPINOS", "Reading message - " + message)
                #TODO act on message

