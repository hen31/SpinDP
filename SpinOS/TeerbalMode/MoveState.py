from TeerbalMode import TeerbalMode
from TeerbalVision import TeerbalVision
import os

__author__ = 'Jeroen'

class MoveState:


    def __init__(self):
        pass

    def doe_stap(self):
        if TeerbalMode.alive:
            found,verdwenen,gecentreerd = TeerbalVision.isCentrated(os.path.join(os.path.dirname(__file__) + "/TestImages",'3.jpg'))
            while TeerbalMode.alive and not found:
                print found
                if gecentreerd:
                    self.walk_forward()
                else:
                    #True = links draaien, False = rechts draaien
                    kant_draaien = TeerbalVision.lost()
                    if kant_draaien:
                        print "Draai terug naar links"
                    else:
                        print "Draai terug naar rechts"
                found,verdwenen,gecentreerd = TeerbalVision.isCentrated(os.path.join(os.path.dirname(__file__) + "/TestImages",'3found.jpg'))
                print found
            if TeerbalMode.alive and verdwenen:
                #als de teerbal is verdwenen na het lopen kijken of hij onder in de foto met een kleinere area nog te vinden is
                pass



    def walk_forward(self):
        pass












