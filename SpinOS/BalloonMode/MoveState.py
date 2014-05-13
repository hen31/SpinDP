__author__ = 'Robert'

from BalloonMode import BalloonMode
from FoundState import FoundState

class MoveState:

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
        #loop naar de ballon
        #lopen moet nog worden gemaakt
        print "Ik ga nu lopen. Maar dat kan ik nog niet :-("
        return True