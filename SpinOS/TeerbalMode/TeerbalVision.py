import os
from SimpleCV import *

__author__ = 'Jeroen'

class TeerbalVision:

    def __init__(self):
        pass

    @staticmethod
    def find_top(image):
        bin_image = image.colorDistance(Color.RED).binarize()
        blobs = bin_image.findBlobs(minsize=3000)
        y_list = sorted(blobs.y())
        return y_list[-1]

    @staticmethod
    def find_teerbal(image, check_for_neigbours = False):
        image = Image(image)
        max_y = TeerbalVision.find_top(image)
        bin_image = image.colorDistance(Color.BLACK).binarize()
        blobs = bin_image.findBlobs(minsize=8000)
        inside_blobs = blobs.inside((180,max_y,450,480))
        print inside_blobs
        overlap_blobs = []


        for e in blobs:
            if (e.x - e.width()/2) < 180 and e.x + e.width()/2>180 and e.y - e.height()/2 > max_y:
                overlap_blobs.append(e)

        #return een bool list als er op buren moet worden gecontroleerd,
        #anders alleen een bool die aangeefrt of er een teerbal is gevonden
        if check_for_neigbours:
            if inside_blobs:
                return (True,False)
            elif overlap_blobs:
                return (True,True)
            #er zijn geen teerballen gevonden
            return (False,False)
        #er word niet gekeken of er buren zijn
        if inside_blobs:
            return True
        elif overlap_blobs:
            return True
        #er zijn geen teerballen gevonden
        return False


    @staticmethod
    def foto_array():
        simulateArray = [[0 for xs in xrange(15)] for xs in xrange(8)]
        for y in xrange(0,len(simulateArray)):
            for x in xrange(0,len(simulateArray[y])):
                simulateArray[y][x] = e = os.path.join(os.path.dirname(__file__) + "/TestImages",'vooruit.png')

        simulateArray[0][2] = os.path.join(os.path.dirname(__file__) + "/TestImages",'boven rood.jpg')
        simulateArray[1][2] = os.path.join(os.path.dirname(__file__) + "/TestImages",'boven rood.jpg')
        simulateArray[3][3] = os.path.join(os.path.dirname(__file__) + "/TestImages",'boven rood.jpg')
        return simulateArray