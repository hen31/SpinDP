__author__ = 'Robert'

from BalloonVision import BalloonVision
from BalloonMode import BalloonMode
from Logger import Logger
from SimpleCV import *

#In de FoundState is de ballon gevonden en wordt er gewacht todat deze kapot gaat
class FoundState:

    LOGGER_NAME = "BalloonMode FoundState"

    def __init__(self):
        pass

    def doe_stap(self, parameters):
        #param 0 = color

        #Balloonmode nog wel alive
        if BalloonMode.alive:
            BalloonMode.logger.logevent(FoundState.LOGGER_NAME, "Vlak voor de ballon, kijken wanneer hij knapt " +parameters[0], Logger.MESSAGE)

            not_found_count = 0

            #aan
            #Leg 1
            leg1 = BalloonMode.movementHandler.legs[0]
            last1 = [leg1.get_hip(),leg1.get_height(),leg1.get_knee()]
            #Leg 4
            leg4 = BalloonMode.movementHandler.legs[3]
            last4 = [leg4.get_hip(),leg4.get_height(),leg4.get_knee()]


            #Not found count <= 2 en Balloonmode nog alive
            while not_found_count <= 2 and BalloonMode.alive:

                sensor1 = BalloonMode.serial.getSensor1()
                sensor2 = BalloonMode.serial.getSensor2()

                leg1.set_knee(sensor1)
                leg4.set_knee(sensor2)

                #Ballon nog gevonden?
                found = self.balloon_alive(parameters[0])
                if not found:
                    not_found_count += 1
                else:
                    not_found_count = 0

            if not BalloonMode.alive:
                return
            #uit poten resseten
            BalloonMode.logger.logevent(FoundState.LOGGER_NAME, "Balloon weg (geknapt)!", Logger.MESSAGE)

            leg1.set_knee(last1[2])
            leg4.set_knee(last4[2])

        return True

    #Methode die een ballon vind op basis van kleur
    def balloon_alive(self, color):
        #Afbeelding ophalen
        img = BalloonVision.get_image()

        #Blob vinden
        return BalloonVision.find_balloon(color, img, True)[0]