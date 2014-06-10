__author__ = 'Robert'

import time

class PotenHoog:
    #1 en 6 omhoog
    #2 en 5 omhoog
    #3 en 4 omhoog

    movementHandler = None

    def __init(self, movementhandler):
        self.movementHandler = movementhandler

    def run(self):
        #1 en 6
        #2 en 5
        #3 en 4
        poten = [[1, 6], [2, 5], [3, 4]]
        for poot in poten:
            self.movementHandler.legs[poot[0]].set_knee(0)
            time.sleep(0.5)
            self.movementHandler.legs[poot[0]].set_hip(0)
            self.movementHandler.legs[poot[0]].set_height(0)

            self.movementHandler.legs[poot[1]].set_knee(0)
            time.sleep(0.5)
            self.movementHandler.legs[poot[1]].set_hip(0)
            self.movementHandler.legs[poot[1]].set_height(0)

            time.sleep(3)

            a,b,g = self.movementHandler.get_angles(self.movementHandler.legs[poot[0]].normal_x, self.movementHandler.legs[poot[0]].normal_y, self.movementHandler.legs[poot[0]].normal_z)
            a2,b2,g2 = self.movementHandler.get_angles(self.movementHandler.legs[poot[1]].normal_x, self.movementHandler.legs[poot[1]].normal_y, self.movementHandler.legs[poot[1]].normal_z)

            self.movementHandler.legs[poot[0]].set_hip(a)
            self.movementHandler.legs[poot[0]].set_height(b)
            self.movementHandler.legs[poot[0]].set_knee(g)

            self.movementHandler.legs[poot[1]].set_hip(a2)
            self.movementHandler.legs[poot[1]].set_height(b2)
            self.movementHandler.legs[poot[1]].set_knee(g2)
            time.sleep(3)

