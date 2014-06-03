__author__ = 'Robert'

from MoveState import MoveState
from Logger import Logger
from BalloonVision import BalloonVision
import time

class SearchState:

    LOGGER_NAME = "BalloonMode SearchState"

    def __init__(self, ballonmode):
        self.balloonmode= ballonmode
        self.colors = []
        self.balloonOrder = []
        self.moveTo = None #true = left, false = right

    def doe_stap(self, parameters):
        if self.balloonmode.alive:
            self.colors = parameters[0]
            self.balloonmode.logger.logevent(SearchState.LOGGER_NAME, "Ballonnen zoeken met de volgende volgorde",
                                        Logger.MESSAGE)
            self.balloonmode.logger.logevent(SearchState.LOGGER_NAME, self.colors, Logger.MESSAGE)

            self.balloonmode.logger.logevent(SearchState.LOGGER_NAME, "Volgorde ballonnen uit omgegving herkennen")

            self.balloonOrder = self.get_balloon_order()

            if not self.balloonOrder:
                return

            self.balloonmode.logger.logevent(SearchState.LOGGER_NAME, "Volgorde van ballonnen uit de omgeving: " + self.balloonOrder[0] +" " + self.balloonOrder[1] +" " +self.balloonOrder[2])


            for i in xrange(0, 3):
                if i > 0: #De eerste ballon kan de spin al zien, niet nodig om te draaien dan.
                    if self.balloonOrder.index(self.colors[i-1]) > self.balloonOrder.index(self.colors[i]):
                        #Naar links draaien
                        self.moveTo = True
                    else:
                        #Naar rechts draaien
                        self.moveTo = False

                blob = self.find_balloon(self.colors[i])
                if blob is not False:
                    self.balloonmode.logger.logevent(SearchState.LOGGER_NAME, self.colors[i] + " gevonden!", Logger.MESSAGE)
                    moveState = MoveState(self.balloonmode)
                    moveState.doe_stap([self.colors[i], blob])

    def find_balloon(self, color):
        if not self.balloonmode.alive:
            return False

        self.balloonmode.logger.logevent(SearchState.LOGGER_NAME, "Zoeken naar ballon " + color, Logger.MESSAGE)

        img = BalloonVision.get_image()

        search = BalloonVision.find_balloon(color, img)

        while not search[0] and self.balloonmode.alive:
            if self.moveTo:
                #TODO: beweeg 5 graden naar links
                self.balloonmode.movementHandler.move(0, 0, 180, 100)
                time.sleep(self.balloonmode.movementHandler.TIME_TURN_PER_DEGREE * 5)
                pass

            elif not self.moveTo:
                #TODO: beweeg 5 graden naar rechts
                self.balloonmode.movementHandler.move(0, 0, 181, 100)
                time.sleep(self.balloonmode.movementHandler.TIME_TURN_PER_DEGREE * 5)
                pass

            img = BalloonVision.get_image()
            search = BalloonVision.find_balloon(color, img)

        if not self.balloonmode.alive:
            return False

        return search[1]

    def get_balloon_order(self):
        if not self.balloonmode.alive:
            return False

        #Alle balonnen kunnen gezien worden
        img = BalloonVision.get_image()

        red = BalloonVision.find_red_balloon(img)[1]
        green = BalloonVision.find_green_balloon(img)[1]
        blue = BalloonVision.find_blue_balloon(img)[1]

        while (red is None or green is None or blue is None) and self.balloonmode.alive:
            img = BalloonVision.get_image()
            red = BalloonVision.find_red_balloon(img)[1]
            green = BalloonVision.find_green_balloon(img)[1]
            blue = BalloonVision.find_blue_balloon(img)[1]

        if not self.balloonmode.alive:
            return False

        red.Name = "red"
        green.Name = "green"
        blue.Name = "blue"

        balloonOrder = [red, green, blue]

        balloonOrder.sort(key=lambda x: x.x)

        balloonOrder = [balloonOrder[0].Name, balloonOrder[1].Name, balloonOrder[2].Name]

        return balloonOrder