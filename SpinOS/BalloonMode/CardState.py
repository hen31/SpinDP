__author__ = 'Robert'

from BalloonMode import BalloonMode
from SearchState import SearchState
from SimpleCV import *

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

        #img = Image("http://localhost:8080/?action=snapshot")
        cam = Camera(0, {"width": 1920, "height": 1080})
        img = cam.getImage()

        blobs = self.getBlobs(img)
        redBlob, greenBlob, blueBlob = blobs

        while redBlob.area() < 30000 or greenBlob.area() < 30000 or blueBlob.area() < 30000 and BalloonMode.alive:
            print "Nog niets gevonden"

            #img = Image("http://localhost:8080/?action=snapshot")

            cam = Camera(0, {"width": 1920, "height": 1080})
            img = cam.getImage()
            blobs = self.getBlobs(img)
            print blobs
            redBlob, greenBlob, blueBlob = blobs

        #Voorbij de while, kaart wordt voorgehouden. Of niet meer alive
        if not BalloonMode.alive:
            return False

        print "Gevonden."
        print redBlob.y
        print greenBlob.y
        print blueBlob.y
        print "\n"
        print redBlob.area()
        print greenBlob.area()
        print blueBlob.area()
        blobs.sort(key=lambda x: x.y)

        return [blobs[0].Name, blobs[1].Name, blobs[2].Name]

    def getBlobs(self, img):
        r = img.hueDistance(Color.RED).binarize(10)
        redBlobs = r.findBlobs()

        g = img.hueDistance(Color.GREEN)
        g = g.binarize(90)

        greenBlobs = g.findBlobs()

        b = img.hueDistance(Color.BLUE)
        b = b.binarize()
        blueBlobs = b.findBlobs()

        redBlob = redBlobs[len(redBlobs) -1]
        redBlob.Name = "red"
        greenBlob = greenBlobs[len(greenBlobs) -1]
        greenBlob.Name = "green"
        blueBlob = blueBlobs[len(blueBlobs) -1]
        blueBlob.Name = "blue"

        return [redBlob, greenBlob, blueBlob]