__author__ = 'Robert'


from BalloonVision import BalloonVision
from FoundState import FoundState
from Logger import Logger
import time


class MoveState:

    LOGGER_NAME = "self.balloonmode MoveState"

    def __init__(self, ballonmode):
        self.self.balloonmode = ballonmode
        pass

    def doe_stap(self, parameters):
        #parameters 0 = color, 1 = blob
        if self.balloonmode.alive:
            move = self.move_to_balloon(parameters[0], parameters[1])

            if move is not False:
                foundState = FoundState(self.balloonmode)
                foundState.doe_stap([parameters[0]])
        return

    def move_to_balloon(self, color, blob):
        self.balloonmode.logger.logevent(MoveState.LOGGER_NAME, "Naar ballon " + color + " lopen", Logger.MESSAGE)
        #Draaien zodat de ballon in het midden van de camera staat
        #Midden van het beeld
        center = 640 / 2

        move = self.move_balloon_to_center(blob, center, color)

        if not move:
            return False

        #loop naar de ballon
        self.balloonmode.logger.logevent(MoveState.LOGGER_NAME, "Vooruit lopen", Logger.MESSAGE)

        #Max area = 640*480 = 307200
        area = 0
        not_found_count = 0

        #vooruit lopen
        self.balloonmode.movementHandler.move(0, 100, 0, 0)
        time.sleep(self.balloonmode.movementHandler.TIME_MOVE_ONE_CM * 10)
        self.balloonmode.movementHandler.move(0, 0, 0, 0)

        while area < 20000 and self.balloonmode.alive:
            if not_found_count >= 5:
                self.balloonmode.logger.logevent(MoveState.LOGGER_NAME, color + " ballon kwijt, wat nu?!", Logger.MESSAGE)
                return False

            img = BalloonVision.get_image()
            search = BalloonVision.find_balloon(color, img, True)

            if search[0]:
                area = search[1].area()
                self.balloonmode.movementHandler.move(0, 100, 0, 0)
                time.sleep(self.balloonmode.movementHandler.TIME_MOVE_ONE_CM * 10)
                self.balloonmode.movementHandler.move(0, 100, 0, 0)

            else:
                not_found_count += 1

        if not self.balloonmode.alive:
            return False

        return True

    def move_balloon_to_center(self, blob, center, color):
        self.balloonmode.logger.logevent(MoveState.LOGGER_NAME, "Ballon " + color + " naar het midden bewegen", Logger.MESSAGE)
        verschil = self.diff_to_center(blob, center)
        while abs(verschil) > 50 and self.balloonmode.alive: #20 px marge voor het midden
            print "Blob nog niet in het midden"
            if verschil > 0:
                #5 graden naar links draaien
                self.balloonmode.movementHandler(0, 0, 181, 100)
                time.sleep(self.balloonmode.movementHandler.TIME_TURN_PER_DEGREE * 5)
                self.balloonmode.movementHandler(0, 0, 0, 0)
            else:
                #5 graden naar rechts draaien
                self.balloonmode.movementHandler(0, 0, 180, 100)
                time.sleep(self.balloonmode.movementHandler.TIME_TURN_PER_DEGREE * 5)
                self.balloonmode.movementHandler(0, 0, 0, 0)

            img = BalloonVision.get_image()
            search = BalloonVision.find_balloon(color, img)

            blob = search[1]

            if search[0]:
                verschil = self.diff_to_center(blob, center)

        if not self.balloonmode.alive:
            return False

        return True

    def balloon_in_center(self, blob, center, marge):
        return abs(center - blob.centroid) > marge

    def diff_to_center(self, blob, center):
        return center - blob.x