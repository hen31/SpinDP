__author__ = 'Robert'

from BalloonMode import BalloonMode
from MoveState import MoveState
from Logger import Logger
from SimpleCV import *
from BalloonVision import BalloonVision


class SearchState:

    def __init__(self):
        self.colors = []
        self.current_color = 0

    def doe_stap(self, parameters):
        if BalloonMode.alive:
            self.colors = parameters[0]
            BalloonMode.logger.logevent("BalloonMode SearchState", "Ballonnen zoeken met de volgende volgorde",
                                        Logger.MESSAGE)
            BalloonMode.logger.logevent("BalloonMode SearchState", self.colors, Logger.MESSAGE)

            BalloonMode.logger.logevent("BalloonMode SearchState", "Volgorde ballonnen uit omgegving herkennen")


            for i in xrange(0, 3):
                blob = self.find_balloon(self.colors[i])
                if blob is not False:
                    print self.colors[i] + " gevonden!"
                    moveState = MoveState()
                    moveState.doe_stap([self.colors[i], blob])

            #img = Image("C:\\balloons\\redBalloon4.jpg")
            #self.find_red_balloon(img)



    def find_balloon(self, color):
        BalloonMode.logger.logevent("BalloonMode SearchState", "Zoeken naar ballon " + color, Logger.MESSAGE)

        img = Image("http://raspberrypi:8080/?action=snapshot")
        #img = Image("C:\\muur\\red.jpg")

        if color == "red":
            search = BalloonVision.find_red_balloon(img)

            while not search[0] and BalloonMode.alive:
                #Draai een beetje en neem een nieuwe foto
                #TODO: draaien
                img = Image("http://raspberrypi:8080/?action=snapshot")
                search = BalloonVision.find_red_balloon(img)

        elif color == "green":
            search = BalloonVision.find_green_balloon(img)

            while not search[0] and BalloonMode.alive:
                #Draai een beetje en neem een nieuwe foto
                img = Image("http://raspberrypi:8080/?action=snapshot")
                search = BalloonVision.find_green_balloon(img)

        elif color == "blue":
            search = BalloonVision.find_blue_balloon(img)

            while not search[0] and BalloonMode.alive:
                #Draai een beetje en neem een nieuwe foto
                img = Image("http://raspberrypi:8080/?action=snapshot")
                search = BalloonVision.find_blue_balloon(img)

        if not BalloonMode.alive:
            return False

        return search[1]