__author__ = 'Robert'

import time

class Rondje:

    movementHandler = None

    def __init__(self, movementhandler):
        self.movementHandler = movementhandler

    def run(self):
        from Zwaaien import Zwaaien
        from PushUps import PushUps
        zwaaien = Zwaaien()

        for i in xrange(0, 3):
            self.movementHandler(0, 0, 181, 100)
            time.sleep(self.movementHandler.TIME_TURN_PER_DEGREE * 90)
            self.movementHandler(0, 0, 0, 0)

            zwaaien.run()

        self.movementHandler(0, 0, 181, 100)
        time.sleep(self.movementHandler.TIME_TURN_PER_DEGREE * 90)
        self.movementHandler(0, 0, 0, 0)

        pushUps = PushUps()
        pushUps.run()