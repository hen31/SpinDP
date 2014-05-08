__author__ = 'Robert'

from BalloonMode import BalloonMode
from Logger import Logger
from SimpleCV import *

class SearchState:

    def __init__(self):
        self.colors = []
        self.current_color = 0

    def doe_stap(self, parameters):
        if BalloonMode.alive:
            self.colors = parameters[0]
            BalloonMode.logger.logevent("BalloonMode SearchState", "Ballonnen zoeken met de volgende volgorde", Logger.MESSAGE)
            BalloonMode.logger.logevent("BalloonMode SearchState", self.colors, Logger.MESSAGE)

            for i in xrange(0, 3):
                self.find_balloon(self.colors[i])


    def find_balloon(self, color):
        BalloonMode.logger.logevent("BalloonMode SearchState", "Zoeken naar ballon " + color, Logger.MESSAGE)

        img = Image("http://localhost:8080/?action=snapshot")
        #img = Image("C:\\balloon2.jpg")

        if color == "red":
            r = img.colorDistance(Color.RED).binarize(110)
            redBlobs = r.findBlobs()

            if redBlobs != None and len(redBlobs) > 0:
                found = True
            else:
                found = False

            while not found and BalloonMode.alive:
                #img = Image("http://localhost:8080/?action=snapshot")
                r = img.colorDistance(Color.RED).binarize(110)
                redBlobs = r.findBlobs()




        elif color == "green":
            g = img.hueDistance(Color.GREEN)
            greenBlobs = g.findBlobs()

        elif color == "blue":
            b = img.colorDistance(Color.BLUE).binarize(130)
            blueBlobs = b.findBlobs()
            blueBalloon = blueBlobs[len(blueBlobs) -1]

        return