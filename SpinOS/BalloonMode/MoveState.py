__author__ = 'Robert'

from BalloonMode import BalloonMode
from BalloonVision import BalloonVision
from FoundState import FoundState
from Logger import Logger
import time


class MoveState:

    LOGGER_NAME = "BalloonMode MoveState"

    def __init__(self):
        pass

    def doe_stap(self, parameters):
        #parameters 0 = color, 1 = blob
        if BalloonMode.alive:
            move = self.move_to_balloon(parameters[0], parameters[1])

            if move is not False:
                foundState = FoundState()
                foundState.doe_stap([parameters[0]])
        return

    def move_to_balloon(self, color, blob):
        BalloonMode.logger.logevent(MoveState.LOGGER_NAME, "Naar ballon " + color + " lopen", Logger.MESSAGE)
        #Draaien zodat de ballon in het midden van de camera staat
        #Midden van het beeld
        center = 640 / 2

        move = self.move_balloon_to_center(blob, center, color)

        if not move:
            return False

        #loop naar de ballon
        BalloonMode.logger.logevent(MoveState.LOGGER_NAME, "Vooruit lopen", Logger.MESSAGE)

        #Max area = 640*480 = 307200
        area = 0
        not_found_count = 0

        #TODO: vooruit lopen
        BalloonMode.movementHandler.move(0, 100, 0, 0)
        time.sleep(BalloonMode.movementHandler.TIME_MOVE_ONE_CM * 10)
        BalloonMode.movementHandler.move(0, 0, 0, 0)

        while area < 20000 and BalloonMode.alive:
            if not_found_count >= 5:
                BalloonMode.logger.logevent(MoveState.LOGGER_NAME, color + " ballon kwijt, wat nu?!", Logger.MESSAGE)
                return False

            img = BalloonVision.get_image()
            search = BalloonVision.find_balloon(color, img, True)

            if search[0]:
                area = search[1].area()
                BalloonMode.movementHandler.move(0, 100, 0, 0)
                time.sleep(BalloonMode.movementHandler.TIME_MOVE_ONE_CM * 10)
                BalloonMode.movementHandler.move(0, 100, 0, 0)

            else:
                not_found_count += 1

        if not BalloonMode.alive:
            return False

        return True

    def move_balloon_to_center(self, blob, center, color):
        BalloonMode.logger.logevent(MoveState.LOGGER_NAME, "Ballon " + color + " naar het midden bewegen", Logger.MESSAGE)
        verschil = self.diff_to_center(blob, center)
        while abs(verschil) > 50 and BalloonMode.alive: #20 px marge voor het midden
            print "Blob nog niet in het midden"
            if verschil > 0:
                #5 graden naar links draaien
                BalloonMode.movementHandler(0, 0, 181, 100)
                time.sleep(BalloonMode.movementHandler.TIME_TURN_PER_DEGREE * 5)
                BalloonMode.movementHandler(0, 0, 0, 0)
            else:
                #5 graden naar rechts draaien
                BalloonMode.movementHandler(0, 0, 180, 100)
                time.sleep(BalloonMode.movementHandler.TIME_TURN_PER_DEGREE * 5)
                BalloonMode.movementHandler(0, 0, 0, 0)

            img = BalloonVision.get_image()
            search = BalloonVision.find_balloon(color, img)

            blob = search[1]

            if search[0]:
                verschil = self.diff_to_center(blob, center)

        if not BalloonMode.alive:
            return False

        return True

    def balloon_in_center(self, blob, center, marge):
        return abs(center - blob.centroid) > marge

    def diff_to_center(self, blob, center):
        return center - blob.x