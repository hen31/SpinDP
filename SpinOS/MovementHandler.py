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



    min_height_mm = 75
    max_height_mm = 175

    min_knee_degrees = 50

    max_internal_degrees = 60
    time_per_degrees = 0.01
    min_exec_time = 0.05
    stap_uitslag = 100
    stap_uitslag_y = 50

    max_uitslag_x_voor = 50
    max_uitslag_x_midden = 50
    max_uitslag_x_achter = 50

    max_uitslag_y_voor = 50
    max_uitslag_y_midden = 50
    max_uitslag_y_achter = 50

    raise_leg_angle = 10

    TIME_TURN_PER_DEGREE = 2
    TIME_MOVE_ONE_CM =2

    PWM_FREQ = 50
    def __init__(self):
        self.pwm = PWM(0x40)                # PWM for the first servo controller
        self.pwm.setPWMFreq(MovementHandler.PWM_FREQ)    # Set frequency to 50 Hz
        self.pwm2 = PWM(0x41)               # PWM for the first servo controller
        self.pwm2.setPWMFreq(53)   # Set frequency to 50 Hz
        self.legs = [Leg(1, self.pwm), Leg(2, self.pwm), Leg(3, self.pwm), Leg(4, self.pwm2), Leg(5, self.pwm2), Leg(6, self.pwm2)]
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
        return math.degrees(float(degrees))


    def get_gammma_angle(self, x, y):
        if y == 0:
            return math.pi/2.0
        return math.atan((float(x) / float(y)))

    def get_angles(self, y, x, z):

        gamma = self.get_gammma_angle(x, y)
        L1 = math.sqrt((x*x)+(y*y))
        L = math.sqrt((float(z) * float(z)) + math.pow((L1 - Leg.COXA), 2))

        z_div_L =float(z) / float(L)
        if z_div_L < -1.0:
            z_div_L = -1
        elif z_div_L > 1.0:
            z_div_L = 1.0
        a1 = math.acos(z_div_L)

        tibia2 = Leg.TIBIA * Leg.TIBIA
        #print((tibia2 - (Leg.FEMUR * Leg.FEMUR) - (L * L)) / (-2 * Leg.FEMUR * L))
        sum = (tibia2 - (Leg.FEMUR * Leg.FEMUR) - (L * L)) / (-2 * Leg.FEMUR * L)
        if sum < -1.0:
            sum = -1
        elif sum > 1.0:
            sum = 1.0
        a2 = math.acos(sum)
        a = a1 + a2
        sum = ((L * L) - (Leg.TIBIA * Leg.TIBIA) - (Leg.FEMUR * Leg.FEMUR)) / (-2 * Leg.TIBIA * Leg.FEMUR)
        if sum < -1.0:
            sum = -1
        elif sum > 1.0:
            sum = 1.0
        beta = math.acos(sum)
        gamma =math.degrees(gamma)
        if gamma <0:
            gamma += 180
        return (math.degrees(a), math.degrees(beta), gamma)


    def kalibreren(self):
        for i in [1]: #,4, 2, 5, 3, 6]:
            leg = self.legs[i-1]
            leg.last_x = 0
            leg.last_y = 150
            leg.last_z = MovementHandler.min_height_mm
            alpha, beta, gamma = self.get_angles(200, 150, MovementHandler.min_height_mm)
            leg.set_height(alpha+30)
            time.sleep(0.5)
            leg.set_hip(gamma)
            leg.set_knee(beta)
            time.sleep(0.5)

        time.sleep(0.5)
        for i in [1]:# , 4, 2, 5, 3, 6]:
            leg = self.legs[i-1]
            alpha, beta, gamma = self.get_angles(0, 150, MovementHandler.min_height_mm)
            leg.set_height(alpha+30)
            time.sleep(0.5)
            leg.set_hip(gamma)
            leg.set_knee(beta)
            time.sleep(0.5)
            leg.set_height(alpha)
            time.sleep(2)

    def raise_leg(self, leg):
        print("raise leg")
        if leg.leg_number >=1 and leg.leg_number<=3:
            self.group2_mutex.acquire()
        if leg.leg_number >=4 and leg.leg_number<=6:
            self.group_mutex.acquire()
        alpha, beta, gamma = self.get_angles(leg.last_x, leg.last_y, leg.last_z)

        dif_alpha = (leg.get_height() - (alpha + MovementHandler.raise_leg_angle))
        dif_gamma = (leg.get_hip() - gamma)
        dif_beta = (leg.get_knee() - beta)
        leg.set_height(alpha + MovementHandler.raise_leg_angle )
        leg.set_hip(gamma)
        leg.set_knee(beta)
        max_dif = max([dif_alpha, dif_gamma, dif_beta])

        excution_time=max_dif * MovementHandler.time_per_degrees
        excution_time = math.fabs(excution_time)
        if excution_time < MovementHandler.min_exec_time:
            excution_time = MovementHandler.min_exec_time

        time.sleep(excution_time)


    def lower_leg(self, leg):
        print("lower leg")
        alpha, beta, gamma = self.get_angles(leg.last_x, leg.last_y, leg.last_z)

        dif_alpha = (leg.get_height() - (alpha - MovementHandler.raise_leg_angle ))
        dif_gamma = (leg.get_hip() - gamma)
        dif_beta = (leg.get_knee() - beta)
        leg.set_height(alpha - MovementHandler.raise_leg_angle )
        leg.set_hip(gamma)
        leg.set_knee(beta)
        max_dif = max([dif_alpha, dif_gamma, dif_beta])

        excution_time=max_dif * MovementHandler.time_per_degrees
        excution_time = math.fabs(excution_time)
        if excution_time < MovementHandler.min_exec_time:
            excution_time = MovementHandler.min_exec_time

        time.sleep(excution_time)
        if leg.leg_number >=1 and leg.leg_number<=3:
            self.group_mutex.release()
        if leg.leg_number >=4 and leg.leg_number<=6:
            self.group2_mutex.release()


    def move_leg_lucht(self, leg, x , y, z):
        print("move lucht")
        x_dif = x  - leg.last_x
        y_dif = y - leg.last_y
        alpha, beta, gamma = self.get_angles(x_dif+ leg.last_x, y_dif+leg.last_y, z)
        dif_alpha = (leg.get_height() - alpha)
        dif_gamma = (leg.get_hip() - gamma)
        dif_beta = (leg.get_knee() - beta)
        leg.set_height(alpha + MovementHandler.raise_leg_angle )
        leg.set_hip(gamma)
        leg.set_knee(beta)

        max_dif = max([dif_alpha, dif_gamma, dif_beta])

        excution_time=max_dif * MovementHandler.time_per_degrees
        excution_time = math.fabs(excution_time)
        if excution_time < MovementHandler.min_exec_time:
            excution_time = MovementHandler.min_exec_time

        time.sleep(excution_time)
        #time.sleep(MovementHandler.min_exec_time)
        leg.last_y += y_dif
        leg.last_x += x_dif
        leg.last_z = z
		



    def move_leg_stilstaand(self, leg, x , y, z):
        print("move stilstaand")
        x_dif = x  - leg.last_x
        aantal_stappen = int(math.fabs(x_dif / 20)) + 1
        if aantal_stappen >15:
            aantal_stappen = 15
        #print(aantal_stappen)
        #x = 125
        #y = 150

        #print(x_dif)#-150
        x_stap = x_dif / aantal_stappen
        y_dif = y - leg.last_y
        #print(y_dif)
        y_stap =  y_dif /aantal_stappen
        #print((leg.last_x +x_dif))
        for i in range(1, aantal_stappen + 1):
            alpha, beta, gamma = self.get_angles((x_stap * i)+ leg.last_x, (y_stap * i)+leg.last_y, z)
            #print(alpha)
            #print(beta)
            #print(gamma)
            #dif_alpha = (leg.get_height() - alpha)
            dif_gamma = (leg.get_hip() - gamma)
            dif_beta = (leg.get_knee() - beta)
           # leg.set_height(alpha)
            leg.set_hip(gamma)
            leg.set_knee(beta)

            max_dif = max([dif_gamma, dif_beta])

            excution_time=max_dif * MovementHandler.time_per_degrees
            excution_time = math.fabs(excution_time)
            if excution_time < MovementHandler.min_exec_time:
                excution_time = MovementHandler.min_exec_time

            time.sleep(excution_time)
        #time.sleep(MovementHandler.min_exec_time)
        leg.last_y += y_dif
        leg.last_x += x_dif
        leg.last_z = z


    def movement(self):
        self.kalibreren()
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
            if power_move != 0 or power_turn != 0 or height != self.last_height:
                y = int((((float(power_internal) * math.cos(self.degrees_to_radians(degrees_internal))) + 100) / 2)) - 50 #-50  - 50
                mm_height = MovementHandler.min_height_mm + (float(MovementHandler.max_height_mm - MovementHandler.min_height_mm) / float(100)) * float(height)
                z_mm_front = mm_height
                z_mm_front += (float(MovementHandler.max_height_mm - mm_height) / float(100)) * y

                z_mm_middle = mm_height

                z_mm_back = mm_height
                z_mm_back -= (float(MovementHandler.max_height_mm - mm_height) / float(100)) * y

                rad = math.radians(float(degrees_move))
                #print("rad")
                #print(rad)
                #print("degree")
                #print(degrees_move)
                y_stap = math.sin(rad) * MovementHandler.stap_uitslag_y
                x_stap = math.cos(rad) * MovementHandler.stap_uitslag
                if power_move == 0:
                    x_stap = 0
                    y_stap = 0
                #print(x_stap)
                rechtsom = False
                if degrees_turn <= 180:
                    power_turn = degrees_turn
                else:
                    power_turn = 360 - degrees_turn
                    rechtsom = True

                leg_front_x_turn = (float(power_turn) / float(100)) * MovementHandler.max_uitslag_x_voor
                leg_front_y_turn = (float(power_turn) / float(100)) * MovementHandler.max_uitslag_y_voor
                leg_middle_x_turn = (float(power_turn) / float(100)) * MovementHandler.max_uitslag_x_midden
                leg_middle_y_turn = (float(power_turn) / float(100)) * MovementHandler.max_uitslag_y_midden
                leg_back_x_turn = (float(power_turn) / float(100)) * MovementHandler.max_uitslag_x_achter
                leg_back_y_turn = (float(power_turn) / float(100)) * MovementHandler.max_uitslag_y_achter

                if rechtsom:
                    left_front_x = x_stap + leg_front_x_turn
                    left_front_y = y_stap + leg_front_y_turn
                    right_front_x = x_stap - leg_front_x_turn
                    right_front_y = y_stap - leg_front_y_turn

                    left_middle_x = x_stap - leg_middle_x_turn
                    left_middle_y = y_stap - leg_middle_y_turn
                    right_middle_x = x_stap + leg_middle_x_turn
                    right_middle_y = y_stap + leg_middle_y_turn

                    left_back_x = x_stap - leg_back_x_turn
                    left_back_y = y_stap - leg_back_y_turn
                    right_back_x = x_stap + leg_back_x_turn
                    right_back_y = y_stap + leg_back_y_turn
                else:
                    left_front_x = x_stap - leg_front_x_turn
                    left_front_y = y_stap - leg_front_y_turn
                    right_front_x = x_stap + leg_front_x_turn
                    right_front_y = y_stap + leg_front_y_turn

                    left_middle_x = x_stap + leg_middle_x_turn
                    left_middle_y = y_stap + leg_middle_y_turn
                    right_middle_x = x_stap - leg_middle_x_turn
                    right_middle_y = y_stap - leg_middle_y_turn

                    left_back_x = x_stap + leg_back_x_turn
                    left_back_y = y_stap + leg_back_y_turn
                    right_back_x = x_stap - leg_back_x_turn
                    right_back_y = y_stap - leg_back_y_turn


                #print(left_front_x)
                threads = []
                #print(self.last_x)

                new_x = self.legs[0].normal_x + left_front_x

                new_y = self.legs[0].normal_y + left_front_y
                # groep 1: 1,5,3
                # groep 2: 4,2,6
                if self.stand_gait == 1:
                    poot1_thread = threading.Thread(target=self.raise_leg, args=(self.legs[0],))
                    threads.append(poot1_thread)
                    poot3_thread = threading.Thread(target=self.raise_leg, args=(self.legs[2],))
                    threads.append(poot3_thread)
                    poot5_thread = threading.Thread(target=self.raise_leg, args=(self.legs[4],))
                    threads.append(poot5_thread)
                    self.stand_gait += 1

                elif self.stand_gait == 2:
                    poot1_thread = threading.Thread(target=self.move_leg_lucht, args=(self.legs[0],self.legs[0].normal_x + left_front_x,self.legs[0].normal_y + left_front_y, z_mm_front ))
                    threads.append(poot1_thread)
                    poot3_thread = threading.Thread(target=self.move_leg_lucht, args=(self.legs[2], self.legs[2].normal_x + left_back_x,self.legs[2].normal_y + left_back_y, z_mm_middle))
                    threads.append(poot3_thread)
                    poot5_thread = threading.Thread(target=self.move_leg_lucht, args=(self.legs[4], self.legs[4].normal_x - right_middle_x,self.legs[4].normal_y + right_middle_y, z_mm_back))
                    threads.append(poot5_thread)
                    self.stand_gait += 1

                elif self.stand_gait == 3:
                    #poot 1 naar beneden
                    poot1_thread = threading.Thread(target=self.lower_leg, args=(self.legs[0],))
                    threads.append(poot1_thread)
                    poot3_thread = threading.Thread(target=self.lower_leg, args=(self.legs[2],))
                    threads.append(poot3_thread)
                    poot5_thread = threading.Thread(target=self.lower_leg, args=(self.legs[4],))
                    threads.append(poot5_thread)


                    #poten 2 omhoog na poten 1 naar beneden
                    poot2_thread = threading.Thread(target=self.raise_leg, args=(self.legs[1],))
                    threads.append(poot2_thread)
                    poot4_thread = threading.Thread(target=self.raise_leg, args=(self.legs[3],))
                    threads.append(poot4_thread)
                    poot6_thread = threading.Thread(target=self.raise_leg, args=(self.legs[5],))
                    threads.append(poot6_thread)
                    self.stand_gait += 2
                elif self.stand_gait == 5:
                    #poten 2 naar voren
                    poot2_thread = threading.Thread(target=self.move_leg_lucht, args=(self.legs[1],self.legs[0].normal_x + left_front_x,self.legs[0].normal_y + left_front_y, z_mm_middle))
                    threads.append(poot2_thread)
                    poot4_thread = threading.Thread(target=self.move_leg_lucht, args=(self.legs[3], self.legs[2].normal_x + left_back_x,self.legs[2].normal_y + left_back_y, z_mm_front))
                    threads.append(poot4_thread)
                    poot6_thread = threading.Thread(target=self.move_leg_lucht, args=(self.legs[5], self.legs[4].normal_x - right_middle_x,self.legs[4].normal_y + right_middle_y, z_mm_back))
                    threads.append(poot6_thread)

                    #poten 1 naar nul stand
                    poot1_thread = threading.Thread(target=self.move_leg_stilstaand, args=(self.legs[0], self.legs[0].normal_x, self.legs[0].normal_y, z_mm_front  ))
                    threads.append(poot1_thread)
                    poot3_thread = threading.Thread(target=self.move_leg_stilstaand, args=(self.legs[2], self.legs[2].normal_x, self.legs[2].normal_y, z_mm_middle))
                    threads.append(poot3_thread)
                    poot5_thread = threading.Thread(target=self.move_leg_stilstaand, args=(self.legs[4], self.legs[4].normal_x, self.legs[4].normal_y, z_mm_back))
                    threads.append(poot5_thread)
                    self.stand_gait +=1
                elif self.stand_gait == 6:
                    #poten 2 naar beneden
                    poot2_thread = threading.Thread(target=self.lower_leg, args=(self.legs[1],))
                    threads.append(poot2_thread)
                    poot4_thread = threading.Thread(target=self.lower_leg, args=(self.legs[3],))
                    threads.append(poot4_thread)
                    poot6_thread = threading.Thread(target=self.lower_leg, args=(self.legs[5],))
                    threads.append(poot6_thread)

                    #poten 1 omhoog na poten 2 naar beneden
                    poot1_thread = threading.Thread(target=self.raise_leg, args=(self.legs[0],))
                    threads.append(poot1_thread)
                    poot3_thread = threading.Thread(target=self.raise_leg, args=(self.legs[2],))
                    threads.append(poot3_thread)
                    poot5_thread = threading.Thread(target=self.raise_leg, args=(self.legs[4],))
                    threads.append(poot5_thread)
                    self.stand_gait += 1
                elif self.stand_gait == 7:
                    #poten 2 nul stand
                    poot2_thread = threading.Thread(target=self.move_leg_stilstaand, args=(self.legs[1], self.legs[1].normal_x, self.legs[1].normal_y, z_mm_middle  ))
                    threads.append(poot2_thread)
                    poot4_thread = threading.Thread(target=self.move_leg_stilstaand, args=(self.legs[3], self.legs[3].normal_x, self.legs[3].normal_y, z_mm_front  ))
                    threads.append(poot4_thread)
                    poot6_thread = threading.Thread(target=self.move_leg_stilstaand, args=(self.legs[5], self.legs[5].normal_x, self.legs[5].normal_y, z_mm_back  ))
                    threads.append(poot6_thread)

                    #poten 1 naar voren
                    poot1_thread = threading.Thread(target=self.move_leg_lucht, args=(self.legs[0],self.legs[0].normal_x + left_front_x,self.legs[0].normal_y + left_front_y, z_mm_front))
                    threads.append(poot1_thread)
                    poot3_thread = threading.Thread(target=self.move_leg_lucht, args=(self.legs[2], self.legs[2].normal_x + left_back_x,self.legs[2].normal_y + left_back_y, z_mm_middle ))
                    threads.append(poot3_thread)
                    poot5_thread = threading.Thread(target=self.move_leg_lucht, args=(self.legs[4], self.legs[4].normal_x - right_middle_x,self.legs[4].normal_y + right_middle_y, z_mm_back))
                    threads.append(poot5_thread)
                    self.stand_gait = 3


                for t in threads:
                    t.start()
                
                print("start")

                for t in threads:
                    t.join()
                print("join")
            self.last_height = height




