import threading
import sys
from SPINOS import Server
from SPINOS import Logger
from SPINOS.SensorLogger import SensorLogger

__author__ = 'Hendrik'


class SpinOS:

    logger = None
#cam = SimpleCV.Camera(prop_set={"width": 300, "height": 300})

#img = cam.getImage()
    def __init__(self):
        print("SpinOS 0.1")
        print("Group 5 IDP 2014 NHL")
        print("Default string encoding : " + str(sys.getdefaultencoding()).upper())
        #logger aanmaken
        SpinOS.logger = Logger.Logger(Logger.Logger.MESSAGE)
        print("Logger level : " + SpinOS.logger.get_loglevel_string())
        #running op true zetten
        self.running = True
        #mode op manual zetten
        self.mode = "manual"
        #server aanmaken en starten
        self.server = Server.Server(15, SpinOS.logger)
        self.server.startServer()
        #main loop opstarten
        self.main_thread = threading.Thread(target=self.run)
        self.main_thread.start()

    def run(self):
        while self.running:
            message_list = self.server.get_messages()
            for message in message_list:
                self.logger.logevent("SPINOS", "Reading message - " + str(message))
                #TODO act on message

