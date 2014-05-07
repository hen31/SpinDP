import os
import platform
import threading
import sys
import time
from BalloonMode.BalloonMode import BalloonMode
from Command import COMMAND
from ManualMode import ManualMode
from MovementHandler import MovementHandler
from Server import Server
from Logger import Logger
from SensorLogger import SensorLogger
from TeerbalMode.TeerbalMode import TeerbalMode

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
        SpinOS.logger = Logger(Logger.SENSOR_VALUES)
        self.movementHandler = MovementHandler()
        print("Logger level : " + SpinOS.logger.get_loglevel_string())
        #running op true zetten
        self.running = True
        #mode op manual zetten
        self.mode = "manual"
        #server aanmaken en starten
        self.server = Server(15, SpinOS.logger)
        self.server.startServer()
        self.current_mode = ManualMode(self.movementHandler )
        #main loop opstarten
        self.main_thread = threading.Thread(target=self.run)
        self.main_thread.start()

        if platform.system() != "Windows":
            from MPU6050 import MPU6050
            self.MPU = MPU6050(SpinOS.logger)
            self.MPU.start()

    def run(self):
        while self.running:
            time.sleep(0.2)
            message_list = self.server.get_messages()
            for message in message_list:
                if message[0] == COMMAND.KILL:
                    self.logger.logevent("SPINOS", "KILLING SPIDER, OH NO!!!!!")
                    self.running = False
                    self.shutdown()
                elif message[0] == COMMAND.TO_MANUAL:
                    self.current_mode.alive = False
                    self.mode = "manual"
                    SpinOS.logger.logevent("SPINOS", "Mode set to " + self.mode, Logger.MESSAGE)
                    self.current_mode = ManualMode(self.movementHandler)
                    self.current_mode.alive = True
                elif message[0] == COMMAND.TO_BALLOON_MODE:
                    self.current_mode.alive = False
                    self.mode = "balloon mode"
                    SpinOS.logger.logevent("SPINOS", "Mode set to " + self.mode, Logger.MESSAGE)
                    self.current_mode = BalloonMode(self.logger)
                    self.current_mode.alive = True
                elif message[0] == COMMAND.TO_TEERBAL_MODE:
                    self.current_mode.alive = False
                    self.mode = "teerbal mode"
                    SpinOS.logger.logevent("SPINOS", "Mode set to " + self.mode, Logger.MESSAGE)
                    self.current_mode = TeerbalMode()
                    self.current_mode.alive = True
                else:
                    command = message[0]
                    message.remove(command)
                    self.current_mode.process_command(command, message)

                #TODO act on message

    def shutdown(self):
        self.server.stop()
                self.movementHandler.die()
        os._exit(0)