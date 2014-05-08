from SimpleCV import *
import FoundState
import MoveState
import os, sys
__author__ = 'Jeroen'

class SearchState:

    def __init__(self, image_path):
        self.image_path = image_path

    def search_teerbal(self):

        image_paths = [self.image_path + "\\TeerbalMode\\TestImages\\teerbal.png", self.image_path + "\\TeerbalMode\\TestImages\\vooruit.png"]
        rand = random.randrange(0,2)
        self.image = Image(image_paths[rand])

        if rand == 0:
            print "FOTO: TEERBAL"
        else:
            print "FOTO: GEEN TEERBAL"

        bin_image = self.image.colorDistance(color=Color.BLACK).binarize(20)
        bin_image.erode(2)


        blobs = bin_image.findBlobs()

        if blobs:
            blobs = blobs.filter(blobs.area() > 1000)

        #voor debugging
        #print blobs
        #index = 0
        #for b in blobs:
        #    blobs[index].show()
        #    index+=1
        #print blobs
        if blobs:
            #blobs[-1].draw()
            #bin_image.show()

            if len(blobs) >= 1:
                return True
            else:
                return False
        return False