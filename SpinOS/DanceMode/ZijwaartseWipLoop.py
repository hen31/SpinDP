from DanceMode import DanceMode
from DanceMode.DanceMode import DanceMode

__author__ = 'Robert'


class ZijwaartseWipLoop:

    def __init__(self, movement):
        pass

    def run(self):

        pass
        # self.poot_omhoog(0)
        # self.poot_omhoog(1)
        # self.poot_omhoog(2)
        #
        # self.poot_omlaag(3)
        # self.poot_omlaag(4)
        # self.poot_omlaag(5)



    def poot_omhoog(self, leg_index):
        alpha, beta, gamma = DanceMode.movementHandler.get_angles(DanceMode.movementHandler.legs[leg_index].normal_x, DanceMode.movementHandler.legs[leg_index].normal_y, 175)
        DanceMode.movementHandler.legs[leg_index].set_height(alpha)
        DanceMode.movementHandler.legs[leg_index].set_hip(gamma)
        DanceMode.movementHandler.legs[leg_index].set_knee(beta)

    def poot_omlaag(self, leg_index):
        alpha, beta, gamma = DanceMode.movementHandler.get_angles(DanceMode.movementHandler.legs[leg_index].normal_x, DanceMode.movementHandler.legs[leg_index].normal_y, 75)
        DanceMode.movementHandler.legs[leg_index].set_height(alpha)
        DanceMode.movementHandler.legs[leg_index].set_hip(gamma)
        DanceMode.movementHandler.legs[leg_index].set_knee(beta)

