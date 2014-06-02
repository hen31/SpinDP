import pygame
import os
import time
from BalloonMode import BalloonMode
from BalloonVision import BalloonVision
from Logger import Logger
from SearchState import SearchState
from SimpleCV import Image, Color

__author__ = 'Robert'


class CardState:

    LOGGER_NAME = "BalloonMode CardState"

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
        if BalloonMode.alive:
            colorOrder = self.recognize_card()
            if colorOrder is not False:
                self.play_sound()
                time.sleep(2)

                nextState = SearchState()
                nextState.doe_stap([colorOrder])

    def recognize_card(self):
        redBlob = None
        greenBlob = None
        blueBlob = None
        blobs = None

        BalloonMode.logger.logevent(CardState.LOGGER_NAME, "Bezig met zoeken", Logger.MESSAGE)

        img = BalloonVision.get_image()
        #img = Image("C:\\cards\\realCard1.jpg")
        #img = Image("C:\\muur\\card.jpg")
        blobs = self.getBlobs(img)

        while blobs is False and BalloonMode.alive:

            img = BalloonVision.get_image()
            #img = Image("C:\\muur\\card.jpg")
            blobs = self.getBlobs(img)


        #Voorbij de while, kaart wordt voorgehouden. Of niet meer alive
        if not BalloonMode.alive:
            return False

        redBlob, greenBlob, blueBlob = blobs

        BalloonMode.logger.logevent(CardState.LOGGER_NAME, "Gevonden.", Logger.MESSAGE)
        blobs.sort(key=lambda x: x.y)

        return [blobs[0].Name, blobs[1].Name, blobs[2].Name]

    def getBlobs(self, img):
        r = img.hueDistance(Color.RED).binarize(18)

        redBlobs = r.findBlobs()

        if redBlobs is None:
            return False


        goodRedBlobs = []
        for i in xrange(0, len(redBlobs)):

            ratio = (float(float(redBlobs[i].height())/float(redBlobs[i].width())))
            if ratio > 0.6 and ratio < 1.2 and redBlobs[i].area() > 5000 :
                goodRedBlobs.append(redBlobs[i])

        if len(goodRedBlobs) == 0:
            return False

        goodRedBlobs.sort(key=lambda x: x.area(), reverse=True)
        redBlob = goodRedBlobs[0]
        redBlob.Name = "red"

        g = img.colorDistance((51, 194, 32)).binarize(105)

        greenBlobs = g.findBlobs()

        if greenBlobs is None:
            g = img.colorDistance(Color.GREEN).binarize(60)
            greenBlobs = g.findBlobs()

        if greenBlobs is None:
            return False

        goodGreenBlobs = []
        for i in xrange(0, len(greenBlobs)):
            ratio = (float(float(greenBlobs[i].height())/float(greenBlobs[i].width())))
            if(ratio > 0.6 and ratio < 1.2 and greenBlobs[i].area() > 5000):
                goodGreenBlobs.append(greenBlobs[i])


        if len(goodGreenBlobs) == 0:
            g = img.colorDistance(Color.GREEN).binarize(65)

            greenBlobs = g.findBlobs()

            if greenBlobs is None:
                return False

            for i in xrange(0, len(greenBlobs)):
                ratio = (float(float(greenBlobs[i].height())/float(greenBlobs[i].width())))
                if ratio > 0.6 and ratio < 1.2 and greenBlobs[i].area() > 5000:
                    goodGreenBlobs.append(greenBlobs[i])

        if len(goodGreenBlobs) == 0:
            return False

        goodGreenBlobs.sort(key=lambda x: x.area(), reverse=True)
        greenBlob = goodGreenBlobs[0]
        greenBlob.Name = "green"

        b = img.hueDistance(Color.BLUE).binarize(70)

        blueBlobs = b.findBlobs()

        if blueBlobs is None:
            return False

        goodBlueBlobs = []

        for i in xrange(0, len(blueBlobs)):
            ratio = (float(float(blueBlobs[i].height())/float(blueBlobs[i].width())))
            if ratio > 0.6 and ratio < 1.2 and blueBlobs[i].area() > 5000:
                goodBlueBlobs.append(blueBlobs[i])

        if len(goodBlueBlobs) == 0:
            return False

        goodBlueBlobs.sort(key=lambda x: x.area(), reverse = True)
        blueBlob = goodBlueBlobs[0]
        blueBlob.Name = "blue"

        return [redBlob, greenBlob, blueBlob]

    def play_sound(self):
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__) + "/Sound",'herkend.wav'))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue