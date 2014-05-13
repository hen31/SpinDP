__author__ = 'Robert'

from BalloonMode import BalloonMode
from MoveState import MoveState
from Logger import Logger
from SimpleCV import *


class SearchState:
    def __init__(self):
        self.colors = []
        self.current_color = 0

    def doe_stap(self, parameters):
        if BalloonMode.alive:
            self.colors = parameters[0]
            BalloonMode.logger.logevent("BalloonMode SearchState", "Ballonnen zoeken met de volgende volgorde",
                                        Logger.MESSAGE)
            BalloonMode.logger.logevent("BalloonMode SearchState", self.colors, Logger.MESSAGE)

            for i in xrange(0, 3):
                blob = self.find_balloon(self.colors[i])
                if blob is not False:
                    moveState = MoveState()
                    moveState.doe_stap([self.colors[i], blob])



    def find_balloon(self, color):
        BalloonMode.logger.logevent("BalloonMode SearchState", "Zoeken naar ballon " + color, Logger.MESSAGE)

        #img = Image("http://192.168.10.1:8080/?action=snapshot")
        img = Image("C:\\balloon2.jpg")

        if color == "red":
            search = self.find_red_balloon(img)

            while not search[0] and BalloonMode.alive:
                #Draai een beetje en neem een nieuwe foto
                img = Image("http://localhost:8080/?action=snapshot")
                search = self.find_red_balloon(img)

        elif color == "green":
            search = self.find_green_balloon(img)

            while not search[0] and BalloonMode.alive:
                #Draai een beetje en neem een nieuwe foto
                img = Image("http://localhost:8080/?action=snapshot")
                search = self.find_green_balloon(img)

        elif color == "blue":
            search = self.find_blue_balloon(img)

            while not search[0] and BalloonMode.alive:
                #Draai een beetje en neem een nieuwe foto
                img = Image("http://localhost:8080/?action=snapshot")
                search = self.find_blue_balloon(img)

        if not BalloonMode.alive:
            return False

        return blob


    def find_red_balloon(self, img):
        r = img.colorDistance(Color.RED).binarize(110)
        redBlobs = r.findBlobs()

        goodRedBlobs = []
        blob = None

        if redBlobs is not None and len(redBlobs) > 0:
            #filter goede blob
            for redBlob in redBlobs:
                if redBlob.isCircle(0.39) and redBlob.area() > 100:
                    goodRedBlobs.append(redBlob)

            if len(goodRedBlobs) == 0:
                found = False
            else:
                goodRedBlobs.sort(key=lambda x: x.area(), reverse=True)
                blob = goodRedBlobs[0]
                found = True

        else:
            found = False

        return [found, blob]

    def find_green_balloon(self, img):
        g = img.colorDistance((51, 194, 32)).binarize(95)  #heb nog geen groene balloons :-(
        greenBlobs = g.findBlobs()

        goodGreenBlobs = []
        blob = None

        if greenBlobs is not None and len(greenBlobs) > 0:

            for greenBlob in greenBlobs:
                if greenBlob.isCircle(0.39) and greenBlob.area() > 100:
                    goodGreenBlobs.append(greenBlob)

            if len(goodGreenBlobs) == 0:
                found = False
            else:
                goodGreenBlobs.sort(key=lambda x: x.area(), reverse=True)
                blob = goodGreenBlobs[0]
                found = True

        else:
            found = False

        return [found, blob]

    def find_blue_balloon(self, img):
        b = img.colorDistance(Color.BLUE).binarize(130)
        blueBlobs = b.findBlobs()

        goodBlueBlobs = []
        blob = None

        if blueBlobs is not None and len(blueBlobs) > 0:

            for blueBlob in blueBlobs:
                if blueBlob.isCircle(0.39) and blueBlob.area() > 100:
                    goodBlueBlobs.append(blueBlob)

            if len(goodBlueBlobs) == 0:
                found = False
            else:
                goodBlueBlobs.sort(key=lambda x: x.area(), reverse=True)
                blob = goodBlueBlobs[0]
                found = True

        else:
            found = False

        return [found, blob]