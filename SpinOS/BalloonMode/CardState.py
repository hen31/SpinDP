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

        #Get een afbeelding
        img = BalloonVision.get_image()
        #img = Image("C:\\cards\\realCard1.jpg")
        #img = Image("C:\\muur\\card.jpg")

        #Blobs uit de afbeelding herkennen
        blobs = self.getBlobs(img)

        #Zolang er geen blobs zijn gevonden en we alive zijn. Door blijven zoeken
        while blobs is False and BalloonMode.alive:

            img = BalloonVision.get_image()
            #img = Image("C:\\muur\\card.jpg")
            blobs = self.getBlobs(img)


        #Voorbij de while, kaart wordt voorgehouden. Of niet meer alive
        if not BalloonMode.alive:
            return False

        #Blobs in variabelen zetten
        redBlob, greenBlob, blueBlob = blobs

        BalloonMode.logger.logevent(CardState.LOGGER_NAME, "Gevonden.", Logger.MESSAGE)
        #Blobs sorteren op y (hoogte)
        blobs.sort(key=lambda x: x.y)

        return [blobs[0].Name, blobs[1].Name, blobs[2].Name]

    #Methode die de juiste blobs van de kleurenkaart herkend
    def getBlobs(self, img):
        #Afstand tot rood
        r = img.hueDistance(Color.RED).binarize(18)

        #Rode blobs vinden
        redBlobs = r.findBlobs()

        #Wel blobs gevonden?
        if redBlobs is None:
            return False

        goodRedBlobs = []
        #Door alle rode blobs loopen
        for i in xrange(0, len(redBlobs)):

            #Ratio berekenen
            ratio = (float(float(redBlobs[i].height())/float(redBlobs[i].width())))
            #Ratio moet tussen 0.6 en 1.2 vallen, zo vierkant mogelijk.
            if ratio > 0.6 and ratio < 1.2 and redBlobs[i].area() > 5000 :
                goodRedBlobs.append(redBlobs[i])

        if len(goodRedBlobs) == 0:
            return False

        goodRedBlobs.sort(key=lambda x: x.area(), reverse=True)
        #De juiste blob is de blob met de grootste area
        redBlob = goodRedBlobs[0]
        redBlob.Name = "red"

        #Afstand tot custom rgb groen.
        g = img.colorDistance((51, 194, 32)).binarize(105)

        #Groene blobs vinden
        greenBlobs = g.findBlobs()

        #Wel blobs gevonden?
        if greenBlobs is None:
            #Geen blob gevonden, de gewone Color.GREEN proberen ipv custom rgb
            g = img.colorDistance(Color.GREEN).binarize(60)
            #Blobs vinden
            greenBlobs = g.findBlobs()

        #Nu ook blobs gevonden?
        if greenBlobs is None:
            return False

        goodGreenBlobs = []
        #Door de groene blobs loopen
        for i in xrange(0, len(greenBlobs)):
            #Ratio van blob berekenen
            ratio = (float(float(greenBlobs[i].height())/float(greenBlobs[i].width())))
            #Blob moet op vierkant lijken ratio tussen 0.6 en 1.2
            if(ratio > 0.6 and ratio < 1.2 and greenBlobs[i].area() > 5000):
                goodGreenBlobs.append(greenBlobs[i])


        if len(goodGreenBlobs) == 0:
            #Niks gevonden, andere binarize proberen
            g = img.colorDistance(Color.GREEN).binarize(65)

            #Blobs vinden
            greenBlobs = g.findBlobs()

            #Niks gevonden?
            if greenBlobs is None:
                return False

            #Door greenBlobs loopen
            for i in xrange(0, len(greenBlobs)):
                #Ratio van blob berekenen
                ratio = (float(float(greenBlobs[i].height())/float(greenBlobs[i].width())))
                #Blob moet zo vierkant mogelijk zijn, ratio moet vallen binnen 0.6 en 1.2
                if ratio > 0.6 and ratio < 1.2 and greenBlobs[i].area() > 5000:
                    goodGreenBlobs.append(greenBlobs[i])

        if len(goodGreenBlobs) == 0:
            return False

        #Goede blobs sorteren op area
        goodGreenBlobs.sort(key=lambda x: x.area(), reverse=True)
        #Blob met de grootste area is de juiste
        greenBlob = goodGreenBlobs[0]
        greenBlob.Name = "green"

        #Afstand tot blauw
        b = img.hueDistance(Color.BLUE).binarize(70)

        #Blauwe blobs vinden
        blueBlobs = b.findBlobs()

        #Geen blobs gevonden?
        if blueBlobs is None:
            return False

        goodBlueBlobs = []

        #Door de blauwe blobs loopen
        for i in xrange(0, len(blueBlobs)):
            #ratio van blob berekenen
            ratio = (float(float(blueBlobs[i].height())/float(blueBlobs[i].width())))
            #Blob moet vierkant zijn, ratio tussen 0.6 en 1.2
            if ratio > 0.6 and ratio < 1.2 and blueBlobs[i].area() > 5000:
                goodBlueBlobs.append(blueBlobs[i])

        if len(goodBlueBlobs) == 0:
            return False

        #Goede blobs sorteren op area
        goodBlueBlobs.sort(key=lambda x: x.area(), reverse = True)
        #Juiste blob is de gene met grooste area
        blueBlob = goodBlueBlobs[0]
        blueBlob.Name = "blue"

        #Verschillende blobs returen in een lijst
        return [redBlob, greenBlob, blueBlob]

    #Methode om het herkend geluid af te spelen
    def play_sound(self):
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__) + "/Sound",'herkend.wav'))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue