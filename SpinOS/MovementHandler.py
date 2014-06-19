import threading
import math
import time
from Adafruit_PWM_Servo_Driver import PWM
from Leg import Leg

__author__ = 'Ruben en Hendrik'


"""
Layout van poten van spin
       1 3
       2 4

 - Poot 1 naar voren
 - Poot 4 naar voren
 - Poot 2 naar voren
 - Poot 3 naar voren

Poten 2 en 4 kunnen niet te ver naar voren, anders valt de spin om

Vervolgens:
 Alle op de grond naar achteren bewegen

"""

class MovementHandler:


    #minmaale en maximale hoogte van onderkant servo ten opzichte van grond
    min_height_mm = 75
    max_height_mm = 125

    #time for turning one degree
    time_per_degrees = 0.004

    #min execution time, for servo chip
    min_exec_time = 0.03

    #uitslag van een stap
    stap_uitslag = 25
    stap_uitslag_y = 27

    turn_x = 10

    #aantal graden dat de poot omhoog gaat
    raise_leg_angle = 25

    #time per degree
    TIME_TURN = 3
    TIME_MOVE_ONE_STEP = 3

    #pwm freq chip 1
    PWM_FREQ = 50
    #pwm freq chip 2
    PWM_FREQ_1 = 53

    #constructor
    def __init__(self):
        self.pwm = PWM(0x46)                # PWM for the first servo controller
        self.pwm.setPWMFreq(MovementHandler.PWM_FREQ_1)    # Set frequency to 50 Hz
        self.pwm2 = PWM(0x47)               # PWM for the first servo controller
        self.pwm2.setPWMFreq(MovementHandler.PWM_FREQ)   # Set frequency to 50 Hz
        self.legs = [Leg(1, self.pwm), Leg(2, self.pwm), Leg(3, self.pwm2), Leg(4, self.pwm2)]
        self.legs[0].normal_x = 20
        #self.legs[0].normal_y = 117
        self.legs[0].normal_y = 80
        self.legs[0].angle_afwijking = -22
        self.legs[0].angle_afwijking_knee = 0

        self.legs[1].normal_x = -20
        #self.legs[1].normal_y = 117
        self.legs[1].normal_y = 80
        self.legs[1].angle_afwijking = 22



        self.legs[2].normal_x = -20
       # self.legs[2].normal_y = 117
        self.legs[2].normal_y = 80
        self.legs[2].angle_afwijking = 22

        self.legs[3].normal_x = 20
        self.legs[3].normal_y = 80
        #self.legs[3].normal_y = 117
        self.legs[3].angle_afwijking = -22

        self.voor = True
        self.move_degrees = 0
        self.move_power = 0
        self.turn_degrees = 0
        self.turn_power = 0
        self.height_setting = 50
        self.internal_degrees = 0
        self.internal_power = 0
        self.variable_mutex = threading.Semaphore(1)
        self.group_mutex = threading.Semaphore(0)
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

        return (math.degrees(alpha), math.degrees(beta), gamma)

    #poten op vaste positie zetten
    def kalibreren(self):
        pass

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
        leg.set_height(alpha)
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


    def get_excution_time(self,leg,x,y,z):
   #verschil uitrekken
        x_dif = x - leg.last_x
        aantal_stappen = 8 #int(math.fabs(x_dif / 20)) + 1
        #aantal stappen uitrekken
        #if aantal_stappen >15:
        #    aantal_stappen = 15

        #lengte per stap uitrekken

        y_dif = y - leg.last_y
        #zorgen dat het niet meer dan 15 stappen worden
        #if aantal_stappen_y >15:
        #    aantal_stappen_y = 15
        max_y_reached = False
        max_x_reached = False
        #grootste aantal stappen x of y is leidend
        #if aantal_stappen_y > aantal_stappen:
        #    aantal_stappen = aantal_stappen_y


        x_stap = x_dif / aantal_stappen
        y_stap =  y_dif /aantal_stappen
        #voor elke stap de poot bewegen
        i=1

        if x_dif >0:
            if (i* x_stap) > x_dif or max_x_reached == True:
                x_stap = 0
                max_x_reached = True
        else:
            if (i* x_stap) < x_dif or max_x_reached == True:
                x_stap = 0
                max_x_reached = True
        if y_dif > 0:
            if (i* y_stap) > y_dif or max_y_reached == True:
                y_stap = 0
                max_y_reached = True
        else:
            if (i* y_stap) < y_dif or max_y_reached == True:
                y_stap = 0
                max_y_reached = True

        new_x = (x_stap)+ leg.last_x
        new_y = (y_stap)+leg.last_y

        #hoeken uitrekken
        alpha, beta, gamma = self.get_angles(new_x, new_y, z, leg)
        #verschil uitrekken
        dif_gamma = abs(leg.get_hip() - gamma)
        dif_beta = abs(leg.get_knee() - beta)



        max_dif = max([abs(dif_gamma), abs(dif_beta)])
            #max verschil wachten tot servo's op juiste posistie staan
        excution_time = max_dif * MovementHandler.time_per_degrees

        if excution_time < MovementHandler.min_exec_time:
            excution_time = MovementHandler.min_exec_time

        excution_time = math.fabs(excution_time)
        return excution_time

    def move_leg_stilstaand(self, leg, x , y, z, max_exec):
        #verschil uitrekken
        x_dif = x - leg.last_x
        aantal_stappen = 8 #int(math.fabs(x_dif / 20)) + 1
        #aantal stappen uitrekken
        #if aantal_stappen >15:
        #    aantal_stappen = 15

        #lengte per stap uitrekken

        y_dif = y - leg.last_y
        #zorgen dat het niet meer dan 15 stappen worden
        #if aantal_stappen_y >15:
        #    aantal_stappen_y = 15
        max_y_reached = False
        max_x_reached = False
        #grootste aantal stappen x of y is leidend
        #if aantal_stappen_y > aantal_stappen:
        #    aantal_stappen = aantal_stappen_y


        x_stap = x_dif / aantal_stappen
        y_stap =  y_dif /aantal_stappen
        #voor elke stap de poot bewegen
        for i in range(1, aantal_stappen + 1):

            if x_dif >0:
                if (i* x_stap) > x_dif or max_x_reached == True:
                    x_stap = 0
                    max_x_reached = True
            else:
                if (i* x_stap) < x_dif or max_x_reached == True:
                    x_stap = 0
                    max_x_reached = True
            if y_dif > 0:
                if (i* y_stap) > y_dif or max_y_reached == True:
                    y_stap = 0
                    max_y_reached = True
            else:
                if (i* y_stap) < y_dif or max_y_reached == True:
                    y_stap = 0
                    max_y_reached = True

            new_x = (x_stap)+ leg.last_x
            new_y = (y_stap)+leg.last_y

            #hoeken uitrekken
            alpha, beta, gamma = self.get_angles(new_x, new_y, z, leg)

            #verschil uitrekken
            dif_gamma = abs(leg.get_hip() - gamma)
            dif_beta = abs(leg.get_knee() - beta)



            max_dif = max([abs(dif_gamma), abs(dif_beta)])
            #max verschil wachten tot servo's op juiste posistie staan
            #excution_time = max_dif * MovementHandler.time_per_degrees

            #if excution_time < MovementHandler.min_exec_time:
            #   excution_time = MovementHandler.min_exec_time

            #excution_time = math.fabs(excution_time)

            leg.last_y = new_y
            leg.last_x = new_x
            leg.last_z = z
            leg.set_hip(gamma)
            leg.set_knee(beta)
            time.sleep(max_exec)



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

                if degrees_turn > 0 and power_turn > 0:
                    #DRAAIEENN1!!!!
                    rad = 3.14159265 #180
                    rad2 = 0 #0

                    if degrees_turn <= 180:
                        #links

                        x_stap_links = math.cos(rad) * MovementHandler.stap_uitslag
                        x_stap_rechts = math.cos(rad2) * MovementHandler.stap_uitslag
                    else:
                        #rechts
                        x_stap_links = math.cos(rad2) * MovementHandler.stap_uitslag
                        x_stap_rechts = math.cos(rad) * MovementHandler.stap_uitslag

                    #hoogte uitrekken in mmm
                    mm_height = MovementHandler.min_height_mm + (float(MovementHandler.max_height_mm - MovementHandler.min_height_mm) / float(100)) * float(height)

                    self.raise_leg(self.legs[0])
                    self.move_leg_lucht(self.legs[0], self.legs[0].normal_x - x_stap_links, self.legs[0].normal_y, mm_height)
                    self.lower_leg(self.legs[0])

                    self.raise_leg(self.legs[3])
                    self.move_leg_lucht(self.legs[3], self.legs[3].normal_x + x_stap_rechts, self.legs[3].normal_y, mm_height)
                    self.lower_leg(self.legs[3])

                    self.raise_leg(self.legs[2])
                    self.move_leg_lucht(self.legs[2], self.legs[2].normal_x + x_stap_rechts, self.legs[2].normal_y, mm_height)
                    self.lower_leg(self.legs[2])

                    self.raise_leg(self.legs[1])
                    self.move_leg_lucht(self.legs[1], self.legs[1].normal_x - x_stap_links, self.legs[1].normal_y, mm_height)
                    self.lower_leg(self.legs[1])

                #Niet draaien
                else:

                    rad = math.radians(float(degrees_move))

                    #hoogte uitrekken in mmm
                    mm_height = MovementHandler.min_height_mm + (float(MovementHandler.max_height_mm - MovementHandler.min_height_mm) / float(100)) * float(height)

                    y_stap = math.sin(rad) * MovementHandler.stap_uitslag_y
                    x_stap = math.cos(rad) * MovementHandler.stap_uitslag

                    if power_move == 0:
                        x_stap = 0

                    if degrees_move >270 or degrees_move < 45:
                        if self.voor == True:

                            #Poten op volgorde omhoog, verplaatsen en weer naar beneden brengen
                            self.raise_leg(self.legs[1])
                            self.move_leg_lucht(self.legs[1], self.legs[1].normal_x + x_stap, self.legs[1].normal_y - y_stap, mm_height)
                            self.lower_leg(self.legs[1])

                            self.raise_leg(self.legs[3])
                            self.move_leg_lucht(self.legs[3], self.legs[3].normal_x - x_stap, self.legs[3].normal_y + y_stap, mm_height)
                            self.lower_leg(self.legs[3])


                            self.raise_leg(self.legs[0])
                            self.move_leg_lucht(self.legs[0], self.legs[0].normal_x + x_stap, self.legs[0].normal_y - y_stap, mm_height)
                            self.lower_leg(self.legs[0])

                            self.raise_leg(self.legs[2])
                            self.move_leg_lucht(self.legs[2], self.legs[2].normal_x - x_stap, self.legs[2].normal_y + y_stap, mm_height)
                            self.lower_leg(self.legs[2])
                            self.voor = False
                        else:
                                           #Poten op volgorde omhoog, verplaatsen en weer naar beneden brengen
                            self.raise_leg(self.legs[3])
                            self.move_leg_lucht(self.legs[3], self.legs[3].normal_x - x_stap, self.legs[3].normal_y + y_stap, mm_height)
                            self.lower_leg(self.legs[3])

                            self.raise_leg(self.legs[1])
                            self.move_leg_lucht(self.legs[1], self.legs[1].normal_x + x_stap, self.legs[1].normal_y - y_stap, mm_height)
                            self.lower_leg(self.legs[1])

                            self.raise_leg(self.legs[2])
                            self.move_leg_lucht(self.legs[2], self.legs[2].normal_x - x_stap, self.legs[2].normal_y + y_stap, mm_height)
                            self.lower_leg(self.legs[2])

                            self.raise_leg(self.legs[0])
                            self.move_leg_lucht(self.legs[0], self.legs[0].normal_x + x_stap, self.legs[0].normal_y - y_stap, mm_height)
                            self.lower_leg(self.legs[0])

                            self.voor = True
                    elif degrees_move> 135 and degrees_move <225:
                        if self.voor == True:
                            self.raise_leg(self.legs[0])
                            self.move_leg_lucht(self.legs[0], self.legs[0].normal_x + x_stap, self.legs[0].normal_y - y_stap, mm_height)
                            self.lower_leg(self.legs[0])

                            self.raise_leg(self.legs[2])
                            self.move_leg_lucht(self.legs[2], self.legs[2].normal_x - x_stap, self.legs[2].normal_y + y_stap, mm_height)
                            self.lower_leg(self.legs[2])
                            #Poten op volgorde omhoog, verplaatsen en weer naar beneden brengen
                            self.raise_leg(self.legs[1])
                            self.move_leg_lucht(self.legs[1], self.legs[1].normal_x + x_stap, self.legs[1].normal_y - y_stap, mm_height)
                            self.lower_leg(self.legs[1])

                            self.raise_leg(self.legs[3])
                            self.move_leg_lucht(self.legs[3], self.legs[3].normal_x - x_stap, self.legs[3].normal_y + y_stap, mm_height)
                            self.lower_leg(self.legs[3])
                            self.voor = False
                        else:
                                           #Poten op volgorde omhoog, verplaatsen en weer naar beneden brengen

                            self.raise_leg(self.legs[2])
                            self.move_leg_lucht(self.legs[2], self.legs[2].normal_x - x_stap, self.legs[2].normal_y + y_stap, mm_height)
                            self.lower_leg(self.legs[2])

                            self.raise_leg(self.legs[0])
                            self.move_leg_lucht(self.legs[0], self.legs[0].normal_x + x_stap, self.legs[0].normal_y - y_stap, mm_height)
                            self.lower_leg(self.legs[0])

                            self.raise_leg(self.legs[3])
                            self.move_leg_lucht(self.legs[3], self.legs[3].normal_x - x_stap, self.legs[3].normal_y + y_stap, mm_height)
                            self.lower_leg(self.legs[3])

                            self.raise_leg(self.legs[1])
                            self.move_leg_lucht(self.legs[1], self.legs[1].normal_x + x_stap, self.legs[1].normal_y - y_stap, mm_height)
                            self.lower_leg(self.legs[1])


                            self.voor = True
                    else:
                        self.raise_leg(self.legs[0])
                        self.move_leg_lucht(self.legs[0], self.legs[0].normal_x + x_stap, self.legs[0].normal_y - y_stap, mm_height)
                        self.lower_leg(self.legs[0])

                        self.raise_leg(self.legs[3])
                        self.move_leg_lucht(self.legs[3], self.legs[3].normal_x - x_stap, self.legs[3].normal_y + y_stap, mm_height)
                        self.lower_leg(self.legs[3])

                        self.raise_leg(self.legs[2])
                        self.move_leg_lucht(self.legs[2], self.legs[2].normal_x - x_stap, self.legs[2].normal_y + y_stap, mm_height)
                        self.lower_leg(self.legs[2])

                        self.raise_leg(self.legs[1])
                        self.move_leg_lucht(self.legs[1], self.legs[1].normal_x + x_stap, self.legs[1].normal_y - y_stap, mm_height)
                        self.lower_leg(self.legs[1])



                #Alle poten weer terug in de normaal stand brengen
                threads = []
                max_execution = 0.0
                for leg in self.legs:
                    if leg.leg_number in [1, 2]:
                        exec_time = self.get_excution_time(leg, leg.normal_x - x_stap, leg.normal_y + y_stap, mm_height)
                        if exec_time >max_execution:
                            max_execution = exec_time
                    else:
                        exec_time = self.get_excution_time(leg, leg.normal_x + x_stap, leg.normal_y - y_stap, mm_height)
                        if exec_time >max_execution:
                            max_execution = exec_time

                for legmove in self.legs:
                    if legmove.leg_number in [1, 2]:
                        thread = threading.Thread(target=self.move_leg_stilstaand, args=(legmove, legmove.normal_x, legmove.normal_y + y_stap, mm_height,max_execution,))
                    else:
                        thread = threading.Thread(target=self.move_leg_stilstaand, args=(legmove, legmove.normal_x, legmove.normal_y - y_stap, mm_height,max_execution,))

                    threads.append(thread)

                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()
                self.last_height = height

