__author__ = 'Robert'

from BalloonMode import BalloonMode

class MoveState:

    def __init__(self):
        pass

    def doe_stap(self, parameters):
        if BalloonMode.alive:
            self.move_to_balloon(parameters[0], parameters[1])
        return

    def move_to_balloon(self, color, blob):
        #loop naar de ballon
        
        return