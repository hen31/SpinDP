import time
__author__ = 'Robert'


class Aftikken:

    movementHandler = None

    def __init(self, movementhandler):
        self.movementHandler = movementhandler

    def run(self):
        for x in range(0, 4):
            heigt = self.movementHandler.legs[0].get_heigt()
            self.movementHandler.legs[0].set_heigt(heigt-20)
            time.sleep(1)
            self.movementHandler.legs[0].set_heigt(heigt)
            time.sleep(1)