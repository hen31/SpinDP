from TeerbalMode import TeerbalMode
from TeerbalVision import TeerbalVision
from MoveState import MoveState

import os
__author__ = 'Jeroen'


class SearchState:

    def __init__(self):
        #self.troll_jeroen()
        pass

    def doe_stap(self):
        nextState = MoveState()
        if TeerbalMode.alive:
            gevonden = TeerbalVision.find_teerbal(os.path.join(os.path.dirname(__file__) + "/TestImages",'1.jpg'))
            if gevonden:
                gecentreerd =  self.centreer()
                while not gecentreerd:
                    gecentreerd = self.centreer()
                nextState.doe_stap()


    def centreer(self):
        draai_graden = 5
        gecentreerd = False
        index = 0
        array = (os.path.join(os.path.dirname(__file__) + "/TestImages",'1.jpg'),os.path.join(os.path.dirname(__file__) + "/TestImages",'2.jpg'),os.path.join(os.path.dirname(__file__) + "/TestImages",'3.jpg'),os.path.join(os.path.dirname(__file__) + "/TestImages",'3found.jpg'),os.path.join(os.path.dirname(__file__) + "/TestImages",'5.jpg'))
        teerbal, rechts_draaien, links_draaien = TeerbalVision.center_on_teerbal(array[index])
        while index < len(array) and not gecentreerd:
            if teerbal:
                if rechts_draaien:
                    print "Draai rechts"
                elif links_draaien:
                    print "Draai links"
                elif not rechts_draaien and not links_draaien:
                    gecentreerd = True
                    TeerbalMode.logger.logevent("TeerbalMode SearchState", "Gecentreerd op de teerbal", TeerbalMode.logger.MESSAGE)
                    return True
            else:
                TeerbalMode.logger.logevent("TeerbalMode SearchState", "Teerbal verloren uit zicht", TeerbalMode.logger.MESSAGE)
                TeerbalVision.lost()
                draai_graden = draai_graden/2
            index+=1
            teerbal, rechts_draaien, links_draaien = TeerbalVision.center_on_teerbal(array[index])


        def troll_jeroen(self):
            print "Lorem Ipsum"