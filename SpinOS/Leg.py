__author__ = 'Rubens'

from Servo import Servo
import time

class Leg:
    #Length in mm
    COXA = 46.13
    FEMUR = 70.61
    TIBIA = 146.0

    def __init__(self, leg_number, pwm):
        #Servo controller
        self.pwm = pwm
        #last leg position
        self.last_x = 0
        self.last_y = 0
        self.last_z = 0
        #normal leg position
        self.normal_x = 0
        self.normal_y = 130
        self.angle_afwijking = 0
        #leg number
        self.leg_number = leg_number

        if leg_number == 1 or leg_number == 3:
            self.hip = Servo(0, pwm)
            self.height = Servo(1, pwm)
            self.knee = Servo(2, pwm)

        elif leg_number == 2 or leg_number == 4:
            self.hip = Servo(6, pwm)
            self.height = Servo(7, pwm)
            self.knee = Servo(8, pwm)


    #set hip
    def set_hip(self, degree):
        self.hip.set_servo(degree - self.angle_afwijking)

    #get hip
    def get_hip(self):
        return self.hip.get_servo()

    #set height
    def set_height(self, degree):
        self.height.set_servo(degree)

    #get height
    def get_height(self):
        return self.height.get_servo()

    #set knee
    def set_knee(self, degree):
        self.knee.set_servo(degree)

    #get knee
    def get_knee(self):
        return self.knee.get_servo()