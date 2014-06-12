import threading
import math
import time
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

class MovementHandler:


    #minmaale en maximale hoogte van onderkant servo ten opzichte van grond
    min_height_mm = 75
    max_height_mm = 175

    #time for turning one degree
    time_per_degrees = 0.01

    #min execution time, for servo chip
    min_exec_time = 0.05

    #uitslag van een stap
    stap_uitslag_front = 50
    stap_uitslag_y_front = 50

    stap_uitslag_middle = 50
    stap_uitslag_y_middle = 50

    stap_uitslag_back = -50
    stap_uitslag_y_back = 50

    #maximale uitslag voor poten
    max_uitslag_x_voor = 50
    max_uitslag_x_midden = 50
    max_uitslag_x_achter = 50

    max_uitslag_y_voor = 50
    max_uitslag_y_midden = 50
    max_uitslag_y_achter = 50

    #aantal graden dat de poot omhoog gaat
    raise_leg_angle = 15

    #time per degree
    TIME_TURN_PER_DEGREE = 2
    TIME_MOVE_ONE_CM =2

    #pwm freq chip 1
    PWM_FREQ = 50
    #pwm freq chip 2
    PWM_FREQ_1 = 53

    #constructor
    def __init__(self):
        self.pwm = PWM(0x47)                # PWM for the first servo controller
        self.pwm.setPWMFreq(MovementHandler.PWM_FREQ)    # Set frequency to 50 Hz
        self.pwm2 = PWM(0x46)               # PWM for the first servo controller
        self.pwm2.setPWMFreq(MovementHandler.PWM_FREQ_1)   # Set frequency to 50 Hz
        self.legs = [Leg(1, self.pwm), Leg(2, self.pwm), Leg(3, self.pwm), Leg(4, self.pwm2), Leg(5, self.pwm2), Leg(6, self.pwm2)]

        self.legs[0].normal_x = 100
        self.legs[0].normal_y = 100
        self.legs[0].angle_afwijking = -22
        self.legs[2].normal_x = 100
        self.legs[2].normal_y = 75
        self.legs[2].angle_afwijking = 22
        self.move_degrees = 0
        self.move_power = 0
        self.turn_degrees = 0
        self.turn_power = 0
        self.height_setting = 50
        self.internal_degrees = 0
        self.internal_power = 0
        self.variable_mutex = threading.Semaphore(1)
        self.group_mutex = threading.Semaphore(3)
        self.group2_mutex = threading.Semaphore(3)
        self.stand_gait = 1 #gait 0 is alle poten op de grond na kaliberen
        thread_main = threading.Thread(target=self.movement)
        thread_main.start()
        self.last_height = 0
    #move, set variabels
    def move(self, degreesMove, powerMove, degreesTurn, powerTurn):
        self.variable_mutex.acquire()
        self.move_degrees = degreesMove
        self.move_power = powerMove
        self.turn_degrees = degreesTurn
        self.turn_power = powerTurn
        self.variable_mutex.release()
    #move height, set variabels
    def move_height(self, height):
        self.variable_mutex.acquire()
        self.height_setting = height
        self.variable_mutex.release()

    #move internal, set variabels
    def move_internal(self, degrees, power):
        self.variable_mutex.acquire()
        self.internal_degrees = degrees
        self.internal_power = power
        self.variable_mutex.release()

    #die all
    def die(self):
        pass

    #omzetten van graden naar radialen
    def degrees_to_radians(self, degrees):
        return math.degrees(float(degrees))


    #get gamma angle
    def get_gammma_angle(self, x, y):
        #poot staat in een rechte hoek
        if y == 0:
            return math.pi/2.0
        #tanges aanliggende zijde delen door de overstaande zijde
        return math.atan((float(x) / float(y)))

    #inverse kinematics hoeken berekenen, aan de hand van x,y,z in mm
    def get_angles(self, y, x, z, leg):
        #if leg.leg_number in [1, 4, 3, 6]:
            #is voor of achter dus x en y schuifen op
        #    x = int(x * math.cos(0.4014257279587))
        #    y = int(y * math.sin(0.4014257279587))

        #gamma hoek berekenen (hoek van de heup)
        gamma = self.get_gammma_angle(x, y)
        #totale lengte poot berekenen
        L1 = math.sqrt((float(x)*float(x))+(float(y)*float(y)))
        #legte L berekenen
        L = math.sqrt((float(z) * float(z)) + (float((L1 - Leg.COXA)) * float((L1 - Leg.COXA))))

        #hoek a1 berekenen waarbij waarde z_div_L tussen -1 en 1
        z_div_L =float(z) / float(L)
        if z_div_L < -1.0:
            z_div_L = -1
        elif z_div_L > 1.0:
            z_div_L = 1.0
        a1 = math.acos(z_div_L)


        #cosinus regel op driehoek Tibia, Femur, L om hoek a2 te berekenen
        sum = ((Leg.TIBIA * Leg.TIBIA) - (Leg.FEMUR * Leg.FEMUR) - (L * L)) / (-2 * Leg.FEMUR * L)
        if sum < -1.0:
            sum = -1
        elif sum > 1.0:
            sum = 1.0
        a2 = math.acos(sum)

        alpha = a1 + a2

        #cosinus regel op driehoek Tibia, Femur, L om hoek beta te berekenen
        sum = ((L * L) - (Leg.TIBIA * Leg.TIBIA) - (Leg.FEMUR * Leg.FEMUR)) / (-2 * Leg.TIBIA * Leg.FEMUR)
        if sum < -1.0:
            sum = -1
        elif sum > 1.0:
            sum = 1.0
        beta = math.acos(sum)

        #gamma naar graden omzetten en indien deze <0 is ophogen
        gamma =math.degrees(gamma)
        if gamma < 0:
            gamma += 180

        if leg.leg_number == 3:
            print gamma
        return (math.degrees(alpha), math.degrees(beta), gamma)

    #poten op vaste positie zetten
    def kalibreren(self):
        for i in [1 ,4, 2, 5, 3, 6]:
            #poten naar voren zetten
            leg = self.legs[i-1]
            leg.last_x = 0
            leg.last_y = 75
            leg.last_z = MovementHandler.min_height_mm
            alpha, beta, gamma = self.get_angles(50, 150, MovementHandler.min_height_mm, leg)
            leg.set_height(alpha+30)
            time.sleep(0.5)
            leg.set_hip(gamma)
            leg.set_knee(beta)
            time.sleep(0.5)

        time.sleep(0.5)
        for i in [1 , 4, 2, 5, 3, 6]:
            leg = self.legs[i-1]
            #hoeken ophalen van poten en op de nul positie zetten
            alpha, beta, gamma = self.get_angles(0, 150, MovementHandler.min_height_mm, leg)
            #poten op juiste posistie zetten
            leg.set_height(alpha+30)
            time.sleep(0.5)
            leg.set_hip(gamma)
            leg.set_knee(beta)
            time.sleep(0.5)
            leg.set_height(alpha)
            time.sleep(2)

    #poot omhoog doen
    def raise_leg(self, leg):
        leg.set_height(leg.get_height() + MovementHandler.raise_leg_angle )
        #tijd wachten zo lang het duurt om de servo te bewegen
        excution_time=MovementHandler.raise_leg_angle * MovementHandler.time_per_degrees
        excution_time = math.fabs(excution_time)
        if excution_time < MovementHandler.min_exec_time:
            excution_time = MovementHandler.min_exec_time

        time.sleep(excution_time)

    #poot omlaag doen
    def lower_leg(self, leg):
        #hoeken uitrekenen
        alpha, beta, gamma = self.get_angles(leg.last_x, leg.last_y, leg.last_z, leg)
        #verschil tussen huidige hoek en nieuwe hoek berekenen
        dif_alpha = (leg.get_height() - (alpha - MovementHandler.raise_leg_angle ))
        dif_gamma = (leg.get_hip() - gamma)
        dif_beta = (leg.get_knee() - beta)
        #hoeken van servo's zetten
        leg.set_height(alpha - MovementHandler.raise_leg_angle )
        leg.set_hip(gamma)
        leg.set_knee(beta)
        #grootste verschil uitrekenen
        max_dif = max([dif_alpha, dif_gamma, dif_beta])
        #tijd wachten tot dat de servo op zijn nieuwe posistie is
        excution_time=max_dif * MovementHandler.time_per_degrees
        excution_time = math.fabs(excution_time)
        if excution_time < MovementHandler.min_exec_time:
            excution_time = MovementHandler.min_exec_time

        time.sleep(excution_time)

    #poten bewegen terwijl ze omhoog staan
    def move_leg_lucht(self, leg, x , y, z):
        #verschil uitrekken
        x_dif = x  - leg.last_x
        y_dif = y - leg.last_y
        alpha, beta, gamma = self.get_angles(x_dif+ leg.last_x, y_dif+leg.last_y, z, leg)


        dif_alpha = (leg.get_height() - alpha)
        dif_gamma = (leg.get_hip() - gamma)
        dif_beta = (leg.get_knee() - beta)

        #hoeken van servo's zetten
        leg.set_height(alpha + MovementHandler.raise_leg_angle )
        leg.set_hip(gamma)
        leg.set_knee(beta)

        max_dif = max([dif_alpha, dif_gamma, dif_beta])
        #tijd wachten tot dat de servo op zijn nieuwe posistie is
        excution_time=max_dif * MovementHandler.time_per_degrees
        excution_time = math.fabs(excution_time)
        if excution_time < MovementHandler.min_exec_time:
            excution_time = MovementHandler.min_exec_time

        time.sleep(excution_time)
        leg.last_y = y
        leg.last_x = x
        leg.last_z = z




    def move_leg_stilstaand(self, leg, x , y, z):
        pass


    def movement(self):
        self.kalibreren()
        while True:
            #variablen ophalen
            self.variable_mutex.acquire()
            power_internal = self.internal_power
            degrees_internal = self.internal_degrees
            power_turn = self.turn_power
            degrees_turn = self.turn_degrees
            power_move = self.move_power
            degrees_move = self.move_degrees
            height = self.height_setting
            self.variable_mutex.release()
            #alleen bewegen als er input is
            if power_move != 0 or power_turn != 0 or height != self.last_height:
                pass