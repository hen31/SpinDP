import time

__author__ = 'Robert'


class PushUps:

    movementHandler = None

    def __init(self, movementhandler):
        self.movementHandler = movementhandler

    def run(self):
        for x in range(0, 4):
            hip = self.movementHandler.legs[0].get_heigt()
            self.movementHandler.legs[0].set_heigt(hip-20)
            hip = self.movementHandler.legs[1].get_heigt()
            self.movementHandler.legs[1].set_heigt(hip-20)
            hip = self.movementHandler.legs[2].get_heigt()
            self.movementHandler.legs[2].set_heigt(hip-20)
            hip = self.movementHandler.legs[3].get_heigt()
            self.movementHandler.legs[3].set_heigt(hip-20)
            hip = self.movementHandler.legs[4].get_heigt()
            self.movementHandler.legs[4].set_heigt(hip-20)
            hip = self.movementHandler.legs[5].get_heigt()
            self.movementHandler.legs[5].set_heigt(hip-20)
            time.sleep(1)
            self.movementHandler.legs[0].set_heigt(hip)
            self.movementHandler.legs[1].set_heigt(hip)
            self.movementHandler.legs[2].set_heigt(hip)
            self.movementHandler.legs[3].set_heigt(hip)
            self.movementHandler.legs[4].set_heigt(hip)
            self.movementHandler.legs[5].set_heigt(hip)
            time.sleep(1)