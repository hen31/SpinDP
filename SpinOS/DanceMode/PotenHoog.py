__author__ = 'Robert'

from DanceMode import DanceMode
import time

class PotenHoog:
    #1 en 6 omhoog
    #2 en 5 omhoog
    #3 en 4 omhoog

    def __init(self):
        pass

    def run(self):
        # 1 en 6
        DanceMode.movementHandler.raise_leg(1)
        DanceMode.movementHandler.raise_leg(6)
        time.sleep(1)
        DanceMode.movementHandler.lower_leg(1)
        DanceMode.movementHandler.lower_leg(6)
        time.sleep(1)

        #2 en 6
        DanceMode.movementHandler.raise_leg(2)
        DanceMode.movementHandler.raise_leg(5)
        time.sleep(1)
        DanceMode.movementHandler.lower_leg(2)
        DanceMode.movementHandler.lower_leg(5)
        time.sleep(1)

        #3 en 4
        DanceMode.movementHandler.raise_leg(3)
        DanceMode.movementHandler.raise_leg(4)
        time.sleep(1)
        DanceMode.movementHandler.lower_leg(3)
        DanceMode.movementHandler.lower_leg(4)
        time.sleep(1)
