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
from ServerClient import ServerClient
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
        SpinOS.logger = Logger(Logger.SENSOR_VALUES)
        print("Logger level : " + SpinOS.logger.get_loglevel_string())


        #logger aanmaken

        self.movementHandler = MovementHandler()
        self.server = Server(15, SpinOS.logger)
        self.server.startServer()
        SpinOS.logger.set_server(self.server)
        #running op true zetten
        self.running = True
        #mode op manual zetten
        self.mode = "manual"
        #server aanmaken en starten

        self.current_mode = ManualMode(self.movementHandler, self.logger)
        #main loop opstarten
        self.main_thread = threading.Thread(target=self.run)
        self.main_thread.start()

        #if platform.system() != "Windows":
        #    from MPU6050 import MPU6050
        #    self.MPU = MPU6050(SpinOS.logger)
        #    self.MPU.start()

    def run(self):
        try:
            while self.running:
                time.sleep(0.2)
                message_list = self.server.get_messages()
                for message in message_list:
                    client = message[0]
                    message.remove(client)
                    if message[0] == COMMAND.IDENTIFY:
                        if message[1] == "dashboard":
                            client.type = ServerClient.ANDROID_DASHBOARD
                            self.logger.logevent("SPINOS", "Connected - ANDROID_DASHBOARD", Logger.MESSAGE)
                        elif message[1] == "controller":
                            client.type = ServerClient.ANDROID_CONTROLLER
                            self.logger.logevent("SPINOS", "Connected - ANDROID_CONTROLLER", Logger.MESSAGE)
                        elif message[1] == "gamepad":
                            client.type = ServerClient.GAMEPAD_CONTROLLER
                            self.logger.logevent("SPINOS", "Connected - GAMEPAD_CONTROLLER", Logger.MESSAGE)
                        else:
                            client.type = ServerClient.UNKNOWN
                            self.logger.logevent("SPINOS", "Connected - UNKNOWN", Logger.WARNING)
                    elif message[0] == COMMAND.KILL:
                        self.logger.logevent("SPINOS", "KILLING SPIDER, OH NO!!!!!")
                        self.running = False
                        self.shutdown()
                    elif message[0] == COMMAND.TO_MANUAL:
                        self.current_mode.set_alive(False)
                        self.mode = "manual"
                        SpinOS.logger.logevent("SPINOS", "Mode set to " + self.mode, Logger.MESSAGE)
                        self.current_mode = ManualMode(self.movementHandler, self.logger)
                        self.current_mode.alive = True
                    elif message[0] == COMMAND.TO_BALLOON_MODE:
                        self.current_mode.set_alive(False)
                        self.mode = "balloon mode"
                        SpinOS.logger.logevent("SPINOS", "Mode set to " + self.mode, Logger.MESSAGE)
                        self.current_mode = BalloonMode(self.logger)
                        self.current_mode.alive = True
                    elif message[0] == COMMAND.TO_TEERBAL_MODE:
                        self.current_mode.set_alive(False)
                        self.mode = "teerbal mode"
                        SpinOS.logger.logevent("SPINOS", "Mode set to " + self.mode, Logger.MESSAGE)
                        self.current_mode = TeerbalMode()
                        self.current_mode.alive = True

                    elif message[0] == COMMAND.SEND_SENSOR_DATA:
                        data = "h1:10, h2:5<;>h1:9, h2:5<;>h1:8, h2:9<;>h1:3,h2:10"
                        encoded = COMMAND.encode_message(COMMAND.SEND_SENSOR_DATA, data)
                        client.send_message(encoded)

                    elif message[0] == COMMAND.SEND_ACCU_DATA:
                        data = "100<;>100<;>100<;>100<;>100<;>100<;>100<;>100<;>100<;>99<;>99<;>99<;>70<;>60<;>50"
                        encoded = COMMAND.encode_message(COMMAND.SEND_ACCU_DATA, data)
                        client.send_message(encoded)

                    else:
                        command = message[0]
                        message.remove(command)
                        self.current_mode.process_command(command, message)

        except:
            self.shutdown()

                #TODO act on message

    def shutdown(self):
        self.server.stop()
        self.movementHandler.die()
        os._exit(0)