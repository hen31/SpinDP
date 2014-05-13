__author__ = 'Robert'

from BalloonVision import BalloonVision
from BalloonMode import BalloonMode
from Logger import Logger
from SimpleCV import *

class FoundState:

    def __init__(self):
        pass

    def doe_stap(self, parameters):
        if BalloonMode.alive:
            BalloonMode.logger.logevent("BalloonMode FoundState", "Kijken wanneer de ballon dood gaat " +parameters[0], Logger.MESSAGE)

            found = self.find_balloon(parameters[0])

            while found is True and BalloonMode.alive:
                found = self.find_balloon(parameters[0])

            if not BalloonMode.alive:
                return

            BalloonMode.logger.logevent("BalloonMode FoundState", "Balloon weg (geknapt)!", Logger.MESSAGE)



        return

    def find_balloon(self, color):
        from SearchState import SearchState
        img = Image("http://raspberrypi:8080/?action=snapshot")

        if color == "red":
            return BalloonVision.find_red_balloon(img)[0]
        elif color == "green":
            return BalloonVision.find_green_balloon(img)[0]
        elif color == "blue":
            return BalloonVision.find_blue_balloon(img)[0]