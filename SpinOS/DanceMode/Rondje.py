__author__ = 'Robert'

from DanceMode import DanceMode
import time

class Rondje:

    def __init__(self):
        pass

    def run(self):
        from Zwaaien import Zwaaien
        from PushUps import PushUps
        zwaaien = Zwaaien()

        for i in xrange(0, 3):
            DanceMode.movementHandler(0, 0, 181, 100)
            time.sleep(DanceMode.movementHandler.TIME_TURN_PER_DEGREE * 90)
            DanceMode.movementHandler(0, 0, 0, 0)

            zwaaien.run()

        DanceMode.movementHandler(0, 0, 181, 100)
        time.sleep(DanceMode.movementHandler.TIME_TURN_PER_DEGREE * 90)
        DanceMode.movementHandler(0, 0, 0, 0)

        pushUps = PushUps()
        pushUps.run()