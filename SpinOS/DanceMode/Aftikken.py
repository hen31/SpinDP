from DanceMode import DanceMode
import time
__author__ = 'Robert'


class Aftikken:

    def __init(self):
        pass

    def run(self):
        for x in range(0, 4):
            hip = DanceMode.movementHandler.legs[0].get_heigt()
            DanceMode.movementHandler.legs[0].set_heigt(hip-20)
            time.sleep(1)
            DanceMode.movementHandler.legs[0].set_heigt(hip)
            time.sleep(1)