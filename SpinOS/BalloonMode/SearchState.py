__author__ = 'Robert'

from BalloonMode import BalloonMode
import SimpleCV
from Logger import Logger

class SearchState:

    def __init__(self):
        self.colors = []
        self.current_color = 0

    def doe_stap(self, parameters):
        if BalloonMode.alive:
            self.colors = parameters[0]
            BalloonMode.logger.logevent("BalloonMode SearchState", "Ballonnen zoeken met de volgende volgorde", Logger.MESSAGE)
            BalloonMode.logger.logevent("BalloonMode SearchState", self.colors, Logger.MESSAGE)

    def find_balloon(self):
        cam = SimpleCV.Camera()
        return