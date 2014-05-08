from SimpleCV import *
import random
import SearchState

__author__ = 'Jeroen'

class MoveState:

    def __init__(self):
        #self.check_for_obstacle()
        pass

    def spin_lopen(self):
        pass

    def check_for_obstacle(self):
        image_path = ["C:\\Users\\Jeroen\\Documents\\GitHub\\SpinDP\\SpinOS\\TeerbalMode\\TestImages\\red bucket.png", "C:\\Users\\Jeroen\\Documents\\GitHub\\SpinDP\\SpinOS\\TeerbalMode\\TestImages\\vooruit.png"]
        rand = random.randrange(0,2)
        if rand == 0:
            print "FOTO: EMMER"
        elif rand == 1:
            print "FOTO: GEEN EMMER"
        self.image = Image(image_path[rand])

        hsv_image = self.image.toHSV()
        hsv_image = hsv_image.hueDistance(color=Color.RED).binarize(40)

        blobs = hsv_image.findBlobs()

        if blobs:
            bucket_blob = blobs.filter(blobs.area() > 1000)
            
            if len(bucket_blob) >=1:
                print "DRAAI"
                self.check_for_obstacle()
            else:
                print "VOORUIT"
        else:
            #TODO: MoveState vooruit want er is geen emmer gevonden.
            print "VOORUIT"



