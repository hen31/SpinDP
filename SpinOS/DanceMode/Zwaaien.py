__author__ = 'Robert'

from DanceMode import DanceMode
import time

class Zwaaien:

    def __init__(self):
        pass

    def run(self):
        #Alleen nog poot 1, twee poten kunnen we pas testen als er een spin is

        #Poot vooruit / omhoog
        DanceMode.movementHandler.legs[0].set_knee(0)
        time.sleep(0.5)
        DanceMode.movementHandler.legs[0].set_height(0)


        #Heen en weer bewegen
        for x in xrange(20, 160):
            DanceMode.movementHandler.legs[0].set_hip(x)

        for x in xrange(160, 20):
            DanceMode.movementHandler.legs[0].set_hip(x)


