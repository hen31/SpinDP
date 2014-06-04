from DanceMode import DanceMode
import time
from DanceMode.DanceMode import DanceMode

__author__ = 'Robert'


class ZijwaartseWipLoop:

    MOVE_DISTANCE = 10

    def __init__(self, movement):
        pass

    def run(self):

        #naar rechts lopen
        DanceMode.movementHandler.move(270,100,0,0)
        time.sleep(DanceMode.movementHandler.TIME_MOVE_ONE_CM* ZijwaartseWipLoop.MOVE_DISTANCE)

        #links omhoog
        self.poot_omhoog(0)
        self.poot_omhoog(1)
        self.poot_omhoog(2)
        #rechts naar beneden
        self.poot_omlaag(3)
        self.poot_omlaag(4)
        self.poot_omlaag(5)

        self.beweeg_middelste(1)
        self.reset(0)
        self.reset(1)
        self.reset(2)
        self.reset(3)
        self.reset(4)
        self.reset(5)

        DanceMode.movementHandler.move(90,100,0,0)
        time.sleep(DanceMode.movementHandler.TIME_MOVE_ONE_CM* (ZijwaartseWipLoop.MOVE_DISTANCE*2))

        #rechts omhoog
        self.poot_omhoog(5)
        self.poot_omhoog(4)
        self.poot_omhoog(3)
        #links naar beneden
        self.poot_omlaag(2)
        self.poot_omlaag(1)
        self.poot_omlaag(0)

        self.beweeg_middelste(4)
        self.reset(0)
        self.reset(1)
        self.reset(2)
        self.reset(3)
        self.reset(4)
        self.reset(5)

        DanceMode.movementHandler.move(270,100,0,0)
        time.sleep(DanceMode.movementHandler.TIME_MOVE_ONE_CM* ZijwaartseWipLoop.MOVE_DISTANCE)


    #gooit de desbetreffende poot omhoog
    def beweeg_middelste(self, leg_index):
        alpha, beta, gamma = DanceMode.movementHandler.get_angles(DanceMode.movementHandler.legs[leg_index].normal_x, DanceMode.movementHandler.legs[leg_index].normal_y, 100)
        DanceMode.movementHandler.legs[leg_index].set_height(alpha)
        DanceMode.movementHandler.legs[leg_index].set_hip(gamma)
        DanceMode.movementHandler.legs[leg_index].set_knee(beta)

    def reset(self, leg_index):
        alpha, beta, gamma = DanceMode.movementHandler.get_angles(0,0,0)
        DanceMode.movementHandler.legs[leg_index].set_height(alpha)
        DanceMode.movementHandler.legs[leg_index].set_hip(gamma)
        DanceMode.movementHandler.legs[leg_index].set_knee(beta)


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

