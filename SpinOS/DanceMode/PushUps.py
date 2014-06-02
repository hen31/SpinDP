from DanceMode import DanceMode
import time

__author__ = 'Robert'


class PushUps:

    def __init(self):
        pass

    def run(self):
        for x in range(0, 4):
            hip = DanceMode.movementHandler.legs[0].get_heigt()
            DanceMode.movementHandler.legs[0].set_heigt(hip-20)
            hip = DanceMode.movementHandler.legs[1].get_heigt()
            DanceMode.movementHandler.legs[1].set_heigt(hip-20)
            hip = DanceMode.movementHandler.legs[2].get_heigt()
            DanceMode.movementHandler.legs[2].set_heigt(hip-20)
            hip = DanceMode.movementHandler.legs[3].get_heigt()
            DanceMode.movementHandler.legs[3].set_heigt(hip-20)
            hip = DanceMode.movementHandler.legs[4].get_heigt()
            DanceMode.movementHandler.legs[4].set_heigt(hip-20)
            hip = DanceMode.movementHandler.legs[5].get_heigt()
            DanceMode.movementHandler.legs[5].set_heigt(hip-20)
            time.sleep(1)
            DanceMode.movementHandler.legs[0].set_heigt(hip)
            DanceMode.movementHandler.legs[1].set_heigt(hip)
            DanceMode.movementHandler.legs[2].set_heigt(hip)
            DanceMode.movementHandler.legs[3].set_heigt(hip)
            DanceMode.movementHandler.legs[4].set_heigt(hip)
            DanceMode.movementHandler.legs[5].set_heigt(hip)
            time.sleep(1)