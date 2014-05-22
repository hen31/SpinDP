__author__ = 'Robert'

from BalloonVision import BalloonVision
from BalloonMode import BalloonMode
from Logger import Logger
from SimpleCV import *


class FoundState:

    LOGGER_NAME = "BalloonMode FoundState"

    def __init__(self):
        pass

    def doe_stap(self, parameters):
        #param 0 = color
        if BalloonMode.alive:
            BalloonMode.logger.logevent(FoundState.LOGGER_NAME, "Vlak voor de ballon, kijken wanneer hij knapt " +parameters[0], Logger.MESSAGE)

            not_found_count = 0

            while not_found_count <= 2 and BalloonMode.alive:
                found = self.balloon_alive(parameters[0])
                if not found:
                    not_found_count += 1
                else:
                    not_found_count = 0

            if not BalloonMode.alive:
                return

            BalloonMode.logger.logevent(FoundState.LOGGER_NAME, "Balloon weg (geknapt)!", Logger.MESSAGE)

        return True

    def balloon_alive(self, color):
        img = BalloonVision.get_image()

        return BalloonVision.find_balloon(color, img, True)[0]