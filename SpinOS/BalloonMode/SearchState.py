__author__ = 'Robert'

from BalloonMode import BalloonMode
from MoveState import MoveState
from Logger import Logger
from SimpleCV import *
from BalloonVision import BalloonVision


class SearchState:

    def __init__(self):
        self.colors = []
        self.balloonOrder = []
        self.moveTo = None #true = left, false = right

    def doe_stap(self, parameters):
        if BalloonMode.alive:
            self.colors = parameters[0]
            BalloonMode.logger.logevent("BalloonMode SearchState", "Ballonnen zoeken met de volgende volgorde",
                                        Logger.MESSAGE)
            BalloonMode.logger.logevent("BalloonMode SearchState", self.colors, Logger.MESSAGE)

            BalloonMode.logger.logevent("BalloonMode SearchState", "Volgorde ballonnen uit omgegving herkennen")

            self.balloonOrder = self.get_balloon_order()

            if not self.balloonOrder:
                return

            BalloonMode.logger.logevent("BalloonMode SearchState", "Volgorde van ballonnen uit de omgeving: " + self.balloonOrder[0] +" " + self.balloonOrder[1] +" " +self.balloonOrder[2])


            for i in xrange(0, 3):
                if i > 0: #De eerste ballon kan de spin al zien, niet nodig om te draaien dan.
                    if self.balloonOrder.index(self.colors[i-1]) > self.balloonOrder.index(self.colors[i]):
                        #Naar links draaien
                        self.moveTo = True
                        print "Naar links draaien"
                    else:
                        #Naar rechts draaien
                        self.moveTo = False
                        print "Naar rechts draaien"

                blob = self.find_balloon(self.colors[i])
                if blob is not False:
                    print self.colors[i] + " gevonden!"
                    moveState = MoveState()
                    moveState.doe_stap([self.colors[i], blob])

    def find_balloon(self, color):
        BalloonMode.logger.logevent("BalloonMode SearchState", "Zoeken naar ballon " + color, Logger.MESSAGE)

        img = BalloonVision.get_image()
        #img = Image("C:\\muur\\red.jpg")

        search = BalloonVision.find_balloon(color, img)

        while not search[0] and BalloonMode.alive:
            if self.moveTo:
                #TODO: beweeg 5 graden naar links
                pass
            elif not self.moveTo:
                #TODO: beweeg 5 graden naar rechts
                pass

            img = BalloonVision.get_image()
            search = BalloonVision.find_red_balloon(img)

        if not BalloonMode.alive:
            return False

        return search[1]

    def get_balloon_order(self):
        #Alle balonnen kunnen gezien worden
        img = BalloonVision.get_image()

        red = BalloonVision.find_red_balloon(img)[1]
        green = BalloonVision.find_green_balloon(img)[1]
        blue = BalloonVision.find_blue_balloon(img)[1]

        while (red is None or green is None or blue is None) and BalloonMode.alive:
            img = BalloonVision.get_image()
            red = BalloonVision.find_red_balloon(img)[1]
            green = BalloonVision.find_green_balloon(img)[1]
            blue = BalloonVision.find_blue_balloon(img)[1]

        if not BalloonMode.alive:
            return False

        red.Name = "red"
        green.Name = "green"
        blue.Name = "blue"

        balloonOrder = [red, green, blue]

        balloonOrder.sort(key=lambda x: x.x)

        balloonOrder = [self.balloonOrder[0].Name, self.balloonOrder[1].Name, self.balloonOrder[2].Name]

        return balloonOrder