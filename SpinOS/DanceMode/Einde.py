import time

__author__ = 'Robert'


class Einde:

    movementHandler = None

    def __init(self, movementhandler):
        self.movementHandler = movementhandler

    def run(self):
        heigt = self.movementHandler.legs[3].get_heigt()
        self.movementHandler.legs[3].set_heigt(heigt-20)
        time.sleep(.5)
        self.movementHandler.legs[3].set_knee(90)

        for x in range(0,5):
            self.movementHandler.legs[3].set_hip(45)
            heigt = self.movementHandler.legs[0].get_heigt()
            self.movementHandler.legs[0].set_heigt(heigt+10)
            self.movementHandler.legs[1].set_heigt(heigt+10)
            self.movementHandler.legs[2].set_heigt(heigt+10)
            self.movementHandler.legs[4].set_heigt(heigt-10)
            self.movementHandler.legs[5].set_heigt(heigt-10)
            time.sleep(1)
            self.movementHandler.legs[0].set_heigt(heigt-10)
            self.movementHandler.legs[1].set_heigt(heigt-10)
            self.movementHandler.legs[2].set_heigt(heigt-10)
            self.movementHandler.legs[4].set_heigt(heigt+10)
            self.movementHandler.legs[5].set_heigt(heigt+10)
            time.sleep(1)
            self.movementHandler.legs[3].set_hip(90)
            heigt = self.movementHandler.legs[0].get_heigt()
            self.movementHandler.legs[0].set_heigt(heigt+10)
            self.movementHandler.legs[1].set_heigt(heigt+10)
            self.movementHandler.legs[2].set_heigt(heigt+10)
            self.movementHandler.legs[4].set_heigt(heigt-10)
            self.movementHandler.legs[5].set_heigt(heigt-10)
            time.sleep(1)
            self.movementHandler.legs[0].set_heigt(heigt-10)
            self.movementHandler.legs[1].set_heigt(heigt-10)
            self.movementHandler.legs[2].set_heigt(heigt-10)
            self.movementHandler.legs[4].set_heigt(heigt+10)
            self.movementHandler.legs[5].set_heigt(heigt+10)
            time.sleep(1)