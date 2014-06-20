import os
from SimpleCV import *

__author__ = 'Jeroen'

class TeerbalVision:

    IMAGE_URL = "http://raspberrypi:8080/?action=snapshot"

    ESTIMATED_MIDDLE = 30
    #True = link, False = Rechts
    LAATST_GEDRAAID = None
    LAST_BLOB_SIZE = 0

    def __init__(self):
        pass

    @staticmethod
    def getImage():
        return Image(TeerbalVision.IMAGE_URL)

    #methode die de rode afbakening herkend
    @staticmethod
    def find_top(img):
        image = Image(img)
        bin_image = image.colorDistance(Color.RED).binarize()
        blobs = bin_image.findBlobs(minsize=3000)
        y_list = sorted(blobs.y())
        return y_list[-1]

    #methode die de teerbal zoekt
    @staticmethod
    def find_teerbal(img):
        image = Image(img)
        bin_image  = image.colorDistance(Color.BLACK).binarize(50)
        blobs = bin_image.findBlobs(minsize=3000)

        # bin_image.show()
        # time.sleep(2)
        if blobs:
            # for e in blobs:
            #     e.show()
            # time.sleep(2)
            return True
        return False

    @staticmethod
    #return values representeren (Teerbal is nog in zicht, draai recht, draai links) indien links en recht allebei False
    #zijn dan staat de spin gecentreerd en kan hij vooruit lopen
    def center_on_teerbal(img):
        image = Image(img)
        bin_image = image.colorDistance(Color.BLACK).binarize(50)
        blobs = bin_image.findBlobs()
        if blobs:
            if blobs[-1].x > (image.width/2) - TeerbalVision.ESTIMATED_MIDDLE and blobs[-1].x < (image.width/2) + TeerbalVision.ESTIMATED_MIDDLE:
                TeerbalVision.LAST_BLOB_SIZE = blobs[-1].area()
                return (True,False,False)
            elif blobs[-1].x < image.width:
                #draai naar links
                TeerbalVision.LAATST_GEDRAAID = True
                return (True,False,True)
            elif blobs[-1].x > image.width:
                #draai naar rechts
                TeerbalVision.LAATST_GEDRAAID = False
                return (True,True,False)
        else:
            #Teerbal is verdwenen, HELP
            return (False,False,False)

    @staticmethod
    def teerbal_found(img):
        image = Image(img)
        bin_image = image.colorDistance(Color.BLACK).binarize(50)
        blobs = bin_image.findBlobs()
        if blobs:
            if blobs[-1].onImageEdge(tolerance=1):
                return (False,True)
            else:
                return (False,False)
        else:
            return (True,False)





    @staticmethod
    #returns (found,verdwenen,centrated)
    def isCentrated(img):
        image = Image(img)

        bin_image = image.colorDistance(Color.BLACK).binarize(50)
        blobs = bin_image.findBlobs()
        if blobs:
            cor = blobs[-1].bottomLeftCorner()
            y = cor[1]
            if blobs[-1].x > (image.width/2) - TeerbalVision.ESTIMATED_MIDDLE and blobs[-1].x < (image.width/2) + TeerbalVision.ESTIMATED_MIDDLE:
                TeerbalVision.LAST_BLOB_SIZE = blobs[-1].area()
                if y > 450:
                    return (True,False,True)
                else:
                    return (False, False,True)
            else:
                TeerbalVision.LAST_BLOB_SIZE = blobs[-1].area()
                if y > 450:
                    return (True, False, False)
                else:
                    return (False,False,False)
        #er ligt geen teerbal meer!
        return (False,True,False)

    @staticmethod
    def lost():
        if TeerbalVision.LAATST_GEDRAAID:
            #draai rechts
            return False
        else:
            #draai links
            return True

    #debug method
    @staticmethod
    def toImage(img):
        return Image(img)
