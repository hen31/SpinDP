import threading
from TeerbalVision import TeerbalVision


__author__ = 'Jeroen'


class TeerbalMode:

    alive = True
    logger = None
    movementHandler = None


    def __init__(self,movementHandler, logger):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        TeerbalMode.logger = logger
        TeerbalMode.movementHandler = movementHandler



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
            # gevonden = TeerbalVision.find_teerbal(os.path.join(os.path.dirname(__file__) + "/TestImages",'vooruit.png'))
            gevonden = TeerbalVision.find_teerbal(TeerbalVision.find_teerbal(TeerbalVision.getImage()))
            while not gevonden:
                TeerbalMode.logger.logevent(self.STATE,"Geen teelbal gevonden, nu draaien",TeerbalMode.logger.MESSAGE)
                #draai x graden naar rechts
                # TeerbalMode.movementHandler.move(0,0,180,100)
                # time.sleep(TeerbalMode.movementHandler.TIME_TURN_PER_DEGREE * 5)

                # gevonden = TeerbalVision.find_teerbal(os.path.join(os.path.dirname(__file__) + "/TestImages",'1.jpg'))
                gevonden = TeerbalVision.find_teerbal(TeerbalVision.find_teerbal(TeerbalVision.getImage()))
            if gevonden:
                TeerbalMode.logger.logevent(self.STATE,"Teerbal gevonden, nu centreren op de teerbal",TeerbalMode.logger.MESSAGE)
                gecentreerd =  self.centreer()
                while not gecentreerd:
                    gecentreerd = self.centreer()
                TeerbalMode.logger.logevent(self.STATE,"Gecentreerd op teerbal, nu ernaar toe lopen",TeerbalMode.logger.MESSAGE)
                nextState.doe_stap()


    def centreer(self):
        draai_graden = 5
        gecentreerd = False
        index = 0
        # array = (os.path.join(os.path.dirname(__file__) + "/TestImages",'1.jpg'),os.path.join(os.path.dirname(__file__) + "/TestImages",'2.jpg'),os.path.join(os.path.dirname(__file__) + "/TestImages",'3.jpg'),os.path.join(os.path.dirname(__file__) + "/TestImages",'3found.jpg'),os.path.join(os.path.dirname(__file__) + "/TestImages",'5.jpg'))
        # teerbal, rechts_draaien, links_draaien = TeerbalVision.center_on_teerbal(array[index])
        teerbal, rechts_draaien, links_draaien = TeerbalVision.center_on_teerbal(TeerbalVision.getImage())
        # while index < len(array) and not gecentreerd:
        while not gecentreerd:
            if teerbal:
                if rechts_draaien:
                    print "Draai rechts"
                    # TeerbalMode.movementHandler.move(0,0,180,100)
                    # time.sleep(TeerbalMode.movementHandler.TIME_TURN_PER_DEGREE * draai_graden)
                elif links_draaien:
                    print "Draai links"
                    # TeerbalMode.movementHandler.move(0,0,181,100)
                    # time.sleep(TeerbalMode.movementHandler.TIME_TURN_PER_DEGREE * draai_graden)

                elif not rechts_draaien and not links_draaien:
                    gecentreerd = True
                    TeerbalMode.logger.logevent(self.STATE, "Gecentreerd op de teerbal", TeerbalMode.logger.MESSAGE)
                    return True
            else:
                TeerbalMode.logger.logevent(self.STATE, "Teerbal verloren uit zicht", TeerbalMode.logger.MESSAGE)
                TeerbalVision.lost()
                draai_graden = draai_graden/2
            index+=1
            # teerbal, rechts_draaien, links_draaien = TeerbalVision.center_on_teerbal(array[index])
            teerbal, rechts_draaien, links_draaien = TeerbalVision.center_on_teerbal((TeerbalVision.getImage()))



class MoveState:

    STATE = "TeerbalMode MoveState"

    def __init__(self):
        pass

    def doe_stap(self):
        if TeerbalMode.alive:
            # found,verdwenen,gecentreerd = TeerbalVision.isCentrated(os.path.join(os.path.dirname(__file__) + "/TestImages",'3.jpg'))
            found,verdwenen,gecentreerd = TeerbalVision.isCentrated(TeerbalVision.getImage())
            while TeerbalMode.alive and not found:
                print found
                if gecentreerd:
                    self.walk_forward()
                else:
                    #True = links draaien, False = rechts draaien
                    kant_draaien = TeerbalVision.lost()
                    if kant_draaien:
                        print "Draai terug naar links"
                        # TeerbalMode.movementHandler.move(0,0,181,100)
                        # time.sleep(TeerbalMode.movementHandler.TIME_TURN_PER_DEGREE * 5)
                    else:
                        print "Draai terug naar rechts"
                        # TeerbalMode.movementHandler.move(0,0,180,100)
                        # time.sleep(TeerbalMode.movementHandler.TIME_TURN_PER_DEGREE * 5)
                # found,verdwenen,gecentreerd = TeerbalVision.isCentrated(os.path.join(os.path.dirname(__file__) + "/TestImages",'3found.jpg'))
                found,verdwenen,gecentreerd = TeerbalVision.isCentrated(TeerbalVision.getImage())
                print found
            if TeerbalMode.alive and verdwenen:
                #als de teerbal is verdwenen na het lopen kijken of hij onder in de foto met een kleinere area nog te vinden is
                pass



    def walk_forward(self):
        pass
        # TeerbalMode.movementHandler.move(0, 100, 0, 0)
        # time.sleep(TeerbalMode.movementHandler.TIME_MOVE_ONE_CM * 10)
        # TeerbalMode.movementHandler.move(0,0,0,0)




