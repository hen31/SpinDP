from BalloonMode import BalloonMode
from Logger import Logger
from SearchState import SearchState
from SimpleCV import *

__author__ = 'Robert'

class CardState:

    def __init__(self):
        pass

    def doe_stap(self, parameters):
        if BalloonMode.alive:
            colorOrder = self.recognize_card()
            if colorOrder:
                nextState = SearchState()
                nextState.doe_stap([colorOrder])

    def recognize_card(self):
        redBlob = None
        greenBlob = None
        blueBlob = None
        blobs = None

        img = Image("http://localhost:8080/?action=snapshot")

        #img = Image("C:\\realCard1.jpg")
        blobs = self.getBlobs(img)

        while blobs == False and BalloonMode.alive:
            BalloonMode.logger.logevent("BalloonMode CardState", "Nog niets gevonden", Logger.MESSAGE)

            img = Image("http://localhost:8080/?action=snapshot")
            #img = Image("C:\\realCard1.jpg")

        #Voorbij de while, kaart wordt voorgehouden. Of niet meer alive
        if not BalloonMode.alive:
            return False

        redBlob, greenBlob, blueBlob = blobs

        BalloonMode.logger.logevent("BalloonMode CardSate", "Gevonden.", Logger.MESSAGE)
        blobs.sort(key=lambda x: x.y)

        return [blobs[0].Name, blobs[1].Name, blobs[2].Name]

    def getBlobs(self, img):
        r = img.hueDistance(Color.RED).binarize(18)
        redBlobs = r.findBlobs()

        if redBlobs == None:
            return False

        goodRedBlobs = []
        for i in xrange(0, len(redBlobs)):
            ratio = (float(float(redBlobs[i].height())/float(redBlobs[i].width())))
            if(ratio > 0.6 and ratio < 1.2 and redBlobs[i].area() > 2000):
                goodRedBlobs.append(redBlobs[i])

        if len(goodRedBlobs) == 0:
            return False

        goodRedBlobs.sort(key=lambda x: x.area(), reverse = True)
        redBlob = goodRedBlobs[0]
        redBlob.Name = "red"

        g = img.colorDistance((51,194,32)).binarize(95)
        greenBlobs = g.findBlobs()

        if greenBlobs == None:
            return False

        goodGreenBlobs = []
        for i in xrange(0, len(greenBlobs)):
            ratio = (float(float(greenBlobs[i].height())/float(greenBlobs[i].width())))
            if(ratio > 0.6 and ratio < 1.2 and greenBlobs[i].area() > 2000):
                goodGreenBlobs.append(greenBlobs[i])

        if len(goodGreenBlobs) == 0:
            return False

        goodGreenBlobs.sort(key=lambda x: x.area(), reverse = True)
        greenBlob = greenBlobs[0]
        greenBlob.Name = "green"

        b = img.hueDistance(Color.BLUE).binarize(60)
        blueBlobs = b.findBlobs()

        if blueBlobs == None:
            return False

        goodBlueBlobs = []

        for i in xrange(0, len(blueBlobs)):
            ratio = (float(float(blueBlobs[i].height())/float(blueBlobs[i].width())))
            if(ratio > 0.6 and ratio < 1.2 and blueBlobs[i].area() > 2000):
                goodBlueBlobs.append(blueBlobs[i])

        if len(goodBlueBlobs) == 0:
            return False

        goodBlueBlobs.sort(key=lambda x: x.area(), reverse = True)
        blueBlob = goodBlueBlobs[0]
        blueBlob.Name = "blue"

        return [redBlob, greenBlob, blueBlob]