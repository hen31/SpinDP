from DanceMode import DanceMode
import time

__author__ = 'Robert'


class Wippen:

    def __init__(self):
        pass

    def run(self):
        for x in range(0,4):
            DanceMode.movementHandler.raise_leg(DanceMode.movementHandler.legs[0])
            DanceMode.movementHandler.raise_leg(DanceMode.movementHandler.legs[3])
            DanceMode.movementHandler.lower_leg(DanceMode.movementHandler.legs[2])
            DanceMode.movementHandler.lower_leg(DanceMode.movementHandler.legs[5])
            time.sleep(1)
            DanceMode.movementHandler.raise_leg(DanceMode.movementHandler.legs[2])
            DanceMode.movementHandler.raise_leg(DanceMode.movementHandler.legs[5])
            DanceMode.movementHandler.lower_leg(DanceMode.movementHandler.legs[0])
            DanceMode.movementHandler.lower_leg(DanceMode.movementHandler.legs[3])
            time.sleep(1)