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
            gevonden = TeerbalVision.find_teerbal(TeerbalVision.getImage())
            while not gevonden:
                TeerbalMode.logger.logevent(self.STATE,"Geen teelbal gevonden, nu naar rechts draaien",TeerbalMode.logger.MESSAGE)
                #draai x graden naar rechts
                TeerbalMode.movementHandler.move_one_turn(False)
                gevonden = TeerbalVision.find_teerbal(TeerbalVision.getImage())
            if gevonden:
                TeerbalMode.logger.logevent(self.STATE,"Teerbal gevonden, door naar MoveState", TeerbalMode.logger.MESSAGE)
                nextState.doe_stap()


    # def centreer(self):
    #     # draai_graden = 5
    #     gecentreerd = False
    #     index = 0
    #
    #     teerbal, links_draaien, rechts_draaien = TeerbalVision.center_on_teerbal(TeerbalVision.getImage())
    #
    #     while not gecentreerd:
    #         if teerbal:
    #             if rechts_draaien:
    #                 TeerbalMode.logger.logevent(self.STATE, "Corrigeeren naar rechts", TeerbalMode.logger.MESSAGE)
    #                 # print "Draai rechts"
    #                 TeerbalMode.movementHandler.move(0,0,180,100)
    #                 time.sleep(TeerbalMode.movementHandler.TIME_TURN)
    #                 TeerbalMode.movementHandler.move(0,0,0,0)
    #             elif links_draaien:
    #                 TeerbalMode.logger.logevent(self.STATE, "Corrigeeren naar links",TeerbalMode.logger.MESSAGE)
    #
    #                 TeerbalMode.movementHandler.move(0,0,181,100)
    #                 time.sleep(TeerbalMode.movementHandler.TIME_TURN)
    #                 TeerbalMode.movementHandler.move(0,0,0,0)
    #
    #             elif not rechts_draaien and not links_draaien:
    #                 gecentreerd = True
    #                 TeerbalMode.logger.logevent(self.STATE, "Gecentreerd op de teerbal", TeerbalMode.logger.MESSAGE)
    #                 return True
    #         else:
    #             TeerbalMode.logger.logevent(self.STATE, "Teerbal verloren uit zicht", TeerbalMode.logger.MESSAGE)
    #             TeerbalVision.lost()
    #             # draai_graden = draai_graden/2
    #         index+=1
    #
    #         teerbal, rechts_draaien, links_draaien = TeerbalVision.center_on_teerbal((TeerbalVision.getImage()))



class MoveState:

    STATE = "TeerbalMode MoveState"

    def __init__(self):
        pass

    def doe_stap(self):
        nextState = FoundState()
        #kijken of de teerbal zo ligt dat hij als gevonden word beschouwd
        found  = TeerbalVision.teerbal_found(TeerbalVision.getImage())
        #blijven zoeken totdat de teerbal gevonden is
        while TeerbalMode.alive and not found:
            gecentreerd = TeerbalVision.center(TeerbalVision.getImage())
            while not gecentreerd:
                kant_draaien = TeerbalVision.turn_side(TeerbalVision.getImage())
                if kant_draaien:
                    #draai naar rechts
                    TeerbalMode.logger.logevent(self.STATE,"Centreren: draai rechts", TeerbalMode.logger.MESSAGE)
                    TeerbalMode.movementHandler.move_one_turn(False)
                else:
                    TeerbalMode.logger.logevent(self.STATE,"Centreren: draai links", TeerbalMode.logger.MESSAGE)
                    TeerbalMode.movementHandler.move_one_turn(True)
                gecentreerd = TeerbalVision.center(TeerbalVision.getImage())

            TeerbalMode.logger.logevent(self.STATE, "Vooruit lopen", TeerbalMode.logger.MESSAGE)
            #vooruit lopen
            for i in xrange(0, 3):
                TeerbalMode.movementHandler.move_one_step()
            found = TeerbalVision.teerbal_found(TeerbalVision.getImage())
        if found:
            #geluid afspelen wanneer de teerbal is gevevonden
            # if TeerbalVision.LAST_BLOB_SIZE > 6000:
            #     TeerbalMode.logger.logevent(self.STATE, "Teerbal gevonden!", TeerbalMode.logger.MESSAGE)
            #     nextState.play_sound()
            # else:
            #     TeerbalMode.logger.logevent(self.STATE, "Teerbal heeft een erg kleine area:{}".format(TeerbalVision.LAST_BLOB_SIZE,TeerbalMode.logger.MESSAGE))
            nextState.play_sound()






    # def doe_stap(self):
        # if TeerbalMode.alive:
        #
        #     found,verdwenen,gecentreerd = TeerbalVision.isCentrated(TeerbalVision.getImage())
        #     while TeerbalMode.alive and not found:
        #         # print found
        #         if gecentreerd:
        #             TeerbalMode.logger.logevent(self.STATE, "Teerbal ligt in het midden, nu een stap naar voren zetten", TeerbalMode.logger.MESSAGE)
        #             self.walk_forward()
        #         else:
        #             #True = links draaien, False = rechts draaien
        #             kant_draaien = TeerbalVision.lost()
        #             if kant_draaien:
        #                 TeerbalMode.logger.logevent(self.STATE,"Terug draaien naar links", TeerbalMode.logger.MESSAGE)
        #
        #                 TeerbalMode.movementHandler.move(0,0,181,100)
        #                 time.sleep(TeerbalMode.movementHandler.TIME_TURN)
        #                 TeerbalMode.movementHandler.move(0,0,0,0)
        #             else:
        #                 TeerbalMode.logger.logevent(self.STATE,"Terug draaien naar rechts", TeerbalMode.logger.MESSAGE)
        #                 TeerbalMode.movementHandler.move(0,0,180,100)
        #                 time.sleep(TeerbalMode.movementHandler.TIME_TURN)
        #                 TeerbalMode.movementHandler.move(0,0,0,0)
        #
        #         found,verdwenen,gecentreerd = TeerbalVision.isCentrated(TeerbalVision.getImage())
        #         # print found
        #     if TeerbalMode.alive and verdwenen:
        #         #als de teerbal is verdwenen na het lopen kijken of hij onder in de foto met een kleinere area nog te vinden is
        #         gevonden = TeerbalVision.teerbal_found(TeerbalVision.getImage())
        #         if gevonden:
        #             FoundState.play_sound()
        #         else:
        #             while not gevonden:
        #                 TeerbalMode.logger.logevent(self.STATE, "Kleine stap vooruit om dichter bij teerbal te komen", TeerbalMode.logger.MESSAGE)
        #                 TeerbalMode.movementHandler.move(0, 100, 0, 0)
        #                 time.sleep(TeerbalMode.movementHandler.TIME_MOVE_ONE_STEP * 3)
        #                 TeerbalMode.movementHandler.move(0,0,0,0)
        #                 # if TeerbalVision.LAST_BLOB_SIZE > 4000:
        #                 if TeerbalVision.teerbal_found(TeerbalVision.getImage()):
        #                     FoundState.play_sound()
        #                 else:
        #                     TeerbalMode.logger.logevent(self.STATE,"Teerbal ligt nog niet deel buiten beeld", TeerbalMode.logger.MESSAGE)
        #     else:
        #         TeerbalMode.logger.logevent(self.STATE,"Teerbal is verdwenen laatste grootte ={}".format(TeerbalVision.LAST_BLOB_SIZE), TeerbalMode.logger.MESSAGE)




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
        TeerbalMode.spinOS.play_sound(1)




