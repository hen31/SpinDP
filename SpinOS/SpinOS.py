import os
import threading
import sys
import time
from Command import COMMAND
from ManualMode import ManualMode
from Server import Server
from Logger import Logger
from SensorLogger import SensorLogger

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
        SpinOS.logger = Logger(Logger.MESSAGE)
        print("Logger level : " + SpinOS.logger.get_loglevel_string())
        #running op true zetten
        self.running = True
        #mode op manual zetten
        self.mode = "manual"
        #server aanmaken en starten
        self.server = Server(15, SpinOS.logger)
        self.server.startServer()
        self.current_mode = ManualMode()
        #main loop opstarten
        self.main_thread = threading.Thread(target=self.run)
        self.main_thread.start()

    def run(self):
        while self.running:
            time.sleep(0.2)
            message_list = self.server.get_messages()
            for message in message_list:
                self.logger.logevent("SPINOS", "Reading message - " + str(message))
                if message[0] == COMMAND.KILL:
                    self.running = False
                    self.shutdown()
                else:
                    command = message[0]
                    message.remove(0)
                    self.current_mode.process_command(command, message)

                #TODO act on message

    def shutdown(self):
        self.server.stop()
        os._exit(0)