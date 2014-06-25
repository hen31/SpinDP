import os
from SimpleCV import *

__author__ = 'Jeroen'

class TeerbalVision:

    IMAGE_URL = "http://raspberrypi:8080/?action=snapshot"
    MIN_AREA = 100
    MAX_AREA = 5000
    ESTIMATED_MIDDLE = 100
    #True = link, False = Rechts
    LAATST_GEDRAAID = None
    LAST_BLOB_SIZE = 0
    BLACK_THRESH = 50

    def __init__(self):
        pass

    @staticmethod
    def getImage():
        return Image(TeerbalVision.IMAGE_URL)

    #methode die de grijze afbakening herkend
    @staticmethod
    def find_top(img):
        image = img
        bin_image = image.colorDistance(Color.GRAY).binarize()
        blobs = bin_image.findBlobs(minsize=TeerbalVision.MIN_AREA,maxsize=TeerbalVision.MAX_AREA)
        y_list = sorted(blobs.y())
        return y_list[-1]

    #methode die de teerbal zoekt
    @staticmethod
    def find_teerbal(img):
        image = img
        bin_image  = image.colorDistance(Color.BLACK).binarize(TeerbalVision.BLACK_THRESH)
        blobs = bin_image.findBlobs(minsize=TeerbalVision.MIN_AREA,maxsize=TeerbalVision.MAX_AREA)

        # bin_image.show()
        # time.sleep(2)

        if blobs:
            for e in blobs:
                if not e.isRectangle(0.3) or e.width() < e.height():
                    blobs.remove(e)
            blobs = sorted(blobs,key=lambda x:(x.y, x.area()))
            if blobs:
                TeerbalVision.LAST_BLOB_SIZE = blobs[-1].area()
                return True

            # for e in blobs:
            #     e.show()
            # time.sleep(2)
            return True
        return False

    @staticmethod
    def center(img):
        image = img
        bin_image = image.colorDistance(Color.BLACK).binarize(TeerbalVision.BLACK_THRESH)
        blobs = bin_image.findBlobs(minsize=TeerbalVision.MIN_AREA, maxsize=TeerbalVision.MAX_AREA)

        if blobs:
            for e in blobs:
                if not e.isRectangle(0.3):
                    blobs.remove(e)
            blobs = sorted(blobs,key=lambda x:(x.y, x.area()))
            if blobs[-1].x > (image.width/2) - 100 and blobs[-1].x < (image.width/2) + 100:
                return True
            else:
                return False

    @staticmethod
    def turn_side(img):
        image = img
        bin_image = image.colorDistance(Color.BLACK).binarize(TeerbalVision.BLACK_THRESH)
        blobs = bin_image.findBlobs(minsize=TeerbalVision.MIN_AREA, maxsize=TeerbalVision.MAX_AREA)


        if blobs:
            for e in blobs:
                if not e.isRectangle(0.3):
                    blobs.remove(e)
            blobs = sorted(blobs,key=lambda x:(x.y, x.area()))

            if blobs[-1].x < image.width/2:
                #draai naar rechts
                return True
            elif blobs[-1].x > image.width/2:
                #draai naar links
                return False


    # @staticmethod
    # #return values representeren (Teerbal is nog in zicht, draai links, draai rechts) indien links en recht allebei False
    # #zijn dan staat de spin gecentreerd en kan hij vooruit lopen
    # def center_on_teerbal(img):
    #     image = img
    #     bin_image = image.colorDistance(Color.BLACK).binarize(TeerbalVision.BLACK_THRESH)
    #     blobs = bin_image.findBlobs(minsize=TeerbalVision.MIN_AREA, maxsize=TeerbalVision.MAX_AREA)
    #     if blobs:
    #         if blobs[-1].x > (image.width/2) - TeerbalVision.ESTIMATED_MIDDLE and blobs[-1].x < (image.width/2) + TeerbalVision.ESTIMATED_MIDDLE:
    #             TeerbalVision.LAST_BLOB_SIZE = blobs[-1].area()
    #             return (True,False,False)
    #         elif blobs[-1].x < image.width/2:
    #             #draai naar rechts
    #             TeerbalVision.LAATST_GEDRAAID = True
    #             return (True,False,True)
    #         elif blobs[-1].x > image.width/2:
    #             #draai naar links
    #             TeerbalVision.LAATST_GEDRAAID = False
    #             return (True,True,False)
    #     else:
    #         #Teerbal is verdwenen, HELP
    #         return (False,False,False)

    @staticmethod
    def teerbal_found(img):
        image = img
        bin_image = image.colorDistance(Color.BLACK).binarize(TeerbalVision.BLACK_THRESH)
        blobs = bin_image.findBlobs(minsize=TeerbalVision.MIN_AREA, maxsize=13000)
        if blobs:
            for e in blobs:
                if not e.isRectangle(0.3):
                    blobs.remove(e)
            blobs = sorted(blobs,key=lambda x:(x.y, x.area()))

            TeerbalVision.LAST_BLOB_SIZE = blobs[-1].area()
            #if blobs[-1].maxY() == 479:
             #   return True
            #else:
             #   return False
            return False

        else:
            return True





    @staticmethod
    #returns (found,verdwenen,centrated)
    def isCentrated(img):
        image = img
        bin_image = image.colorDistance(Color.BLACK).binarize(TeerbalVision.BLACK_THRESH)
        blobs = bin_image.findBlobs(minsize=TeerbalVision.MIN_AREA, maxsize=TeerbalVision.MAX_AREA)
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
            TeerbalVision.LAATST_GEDRAAID = False
            return False
        else:
            #draai links
            TeerbalVision.LAATST_GEDRAAID = True
            return True

    #debug method
    @staticmethod
    def toImage(img):
        return Image(img)
