__author__ = 'Robert'

import threading
from CardState import CardState
class BalloonMode:

    #Alive variabele, alle states controleren hierop
    alive = True
    #Logger variabele
    logger = None
    #Movement handler, zo kan er gelopen worden
    movementHandler = None

    #Constructor
    def __init__(self, movementHandler, logger, serial):
        #Alive aanzetten
        self.set_alive(True)
        #Logger instellen
        BalloonMode.logger = logger
        #MovementHandler instellen
        BalloonMode.movementHandler = movementHandler
        #Serial instellen
        BalloonMode.serial = serial
        #Thread opstarten
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        #Volgendee opstarten

        state = CardState(self)
        state.doe_stap([])

    def set_alive(self, value):
        #Alive variabele value geven
        BalloonMode.alive = value

    def process_command(self, command, message):
        pass