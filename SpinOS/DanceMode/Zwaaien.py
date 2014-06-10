__author__ = 'Robert'

import time

class Zwaaien:

    movementHandler = None

    def __init__(self, movementhandler):
        self.movementHandler = movementhandler

    def run(self):
        #Alleen nog poot 1, twee poten kunnen we pas testen als er een spin is

        #Poot vooruit / omhoog
        self.movementHandler.legs[0].set_knee(0)
        time.sleep(0.5)
        self.movementHandler.legs[0].set_height(0)


        #Heen en weer bewegen
        for x in xrange(20, 160):
            self.movementHandler.legs[0].set_hip(x)

        for x in xrange(160, 20):
            self.movementHandler.legs[0].set_hip(x)


