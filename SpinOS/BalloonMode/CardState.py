import pygame
import os
import time
from BalloonMode import BalloonMode
from BalloonVision import BalloonVision
from Logger import Logger
from SearchState import SearchState
from SimpleCV import Image, Color

__author__ = 'Robert'

#In de cardstate wordt de kleurenkaart herkend
class CardState:

    LOGGER_NAME = "BalloonMode CardState"

    #Constructor
    def __init__(self):
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
        if BalloonMode.alive:
            #Kaart herkennen
            colorOrder = self.recognize_card()
            #Kleurenkaart goed herkend?
            if colorOrder is not False:
                #Geluid afspelen
                self.play_sound()
                time.sleep(2)

                #Volgende state opstarten
                nextState = SearchState()
                nextState.doe_stap([colorOrder])

    def recognize_card(self):
        redBlob = None
        greenBlob = None
        blueBlob = None
        blobs = None

        BalloonMode.logger.logevent(CardState.LOGGER_NAME, "Bezig met zoeken", Logger.MESSAGE)

        #img = Image("C:\\cards\\realCard1.jpg")
        #img = Image("C:\\muur\\card.jpg")

        #Blobs uit de afbeelding herkennen
        blobs = BalloonVision.recognize_card()

        #Zolang er geen blobs zijn gevonden en we alive zijn. Door blijven zoeken
        while not blobs[0] or not blobs[1] or not blobs[2] and BalloonMode.alive:

            blobs = BalloonVision.recognize_card()

        #Voorbij de while, kaart wordt voorgehouden. Of niet meer alive
        if not BalloonMode.alive:
            return False

        #Blobs in variabelen zetten
        redBlob, greenBlob, blueBlob = blobs

        BalloonMode.logger.logevent(CardState.LOGGER_NAME, "Gevonden.", Logger.MESSAGE)
        #Blobs sorteren op y (hoogte)
        blobs.sort(key=lambda x: x.y)

        return [blobs[0].Name, blobs[1].Name, blobs[2].Name]

    #Methode om het herkend geluid af te spelen
    def play_sound(self):
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__) + "/Sound",'herkend.wav'))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue