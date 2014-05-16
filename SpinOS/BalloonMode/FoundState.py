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
        img = BalloonVision.get_image()

        return BalloonVision.find_balloon(color, img, True)