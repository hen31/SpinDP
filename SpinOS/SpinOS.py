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
from DanceMode import DanceMode
import RPi.GPIO as GPIO

__author__ = 'Hendrik'





class SpinOS:

    logger = None
    def __init__(self):
        print("SpinOS 0.2")
        print("Group 5 IDP 2014 NHL")
        print("Default string encoding : " + str(sys.getdefaultencoding()).upper())
        SpinOS.logger = Logger(Logger.SENSOR_VALUES)
        print("Logger level : " + SpinOS.logger.get_loglevel_string())

        GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
        GPIO.setup(11, GPIO.OUT)


        #logger aanmaken
        self.movementHandler = MovementHandler()

        #server maken op poort 15, omdat ie vrij is
        self.server = Server(15, SpinOS.logger)
        #server starten
        self.server.startServer()
        #server aan logger geven
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

        #Check of we op de raspberry pi zitten
        if platform.system() != "Windows":
            #import mpu
            from MPU6050 import MPU6050
            self.MPU = MPU6050(SpinOS.logger)
            #import os.path om te kijken of de arduino er is
            import os.path
            self.serial_device = None
            #loop door verschillende usb devices. De naam veranderd namelijk soms
            for i in xrange(0, 3):
                #de naam van de usb
                serial_device = "/dev/ttyUSB" + str(i)
                #kijk of de usb er is
                if os.path.exists(serial_device):
                    #als de arduino er is moeten we serial importen
                    from Serial import Serial
                    #maak een nieuwe serial
                    self.serial = Serial(SpinOS.logger, serial_device)
                    #sla de naam van de arduino op
                    self.serial_device = serial_device
                    break
            #start de sensor thread
            self.sensor_running = True
            self.sensor_thread = threading.Thread(target=self.runSensors())
            self.sensor_thread.start()

    @staticmethod
    def play_sound(time):
        GPIO.output(11,True)
        time.sleep(time)
        GPIO.output(11,False)
        GPIO.cleanup()

    #run methode, deze loopt in eigen thread en halen de commando's op
    def run(self):
        try:
            while self.running:
                time.sleep(0.2)
                message_list = self.server.get_messages()#berichten ophalen van serverclients
                for message in message_list:
                    client = message[0]#client is eerste in lijst
                    message.remove(client)#verwijderen uit lijst
                    if message[0] == COMMAND.IDENTIFY:#if en elsif om te achterhalen welk commando is gegeven
                        #kijken welk apparaat connect
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
                        #spider wordt uitegezet alle threads worden gestopt
                        self.logger.logevent("SPINOS", "KILLING SPIDER, OH NO!!!!!")
                        self.running = False
                        self.shutdown()
                    elif message[0] == COMMAND.TO_MANUAL:
                        #huidige mode alive false zodat threads stoppen
                        self.current_mode.set_alive(False)
                        self.mode = "manual"
                        #set mode naar manual besturing
                        SpinOS.logger.logevent("SPINOS", "Mode set to " + self.mode, Logger.MESSAGE)
                        self.current_mode = ManualMode(self.movementHandler, self.logger)
                        self.current_mode.alive = True
                    elif message[0] == COMMAND.TO_BALLOON_MODE:
                        #huidige mode alive false zodat threads stoppen
                        self.current_mode.set_alive(False)
                        self.mode = "balloon mode"
                        #set mode naar balloon mode
                        SpinOS.logger.logevent("SPINOS", "Mode set to " + self.mode, Logger.MESSAGE)
                        self.current_mode = BalloonMode(self.movementHandler, self.logger, self.serial)
                        self.current_mode.alive = True
                    elif message[0] == COMMAND.TO_TEERBAL_MODE:
                        #huidige mode alive false zodat threads stoppen
                        self.current_mode.set_alive(False)
                        self.mode = "teerbal mode"
                        #mode naar teerbal zetten
                        SpinOS.logger.logevent("SPINOS", "Mode set to " + self.mode, Logger.MESSAGE)
                        self.current_mode = TeerbalMode()
                        self.current_mode.alive = True
                    elif message[0] == COMMAND.TO_DANCE_MODE:
                        #huidige mode alive false zodat threads stoppen
                        self.current_mode.set_alive(False)
                        self.mode = "dance mode"
                        #dance mode aanzetten
                        SpinOS.logger.logevent("SPINOS", "Mode set to " + self.mode, Logger.MESSAGE)
                        self.current_mode = DanceMode(self.movementHandler, self.logger)
                        self.current_mode.set_alive(True)

                    elif message[0] == COMMAND.SEND_SENSOR_DATA:
                        data = self.MPU.sensorlogger.get_log()
                        encoded = COMMAND.encode_message(COMMAND.SEND_SENSOR_DATA, data)
                        client.send_message(encoded)

                    elif message[0] == COMMAND.SEND_ACCU_DATA:
                        data = self.serial.voltagelogger.get_log()
                        encoded = COMMAND.encode_message(COMMAND.SEND_ACCU_DATA, data)
                        client.send_message(encoded)

                    else:
                        command = message[0]
                        message.remove(command)
                        self.current_mode.process_command(command, message)

        except:
            self.shutdown()#als er een exception optreedt wordt de spin gedood

    #loop voor het ophalen van sensor waarden
    def runSensors(self):
        while self.sensor_running and self.running:
            if self.MPU:
                #haal de waarde op van de MPU6050
                self.MPU.getValues()
            if self.serial_device:
                #haal de waardes op van de arduino
                self.serial.getValues()
            time.sleep(0.3)
            
    #alle threads stoppen
    def shutdown(self):
        self.server.stop()
        self.movementHandler.die()
        os._exit(0)
