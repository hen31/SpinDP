__author__ = 'Robert'

import threading
import pygame
import os
import time
from Logger import Logger
from BalloonVision import BalloonVision

class BalloonMode:

    #Alive variabele, alle states controleren hierop
    alive = True
    #Logger variabele
    logger = None

    #Movement handler, zo kan er gelopen worden
    movementHandler = None

    SpinOS = None

    #Constructor
    def __init__(self, movementHandler, logger, spin_os):
        #Alive aanzetten
        self.set_alive(True)
        #Logger instellen
        BalloonMode.logger = logger
        #MovementHandler instellen
        BalloonMode.movementHandler = movementHandler
        BalloonMode.SpinOS = spin_os
        #Thread opstarten
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        #Volgendee opstarten

        state = CardState(self)
        state.doe_stap([])

        #Aan het einde van alles
        BalloonMode.SpinOS.play_sound(0.5)
        time.sleep(0.2)
        BalloonMode.SpinOS.play_sound(0.5)
        time.sleep(0.2)
        BalloonMode.SpinOS.play_sound(1)

    def set_alive(self, value):
        #Alive variabele value geven
        BalloonMode.alive = value

    def process_command(self, command, message):
        pass

#In de cardstate wordt de kleurenkaart herkend
class CardState:

    LOGGER_NAME = "BalloonMode CardStateA"

    #Constructor
    def __init__(self, ballonmode):
        self.balloonmode = ballonmode
        #redImg = Image("C:\Users\Robert\Desktop\\ballon\\red.jpg")
        #greenImg = Image("C:\Users\Robert\Desktop\\ballon\\green.jpg")
        #blueImg = Image("C:\Users\Robert\Desktop\\ballon\\blue.jpg")

        #searchR = BalloonVision.find_red_balloon(redImg)
        #searchG = BalloonVision.find_green_balloon(greenImg)
        #searchB = BalloonVision.find_blue_balloon(blueImg)

        #searchR[1].show(Color.RED)
        #time.sleep(2)
        #searchG[1].show(Color.GREEN)
        #time.sleep(4)
        #searchB[1].show(Color.BLUE)
        #time.sleep(6)

        #while True:
        #    pass

        #img = BalloonVision.get_image()
        #while True:
        #    img = Image("http://raspberrypi:8080/?action=snapshot")

        #    search = BalloonVision.find_balloon("green", img)

        #    if search[0]:
        #        search[1].show()
        pass

    def doe_stap(self, parameters):
        #Balloonmode moet nog alive zijn
        if self.balloonmode.alive:
            #Kaart herkennen
            colorOrder = self.recognize_card()
            #Kleurenkaart goed herkend?
            if colorOrder is not False:
                #Geluid afspelen
                self.play_sound()

                #Volgende state opstarten
                nextState = SearchState(self.balloonmode)
                nextState.doe_stap([colorOrder])

    def recognize_card(self):
        redBlob = None
        greenBlob = None
        blueBlob = None
        blobs = None

        self.balloonmode.logger.logevent(CardState.LOGGER_NAME, "Bezig met zoeken", Logger.MESSAGE)

        #img = Image("C:\\cards\\realCard1.jpg")
        #img = Image("C:\\muur\\card.jpg")

        #Blobs uit de afbeelding herkennen
        blobs = BalloonVision.recognize_card()

        #Zolang er geen blobs zijn gevonden en we alive zijn. Door blijven zoeken
        while not blobs[0] or not blobs[1] or not blobs[2] and self.balloonmode.alive:

            blobs = BalloonVision.recognize_card()

        #Voorbij de while, kaart wordt voorgehouden. Of niet meer alive
        if not self.balloonmode.alive:
            return False

        #Blobs in variabelen zetten
        redBlob, greenBlob, blueBlob = blobs

        self.balloonmode.logger.logevent(CardState.LOGGER_NAME, "Gevonden.", Logger.MESSAGE)
        #Blobs sorteren op y (hoogte)
        blobs.sort(key=lambda x: x.y)

        return [blobs[0].Name, blobs[1].Name, blobs[2].Name]

    #Methode om het herkend geluid af te spelen
    def play_sound(self):
        BalloonMode.SpinOS.play_sound(0.5)
        time.sleep(0.1)
        BalloonMode.SpinOS.play_sound(0.5)


#In de FoundState is de ballon gevonden en wordt er gewacht todat deze kapot gaat
class FoundState:

    LOGGER_NAME = "self.balloonmode FoundState"

    def __init__(self, ballonmode):
        self.balloonmode = ballonmode
        pass

    def doe_stap(self, parameters):
        #param 0 = color

        #self.balloonmode nog wel alive
        if self.balloonmode.alive:
            self.balloonmode.logger.logevent(FoundState.LOGGER_NAME, "Vlak voor de ballon, kijken wanneer hij knapt " +parameters[0], Logger.MESSAGE)
            self.play_sound()

            not_found_count = 0

            #Not found count <= 2 en self.balloonmode nog alive
            while not_found_count <= 2 and self.balloonmode.alive:

                #Ballon nog gevonden?
                found = self.balloon_alive(parameters[0])
                if not found:
                    not_found_count += 1
                else:
                    not_found_count = 0

            if not self.balloonmode.alive:
                return

            self.balloonmode.logger.logevent(FoundState.LOGGER_NAME, "Balloon weg (geknapt)!", Logger.MESSAGE)

        return True

    #Methode die een ballon vind op basis van kleur
    def balloon_alive(self, color):
        #Afbeelding ophalen
        img = BalloonVision.get_image()

        #Blob vinden
        return BalloonVision.find_balloon(color, img, True)[0]

    #Methode om geluid af te spelen wanneer een ballon gevonden is
    def play_sound(self):
        BalloonMode.SpinOS.play_sound(2)

class MoveState:

    LOGGER_NAME = "self.balloonmode MoveState"

    def __init__(self, ballonmode):
        self.balloonmode = ballonmode
        pass

    def doe_stap(self, parameters):
        #parameters 0 = color, 1 = blob
        if self.balloonmode.alive:
            move = self.move_to_balloon(parameters[0], parameters[1])

            if move is not False:
                foundState = FoundState(self.balloonmode)
                foundState.doe_stap([parameters[0]])
        return

    def move_to_balloon(self, color, blob):
        self.balloonmode.logger.logevent(MoveState.LOGGER_NAME, "Naar ballon " + color + " lopen", Logger.MESSAGE)

        #Midden van het beeld
        center = 640 / 2

        #Draaien zodat de ballon in het midden van de camera staat
        move = self.move_balloon_to_center(blob, center, color)

        if not move:
            return False

        #loop naar de ballon
        self.balloonmode.logger.logevent(MoveState.LOGGER_NAME, "Vooruit lopen", Logger.MESSAGE)

        #Max area = 640*480 = 307200
        area = 0
        not_found_count = 0

        #vooruit lopen
        for i in xrange(0, 5):
            self.balloonmode.movementHandler.move_one_step()

        #self.balloonmode.movementHandler.move(0, 100, 0, 0)
        #time.sleep(self.balloonmode.movementHandler.TIME_MOVE_ONE_STEP * 5)
        #self.balloonmode.movementHandler.move(0, 0, 0, 0)

        while area < 300000 and self.balloonmode.alive:
            if not_found_count >= 5:
                self.balloonmode.logger.logevent(MoveState.LOGGER_NAME, color + " ballon kwijt, wat nu?!", Logger.MESSAGE)
                return False

            img = BalloonVision.get_image()
            search = BalloonVision.find_balloon(color, img, True)

            if search[0]:
                #Ballon als nodig naar het midden krijgen.
                move = self.move_balloon_to_center(search[1], center, color)
                if not move:
                    return False
                
                area = search[1].area()
                for i in xrange(0,5):
                    self.balloonmode.movementHandler.move_one_step()

                #self.balloonmode.movementHandler.move(0, 100, 0, 0)
                #time.sleep(self.balloonmode.movementHandler.TIME_MOVE_ONE_STEP * 5)
                #self.balloonmode.movementHandler.move(0, 0, 0, 0)

            else:
                not_found_count += 1

        if not self.balloonmode.alive:
            return False

        return True

    def move_balloon_to_center(self, blob, center, color):
        self.balloonmode.logger.logevent(MoveState.LOGGER_NAME, "Ballon " + color + " naar het midden bewegen", Logger.MESSAGE)
        verschil = self.diff_to_center(blob, center)
        while abs(verschil) > 100 and self.balloonmode.alive: #100 px marge voor het midden
            print "Blob nog niet in het midden"
            if verschil > 0:
                #naar links draaien
                self.balloonmode.movementHandler.move_one_turn(True)
                #self.balloonmode.movementHandler.move(0, 0, 181, 100)
                #time.sleep(self.balloonmode.movementHandler.TIME_TURN)
                #self.balloonmode.movementHandler.move(0, 0, 0, 0)
            else:
                #naar rechts draaien
                self.balloonmode.movementHandler.move_one_turn(False)
                #self.balloonmode.movementHandler.move(0, 0, 180, 100)
                #time.sleep(self.balloonmode.movementHandler.TIME_TURN)
                #self.balloonmode.movementHandler.move(0, 0, 0, 0)

            img = BalloonVision.get_image()
            search = BalloonVision.find_balloon(color, img)

            blob = search[1]

            if search[0]:
                verschil = self.diff_to_center(blob, center)

        if not self.balloonmode.alive:
            return False

        return True

    def balloon_in_center(self, blob, center, marge):
        return abs(center - blob.centroid) > marge

    def diff_to_center(self, blob, center):
        blobCenter = float(blob.bottomLeftCorner()[0]) + float(float(blob.width()) / float(2))
        return int(center) - int(blobCenter)

class SearchState:

    LOGGER_NAME = "BalloonMode SearchState"

    def __init__(self, ballonmode):
        self.balloonmode = ballonmode
        self.colors = []
        self.balloonOrder = []
        self.moveTo = None #true = left, false = right

    def doe_stap(self, parameters):
        if self.balloonmode.alive:
            self.colors = parameters[0]
            self.balloonmode.logger.logevent(SearchState.LOGGER_NAME, "Ballonnen zoeken met de volgende volgorde",
                                        Logger.MESSAGE)
            self.balloonmode.logger.logevent(SearchState.LOGGER_NAME, self.colors, Logger.MESSAGE)

            #self.balloonmode.logger.logevent(SearchState.LOGGER_NAME, "Volgorde ballonnen uit omgegving herkennen")

            #self.balloonOrder = self.get_balloon_order()
            #Lol kan gewoon hardcoded, staat in wedstrijddocument
            self.balloonOrder = ["blue", "red", "green"]

            if not self.balloonOrder:
                return

            #self.balloonmode.logger.logevent(SearchState.LOGGER_NAME, "Volgorde van ballonnen uit de omgeving: " + self.balloonOrder[0] +" " + self.balloonOrder[1] +" " +self.balloonOrder[2])



            for i in xrange(0, 3):
                if i > 0: #De spin kan rood zien bij de eerste keer
                    if self.balloonOrder.index(self.colors[i-1]) > self.balloonOrder.index(self.colors[i]):
                        #Naar links draaien
                        self.moveTo = True
                    else:
                        #Naar rechts draaien
                        self.moveTo = False
                else:
                    if self.colors[i] != "red":
                        if self.balloonOrder.index(self.colors[i]) > 1:
                            self.moveTo = False
                        else:
                            self.moveTo = True

                blob = self.find_balloon(self.colors[i])
                if blob is not False:
                    self.balloonmode.logger.logevent(SearchState.LOGGER_NAME, self.colors[i] + " gevonden!", Logger.MESSAGE)
                    moveState = MoveState(self.balloonmode)
                    moveState.doe_stap([self.colors[i], blob])

    def find_balloon(self, color):
        if not self.balloonmode.alive:
            return False

        self.balloonmode.logger.logevent(SearchState.LOGGER_NAME, "Zoeken naar ballon " + color, Logger.MESSAGE)

        img = BalloonVision.get_image()

        search = BalloonVision.find_balloon(color, img)

        while not search[0] and self.balloonmode.alive:
            if self.moveTo:
                #Beweeg naar links
                self.balloonmode.movementHandler.move_one_turn(True)
                #self.balloonmode.movementHandler.move(0, 0, 180, 100)
                #time.sleep(self.balloonmode.movementHandler.TIME_TURN * 5)
                #self.balloonmode.movementHandler.move(0, 0, 0, 0)

            elif not self.moveTo:
                #Beweeg naar rechts
                self.balloonmode.movementHandler.move_one_turn(False)
                # self.balloonmode.movementHandler.move(0, 0, 181, 100)
                # time.sleep(self.balloonmode.movementHandler.TIME_TURN * 5)
                # self.balloonmode.movementHandler.move(0, 0, 0, 0)

            img = BalloonVision.get_image()
            search = BalloonVision.find_balloon(color, img)

        if not self.balloonmode.alive:
            return False

        return search[1]

    def get_balloon_order(self):
        if not self.balloonmode.alive:
            return False

        #Alle balonnen kunnen gezien worden
        img = BalloonVision.get_image()

        red = BalloonVision.find_red_balloon(img)[1]
        green = BalloonVision.find_green_balloon(img)[1]
        blue = BalloonVision.find_blue_balloon(img)[1]

        while (red is None or green is None or blue is None) and self.balloonmode.alive:
            img = BalloonVision.get_image()
            red = BalloonVision.find_red_balloon(img)[1]
            green = BalloonVision.find_green_balloon(img)[1]
            blue = BalloonVision.find_blue_balloon(img)[1]

        if not self.balloonmode.alive:
            return False

        red.Name = "red"
        green.Name = "green"
        blue.Name = "blue"

        balloonOrder = [red, green, blue]

        balloonOrder.sort(key=lambda x: x.x)

        balloonOrder = [balloonOrder[0].Name, balloonOrder[1].Name, balloonOrder[2].Name]

        return balloonOrder