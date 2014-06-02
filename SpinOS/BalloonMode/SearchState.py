__author__ = 'Robert'

from BalloonMode import BalloonMode
from MoveState import MoveState
from Logger import Logger
from BalloonVision import BalloonVision
import time

class SearchState:

    LOGGER_NAME = "BalloonMode SearchState"

    def __init__(self):
        self.colors = []
        self.balloonOrder = []
        self.moveTo = None #true = left, false = right

    def doe_stap(self, parameters):
        if BalloonMode.alive:
            self.colors = parameters[0]
            BalloonMode.logger.logevent(SearchState.LOGGER_NAME, "Ballonnen zoeken met de volgende volgorde",
                                        Logger.MESSAGE)
            BalloonMode.logger.logevent(SearchState.LOGGER_NAME, self.colors, Logger.MESSAGE)

            BalloonMode.logger.logevent(SearchState.LOGGER_NAME, "Volgorde ballonnen uit omgegving herkennen")

            self.balloonOrder = self.get_balloon_order()

            if not self.balloonOrder:
                return

            BalloonMode.logger.logevent(SearchState.LOGGER_NAME, "Volgorde van ballonnen uit de omgeving: " + self.balloonOrder[0] +" " + self.balloonOrder[1] +" " +self.balloonOrder[2])


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
                    BalloonMode.logger.logevent(SearchState.LOGGER_NAME, self.colors[i] + " gevonden!", Logger.MESSAGE)
                    moveState = MoveState()
                    moveState.doe_stap([self.colors[i], blob])

    def find_balloon(self, color):
        if not BalloonMode.alive:
            return False

        BalloonMode.logger.logevent(SearchState.LOGGER_NAME, "Zoeken naar ballon " + color, Logger.MESSAGE)

        img = BalloonVision.get_image()

        search = BalloonVision.find_balloon(color, img)

        while not search[0] and BalloonMode.alive:
            if self.moveTo:
                #TODO: beweeg 5 graden naar links
                BalloonMode.movementHandler.move(0, 0, 180, 100)
                time.sleep(BalloonMode.movementHandler.TIME_TURN_PER_DEGREE * 5)
                pass

            elif not self.moveTo:
                #TODO: beweeg 5 graden naar rechts
                BalloonMode.movementHandler.move(0, 0, 181, 100)
                time.sleep(BalloonMode.movementHandler.TIME_TURN_PER_DEGREE * 5)
                pass

            img = BalloonVision.get_image()
            search = BalloonVision.find_balloon(color, img)

        if not BalloonMode.alive:
            return False

        return search[1]

    def get_balloon_order(self):
        if not BalloonMode.alive:
            return False

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

        balloonOrder = [balloonOrder[0].Name, balloonOrder[1].Name, balloonOrder[2].Name]

        return balloonOrder