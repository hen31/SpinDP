import threading
from Adafruit_PWM_Servo_Driver import PWM
from Leg import Leg

__author__ = 'Ruben en Hendrik'
#Layout van poten van spin
#       14
#       25
#       36
#Lopen gebeurt op gait manier de poten zijn dan als volgt
# groep 1: 1,5,3
# groep 2: 4,2,6
# 6 mogelijkheden groep is in de lucht groep staat op de grond
# groep 1 omhoog aan het bewegen, groep 2 op de grond
# groep 1 naar voren/achteren aan het bewegen, groep 2 op de grond
# groep 1 naar beneden aan het bewegen, groep 2 op de grond
# groep 2 omhoog aan het bewegen, groep 1 op de grond
# groep 2 naar voren/achteren aan het bewegen, groep 1 op de grond
# groep 2 naar beneden aan het bewegen, groep 1 op de grond
class MovementHandler:


    def __init__(self):

        self.pwm = PWM(0x40, debug=False)               # PWM for the first servo controller
        self.pwm.setPWMFreq(50)                         # Set frequency to 50 Hz
        self.leg = Leg(0, self.pwm)
        self.leg.set_height(180)

    def move(self, degreesMove, powerMove, degreesTurn, powerTurn):
        pass

    def move_height(self, height):
        pass



    def move_internal(self, degrees, power):
        pass

    def die(self):
        pass

    def movement(self):
        pass
