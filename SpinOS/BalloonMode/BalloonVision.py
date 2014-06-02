__author__ = 'Robert'

from SimpleCV import Image
import time

#Class die alle vision voor balloonMode bevat
class BalloonVision:

    IMAGE_URL = "http://raspberrypi:8080/?action=snapshot"

    def __init__(self):
        pass

    #Methode die een Image returned van de IMAGE_URL
    @staticmethod
    def get_image():
        return Image(BalloonVision.IMAGE_URL)

    #Methode die een ballon vind op basis van kleur en de meegegeven afbeelding
    @staticmethod
    def find_balloon(color, img, color_only=False):
        if color == "red":
            return BalloonVision.find_red_balloon(img, color_only)
        elif color == "green":
            return BalloonVision.find_green_balloon(img, color_only)
        elif color == "blue":
            return BalloonVision.find_blue_balloon(img, color_only)

    #Methode voor het zoeken van een rode ballon
    @staticmethod
    def find_red_balloon(img, color_only=False):
        #binarize waarden die afgegaan worden
        binValues = [100, 105, 110]

        #Afstand tot kleur rood (255,0,0) rgb
        r = img.colorDistance((255, 0, 0))

        #Loopen door de verschillende binarize waarden
        for i in xrange(0, len(binValues)):
            bin = r.binarize(binValues[i])

            #Blobs vinden in de afbeelding
            redBlobs = bin.findBlobs()

            goodRedBlobs = []
            blob = None
            found = False

            #Als er blobs zijn gevonden
            if redBlobs is not None and len(redBlobs) > 0:

                #Als er door een te hoge binarize value te veel blobs verschijnen, stoppen.
                if len(redBlobs) > 10:
                    break

                #filter goede blob
                for redBlob in redBlobs:

                    #De blob moet voldoen aan verschillende citerea, het moet lijken op een circle
                    if (redBlob.area() > 800 and not redBlob.isSquare(0.10) and redBlob.isCircle(0.40)) or (color_only and redBlob.area() > 20000):
                        goodRedBlobs.append(redBlob)


                if len(goodRedBlobs) == 0:
                    found = False
                else:
                    blob = goodRedBlobs[-1]
                    found = True
                    break

            else:
                found = False

        return [found, blob]

    #Methode om een groene balloon te herkennen
    @staticmethod
    def find_green_balloon(img, color_only=False):
        #binarize waarden die afgegaan worden
        binValues = [140, 145, 150, 155, 160, 165, 170]

        #Afstand tot kleur groen (0,255,0) rgb
        g = img.colorDistance((0, 255, 0))

        #Voor verschillende binarize waarden loopen
        for i in xrange(0, len(binValues)):
            bin = g.binarize(binValues[i])

            #Blobs vinden in de afbeelding
            greenBlobs = bin.findBlobs()

            goodGreenBlobs = []
            blob = None
            found = False

            #Als er blobs zijn gevonden
            if greenBlobs is not None and len(greenBlobs) > 0:
                #Als er door een te hoge binarize waarde te veel blobs zijn gevonden, stoppen.
                if len(greenBlobs) > 10:
                    break

                for greenBlob in greenBlobs:
                    #Blob moet aan verschillende citerea voldoen, het moet lijken op een circle
                    if (greenBlob.isCircle(0.40) and greenBlob.area() > 800 and not greenBlob.isSquare(0.10)) or (color_only and greenBlob.area() > 20000):
                        goodGreenBlobs.append(greenBlob)

                if len(goodGreenBlobs) == 0:
                    found = False
                else:
                    blob = goodGreenBlobs[-1]
                    found = True
                    break
            else:
                found = False

        return [found, blob]

    #Metode om een blauwe ballon te herkennen
    @staticmethod
    def find_blue_balloon(img, color_only=False):
        #Verschillende binarize waarden
        binValues = [115, 120, 125, 130, 135, 140, 145]

        #Afstand tot een blauwe kleur (0,0,255) rgb
        b = img.colorDistance((0,0,255))

        #Door de verschillende binarize waarden loopen
        for i in xrange(0, len(binValues)):
            bin = b.binarize(binValues[i])

            #Blobs vinden
            blueBlobs = bin.findBlobs()

            goodBlueBlobs = []
            blob = None
            found = False

            #Als er blobs zijn gevonden
            if blueBlobs is not None and len(blueBlobs) > 0:
                #Als er door een te hoge binarize value te veel blobs worden gevonden, stoppen
                if len(blueBlobs) > 10:
                    break

                for blueBlob in blueBlobs:
                    #Blob moet aan verschillende criterea voldoen, het moet lijken op een circle
                    if (blueBlob.isCircle(0.40) and blueBlob.area() > 800 and not blueBlob.isSquare(0.10)) or (color_only and blueBlob.area() > 20000):
                        goodBlueBlobs.append(blueBlob)

                if len(goodBlueBlobs) == 0:
                    found = False
                else:
                    blob = goodBlueBlobs[-1]
                    found = True
                    break

            else:
                found = False

        return [found, blob]