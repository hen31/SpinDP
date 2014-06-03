from DanceMode import DanceMode
import time

__author__ = 'Robert'


class Einde:

    def __init(self):
        pass

    def run(self):
        heigt = DanceMode.movementHandler.legs[3].get_heigt()
        DanceMode.movementHandler.legs[3].set_heigt(heigt-20)
        time.sleep(.5)
        DanceMode.movementHandler.legs[3].set_knee(90)

        for x in range(0,5):
            DanceMode.movementHandler.legs[3].set_hip(45)
            heigt = DanceMode.movementHandler.legs[0].get_heigt()
            DanceMode.movementHandler.legs[0].set_heigt(heigt+10)
            DanceMode.movementHandler.legs[1].set_heigt(heigt+10)
            DanceMode.movementHandler.legs[2].set_heigt(heigt+10)
            DanceMode.movementHandler.legs[4].set_heigt(heigt-10)
            DanceMode.movementHandler.legs[5].set_heigt(heigt-10)
            time.sleep(1)
            DanceMode.movementHandler.legs[0].set_heigt(heigt-10)
            DanceMode.movementHandler.legs[1].set_heigt(heigt-10)
            DanceMode.movementHandler.legs[2].set_heigt(heigt-10)
            DanceMode.movementHandler.legs[4].set_heigt(heigt+10)
            DanceMode.movementHandler.legs[5].set_heigt(heigt+10)
            time.sleep(1)
            DanceMode.movementHandler.legs[3].set_hip(90)
            heigt = DanceMode.movementHandler.legs[0].get_heigt()
            DanceMode.movementHandler.legs[0].set_heigt(heigt+10)
            DanceMode.movementHandler.legs[1].set_heigt(heigt+10)
            DanceMode.movementHandler.legs[2].set_heigt(heigt+10)
            DanceMode.movementHandler.legs[4].set_heigt(heigt-10)
            DanceMode.movementHandler.legs[5].set_heigt(heigt-10)
            time.sleep(1)
            DanceMode.movementHandler.legs[0].set_heigt(heigt-10)
            DanceMode.movementHandler.legs[1].set_heigt(heigt-10)
            DanceMode.movementHandler.legs[2].set_heigt(heigt-10)
            DanceMode.movementHandler.legs[4].set_heigt(heigt+10)
            DanceMode.movementHandler.legs[5].set_heigt(heigt+10)
            time.sleep(1)