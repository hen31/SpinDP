import threading
import math
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

# het aansturen van het lopen gebeurt in de movement methode, deze loopt op zijn eigen thread doorlopend
# dit gebeurt om stoteren tijdens het lopen te voorkomen,
# het laatste commando dat is gegeven wordt door lopend uitgevoerd

# als er een verandering van commando's is worden de waarde's waarmee de berekingen worden uitgevoerd opnieuw berekend
#


class MovementHandler:



    min_height_mm = 50
    max_height_mm = 100

    min_knee_degrees = 50

    max_internal_degrees = 60



    PWM_FREQ = 50
    def __init__(self):

        self.pwm = PWM(0x40)                # PWM for the first servo controller
        self.pwm.setPWMFreq(MovementHandler.PWM_FREQ)    # Set frequency to 50 Hz
        self.pwm2 = PWM(0x41)               # PWM for the first servo controller
        self.pwm2.setPWMFreq(MovementHandler.PWM_FREQ)   # Set frequency to 50 Hz
        self.leg = Leg(0, self.pwm)
        self.leg.set_height(180)
        self.legs = [Leg(1, self.pwm), Leg(2, self.pwm), Leg(3, self.pwm), Leg(4, self.pwm2), Leg(5, self.pwm2), Leg(6, self.pwm2)]
        self.move_degrees = 0
        self.move_power = 0
        self.turn_degrees = 0
        self.turn_power = 0
        self.height_setting = 50
        self.internal_degrees = 0
        self.internal_power = 0
        self.variable_mutex = threading.Semaphore(1)

    def move(self, degreesMove, powerMove, degreesTurn, powerTurn):
        self.variable_mutex.acquire()
        self.move_degrees = degreesMove
        self.move_power = powerMove
        self.turn_degrees = degreesTurn
        self.turn_power = powerTurn
        self.variable_mutex.release()

    def move_height(self, height):
        self.variable_mutex.acquire()
        self.height_setting = height
        self.variable_mutex.release()

    def move_internal(self, degrees, power):
        self.variable_mutex.acquire()
        self.internal_degrees = degrees
        self.internal_power = power
        self.variable_mutex.release()

    def die(self):
        pass

    def degrees_to_radians(self, degrees):
        return degrees *( math.pi/180)


    def get_gammma_angle(self, x, y):
        return math.degrees(math.atan(float(x) / float(y)))

    def get_angles(self, x, y, z):

        gamma = self.get_gammma_angle(x, y)

        L = math.sqrt((float(z) * float(z)) + math.exp((y - Leg.COXA), 2))

        a1 = math.acos(float(z) / float(L))

        tibia2 = Leg.TIBIA * Leg.TIBIA
        a2 = math.acos((tibia2 - (Leg.FEMUR * Leg.FEMUR) - (L * L)) / (-2 * Leg.FEMUR * L))
        a = a1 + a2

        beta = math.acos(((L * L) - (Leg.TIBIA * Leg.TIBIA) - (Leg.FEMUR * Leg.FEMUR)) / (-2 * Leg.TIBIA * Leg.FEMUR))

        return (math.degrees(a) , math.degrees(beta), math.degrees(gamma))



    def movement(self):
        while True:
            self.variable_mutex.acquire()
            power_internal = self.internal_power
            degrees_internal = self.internal_degrees
            power_turn = self.turn_power
            degrees_turn = self.turn_degrees
            power_move = self.move_power
            degrees_move = self.move_degrees
            height = self.height_setting
            self.variable_mutex.release()
            if power_move != 0 and power_turn != 0:
                y = (((power_internal * math.cos(self.degrees_to_radians(degrees_internal))) + 100) / 2) - 50 #-50  - 50
                mm_height = MovementHandler.min_height_mm + (float(MovementHandler.max_height_mm - MovementHandler.min_height_mm) / float(100)) * height

                z_mm_front = mm_height
                z_mm_front += (float(MovementHandler.max_height_mm - mm_height) / float(100)) * y

                z_mm_middle = mm_height

                z_mm_back = mm_height
                z_mm_back -= (float(MovementHandler.max_height_mm - mm_height) / float(100)) * y

                alpha, beta, gamma = self.get_angles(0, 0, z_mm_front)

                self.legs[0].set_hip(gamma)
                self.legs[0].set_height(alpha)
                self.legs[0].set_knee(beta)










            else:

                y = ((power_internal * math.cos(degrees_internal)) + 100) / 2
                x = ((power_internal * math.sin(degrees_internal)) + 100) / 2
                #uitrekenen waardes
                servo_height = (float(MovementHandler.max_height_degrees - MovementHandler.min_height_degrees) / float(100)) * height
                servo_angle_calc = ((float(MovementHandler.max_internal_degrees) / float(100)) * y) - (MovementHandler.max_internal_degrees / 2)
                servo_bank_calc = ((float(MovementHandler.max_internal_degrees) / float(100)) * x) - (MovementHandler.max_internal_degrees / 2)


                #voorste servo
                servo_1 = servo_height
                servo_1 = servo_front_height + servo_angle_calc

                servo_4 = servo_height
                servo_4 = servo_front_height + servo_angle_calc

                #midelste servo
                servo_2 = servo_height
                servo_5 = servo_height

                #achterste servo
                servo_3 = servo_height
                servo_3 = servo_back_height - servo_angle_calc

                servo_6 = servo_height
                servo_6 = servo_back_height - servo_angle_calc


                #left
                servo_1 += servo_bank_calc #front
                servo_2 += servo_bank_calc #middle
                servo_3 += servo_bank_calc #back

                #right
                servo_4 -= servo_bank_calc #front
                servo_5 -= servo_bank_calc #middle
                servo_6 -= servo_bank_calc #back

