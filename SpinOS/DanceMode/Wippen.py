import time

__author__ = 'Robert'


class Wippen:

    movementHandler = None

    def __init__(self, movementhandler):
        self.movementHandler = movementhandler

    def run(self):
        for x in range(0,4):
            self.movementHandler.raise_leg(self.movementHandler.legs[0])
            self.movementHandler.raise_leg(self.movementHandler.legs[3])
            self.movementHandler.lower_leg(self.movementHandler.legs[2])
            self.movementHandler.lower_leg(self.movementHandler.legs[5])
            time.sleep(1)
            self.movementHandler.raise_leg(self.movementHandler.legs[2])
            self.movementHandler.raise_leg(self.movementHandler.legs[5])
            self.movementHandler.lower_leg(self.movementHandler.legs[0])
            self.movementHandler.lower_leg(self.movementHandler.legs[3])
            time.sleep(1)