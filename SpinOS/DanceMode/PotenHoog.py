__author__ = 'Robert'

from DanceMode import DanceMode
import time

class PotenHoog:
    #1 en 6 omhoog
    #2 en 5 omhoog
    #3 en 4 omhoog

    def __init(self):
        pass

    def run(self):
        #1 en 6
        #2 en 5
        #3 en 4
        poten = [[1, 6], [2, 5], [3, 4]]
        for poot in poten:
            DanceMode.movementHandler.legs[poot[0]].set_knee(0)
            time.sleep(0.5)
            DanceMode.movementHandler.legs[poot[0]].set_hip(0)
            DanceMode.movementHandler.legs[poot[0]].set_height(0)

            DanceMode.movementHandler.legs[poot[1]].set_knee(0)
            time.sleep(0.5)
            DanceMode.movementHandler.legs[poot[1]].set_hip(0)
            DanceMode.movementHandler.legs[poot[1]].set_height(0)

            time.sleep(3)

            a,b,g = DanceMode.movementHandler.get_angles(DanceMode.movementHandler.legs[poot[0]].normal_x, DanceMode.movementHandler.legs[poot[0]].normal_y, DanceMode.movementHandler.legs[poot[0]].normal_z)
            a2,b2,g2 = DanceMode.movementHandler.get_angles(DanceMode.movementHandler.legs[poot[1]].normal_x, DanceMode.movementHandler.legs[poot[1]].normal_y, DanceMode.movementHandler.legs[poot[1]].normal_z)

            DanceMode.movementHandler.legs[poot[0]].set_hip(a)
            DanceMode.movementHandler.legs[poot[0]].set_height(b)
            DanceMode.movementHandler.legs[poot[0]].set_knee(g)

            DanceMode.movementHandler.legs[poot[1]].set_hip(a2)
            DanceMode.movementHandler.legs[poot[1]].set_height(b2)
            DanceMode.movementHandler.legs[poot[1]].set_knee(g2)
            time.sleep(3)

