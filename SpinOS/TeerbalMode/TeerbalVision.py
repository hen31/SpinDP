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
        blobs = blobs.inside((180,max_y,450,480))
        print blobs

        if blobs:
            if check_for_neigbours:
                blobs.overlaps()
            else:
                return True
        return False

    @staticmethod
    def foto_array():
        simulateArray = [[0 for xs in xrange(15)] for xs in xrange(8)]
        for y in xrange(0,len(simulateArray)):
            for x in xrange(0,len(simulateArray[y])):
                simulateArray[y][x] = e = os.path.join(os.path.dirname(__file__) + "/TestImages",'vooruit.png')

        simulateArray[0][5] = os.path.join(os.path.dirname(__file__) + "/TestImages",'boven rood.jpg')
        simulateArray[1][5] = os.path.join(os.path.dirname(__file__) + "/TestImages",'boven rood.jpg')
        simulateArray[4][14] = os.path.join(os.path.dirname(__file__) + "/TestImages",'boven rood.jpg')
        return simulateArray