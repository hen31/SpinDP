import threading
from TeerbalVision import TeerbalVision
import time


__author__ = 'Jeroen'


class TeerbalMode:

    alive = True
    logger = None
    movementHandler = None
    spinOS = None


    def __init__(self,movementHandler, logger, spinOS):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        TeerbalMode.logger = logger
        TeerbalMode.movementHandler = movementHandler
        TeerbalMode.spinOS = spinOS


    def run(self):

        state = SearchState()
        state.doe_stap()


    def set_alive(self, bool):
        TeerbalMode.alive = bool


class SearchState:

    STATE = "TeerbalMode SearchState"

    def __init__(self):
        pass

    def doe_stap(self):
        nextState = MoveState()
        if TeerbalMode.alive:

            gevonden = TeerbalVision.find_teerbal(TeerbalVision.find_teerbal(TeerbalVision.getImage()))
            while not gevonden:
                TeerbalMode.logger.logevent(self.STATE,"Geen teelbal gevonden, nu draaien",TeerbalMode.logger.MESSAGE)
                #draai x graden naar rechts
                TeerbalMode.movementHandler.move(0,0,180,100)
                time.sleep(TeerbalMode.movementHandler.TIME_TURN)
                TeerbalMode.movementHandler.move(0,0,0,0)


                gevonden = TeerbalVision.find_teerbal(TeerbalVision.find_teerbal(TeerbalVision.getImage()))
            if gevonden:
                TeerbalMode.logger.logevent(self.STATE,"Teerbal gevonden, nu centreren op de teerbal",TeerbalMode.logger.MESSAGE)
                gecentreerd =  self.centreer()
                while not gecentreerd:
                    gecentreerd = self.centreer()
                TeerbalMode.logger.logevent(self.STATE,"Gecentreerd op teerbal, nu ernaar toe lopen",TeerbalMode.logger.MESSAGE)
                nextState.doe_stap()


    def centreer(self):
        # draai_graden = 5
        gecentreerd = False
        index = 0

        teerbal, rechts_draaien, links_draaien = TeerbalVision.center_on_teerbal(TeerbalVision.getImage())

        while not gecentreerd:
            if teerbal:
                if rechts_draaien:
                    TeerbalMode.logger.logevent(self.STATE, "Corrigeeren naar rechts", TeerbalMode.logger.MESSAGE)
                    # print "Draai rechts"
                    TeerbalMode.movementHandler.move(0,0,180,100)
                    time.sleep(TeerbalMode.movementHandler.TIME_TURN)
                    TeerbalMode.movementHandler.move(0,0,0,0)
                elif links_draaien:
                    TeerbalMode.logger.logevent(self.STATE, "Corrigeeren naar links",TeerbalMode.logger.MESSAGE)

                    TeerbalMode.movementHandler.move(0,0,181,100)
                    time.sleep(TeerbalMode.movementHandler.TIME_TURN)
                    TeerbalMode.movementHandler.move(0,0,0,0)

                elif not rechts_draaien and not links_draaien:
                    gecentreerd = True
                    TeerbalMode.logger.logevent(self.STATE, "Gecentreerd op de teerbal", TeerbalMode.logger.MESSAGE)
                    return True
            else:
                TeerbalMode.logger.logevent(self.STATE, "Teerbal verloren uit zicht", TeerbalMode.logger.MESSAGE)
                TeerbalVision.lost()
                # draai_graden = draai_graden/2
            index+=1

            teerbal, rechts_draaien, links_draaien = TeerbalVision.center_on_teerbal((TeerbalVision.getImage()))



class MoveState:

    STATE = "TeerbalMode MoveState"

    def __init__(self):
        pass

    def doe_stap(self):
        if TeerbalMode.alive:

            found,verdwenen,gecentreerd = TeerbalVision.isCentrated(TeerbalVision.getImage())
            while TeerbalMode.alive and not found:
                # print found
                if gecentreerd:
                    TeerbalMode.logger.logevent(self.STATE, "Teerbal ligt in het midden, nu een stap naar voren zetten", TeerbalMode.logger.MESSAGE)
                    self.walk_forward()
                else:
                    #True = links draaien, False = rechts draaien
                    kant_draaien = TeerbalVision.lost()
                    if kant_draaien:
                        print "Draai terug naar links"
                        TeerbalMode.movementHandler.move(0,0,181,100)
                        time.sleep(TeerbalMode.movementHandler.TIME_TURN)
                        TeerbalMode.movementHandler.move(0,0,0,0)
                    else:
                        print "Draai terug naar rechts"
                        TeerbalMode.movementHandler.move(0,0,180,100)
                        time.sleep(TeerbalMode.movementHandler.TIME_TURN)
                        TeerbalMode.movementHandler.move(0,0,0,0)

                found,verdwenen,gecentreerd = TeerbalVision.isCentrated(TeerbalVision.getImage())
                print found
            if TeerbalMode.alive and verdwenen:
                #als de teerbal is verdwenen na het lopen kijken of hij onder in de foto met een kleinere area nog te vinden is
                FoundState.play_sound()



    def walk_forward(self):
        TeerbalMode.logger.logevent(self.STATE, "Stap vooruit", TeerbalMode.logger.MESSAGE)
        TeerbalMode.movementHandler.move(0, 100, 0, 0)
        time.sleep(TeerbalMode.movementHandler.TIME_MOVE_ONE_STEP * 5)
        TeerbalMode.movementHandler.move(0,0,0,0)



class FoundState:

    STATE = "TeerbalMode FoundState"

    def __init__(self):
        #self.image_path = image_path
        pass

    #methode die een geluids bestand afspeelt
    def play_sound(self):
        TeerbalMode.logger.logevent(self.STATE, "Maak nu geluid!", TeerbalMode.logger.MESSAGE)
        # TeerbalMode.spinOS.play_sound(1)




