__author__ = 'Rubens'

from Servo import Servo
import time

class Leg:
    COXA = 46.13
    FEMUR = 70.61
    TIBIA = 146.0

    def __init__(self, leg_number, pwm):
        self.pwm = pwm
        self.last_x = 0
        self.last_y = 0
        self.last_z = 0
        self.normal_x = 0
        self.normal_y = 100
        self.leg_number = leg_number
        if leg_number > 3:
            leg_number -= 3
        leg_number -= 1

        self.hip = Servo((leg_number) *3, pwm)
        self.height = Servo((leg_number)*3+1, pwm)
        self.knee = Servo((leg_number)*3+2, pwm)

    #def walk(self):
    #    while (True):
    #        self.set_hip(180)
    #        self.set_height(180)
    #        self.set_knee(180)
    #        time.sleep(2)
    #        self.set_hip(0)
    #        self.set_height(0)
    #        self.knee.set(0)
    #        time.sleep(2)

    def set_hip(self, degree):
        self.hip.set_servo(degree)

    def get_hip(self):
        return self.hip.get_servo()

    def set_height(self, degree):
        self.height.set_servo(degree)

    def get_height(self):
        return self.height.get_servo()

    def set_knee(self, degree):
        self.knee.set_servo(degree)

    def get_knee(self):
        return self.knee.get_servo()