__author__ = 'Robert'

from SimpleCV import Image


class BalloonVision:

    IMAGE_URL = "http://raspberrypi:8080/?action=snapshot"

    def __init__(self):
        pass

    @staticmethod
    def get_image():
        return Image(BalloonVision.IMAGE_URL)

    @staticmethod
    def find_balloon(color, img, color_only=False):
        if color == "red":
            return BalloonVision.find_red_balloon(img, color_only)
        elif color == "green":
            return BalloonVision.find_green_balloon(img, color_only)
        elif color == "blue":
            return BalloonVision.find_blue_balloon(img, color_only)

    @staticmethod
    def find_red_balloon(img, color_only=False):
        binValues = [100, 105, 110]

        r = img.colorDistance((255, 0, 0))

        for i in xrange(0, len(binValues)):
            bin = r.binarize(binValues[i])

            redBlobs = bin.findBlobs()

            goodRedBlobs = []
            blob = None
            found = False

            if redBlobs is not None and len(redBlobs) > 0:

                if len(redBlobs) > 10:
                    break

                #filter goede blob
                for redBlob in redBlobs:

                    if (redBlob.area() > 800 and not redBlob.isSquare(0.10) and redBlob.isCircle(0.40)) or (color_only and redBlob.area() > 800):
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

    @staticmethod
    def find_green_balloon(img, color_only=False):
        binValues = [140, 145, 150, 155, 160, 165, 170]

        g = img.colorDistance((0, 255, 0))

        for i in xrange(0, len(binValues)):
            bin = g.binarize(binValues[i])

            greenBlobs = bin.findBlobs()

            goodGreenBlobs = []
            blob = None
            found = False

            if greenBlobs is not None and len(greenBlobs) > 0:
                if len(greenBlobs) > 10:
                    break

                for greenBlob in greenBlobs:
                    if (greenBlob.isCircle(0.40) and greenBlob.area() > 800 and not greenBlob.isSquare(0.10)) or (color_only and greenBlob.area()):
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

    @staticmethod
    def find_blue_balloon(img, color_only=False):
        binValues = [115, 120, 125, 130, 135, 140, 145, 150]

        b = img.colorDistance((0,0,255))

        for i in xrange(0, len(binValues)):
            bin = b.binarize(binValues[i])

            blueBlobs = bin.findBlobs()

            goodBlueBlobs = []
            blob = None
            found = False

            if blueBlobs is not None and len(blueBlobs) > 0:
                if len(blueBlobs) > 10:
                    break

                for blueBlob in blueBlobs:
                    if (blueBlob.isCircle(0.40) and blueBlob.area() > 800 and not blueBlob.isSquare(0.10)) or (color_only and blueBlob.area() > 800):
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