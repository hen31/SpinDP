__author__ = 'Robert'

from SimpleCV import *


class BalloonVision:

    def __init__(self):
        pass

    @staticmethod
    def find_red_balloon(img):
        r = img.colorDistance(Color.RED).binarize(100)
        redBlobs = r.findBlobs()

        goodRedBlobs = []
        blob = None

        if redBlobs is not None and len(redBlobs) > 0:
            #filter goede blob
            for redBlob in redBlobs:
                if redBlob.isCircle(0.80) and redBlob.area() > 1500:
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

    @staticmethod
    def find_green_balloon(img):
        g = img.hueDistance(Color.GREEN).binarize(45).erode(10)
        greenBlobs = g.findBlobs()

        goodGreenBlobs = []
        blob = None

        if greenBlobs is not None and len(greenBlobs) > 0:

            for greenBlob in greenBlobs:
                if greenBlob.isCircle(0.84) and greenBlob.area() > 1500:
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

    @staticmethod
    def find_blue_balloon(img):
        b = img.colorDistance(Color.BLUE).binarize(140)
        b.show()
        blueBlobs = b.findBlobs()

        goodBlueBlobs = []
        blob = None

        if blueBlobs is not None and len(blueBlobs) > 0:

            for blueBlob in blueBlobs:
                if blueBlob.isCircle(0.39) and blueBlob.area() > 1500:
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