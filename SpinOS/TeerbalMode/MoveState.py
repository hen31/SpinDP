from SimpleCV import *
import random
import SearchState


__author__ = 'Jeroen'

class MoveState:

    def __init__(self):
        #self.image_path = image_path
        pass

    def spin_walk_up(self):
        print "WALK UP"

    def spin_walk_down(self):
        print "WALK DOWN"

    def spin_walk_right(self):
        print "WALK RIGHT"

    def spin_walk_left(self):
        print "WALK LEFT"

    def check_for_obstacle(self):

        image_path = [os.path.join(os.path.dirname(__file__) + "/TestImages",'red bucket.png'), os.path.join(os.path.dirname(__file__) + "/TestImages",'vooruit.png')]
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
            #hsv_image.show()
            if len(bucket_blob) >=1:
                print "DRAAI"
                self.check_for_obstacle()
            else:
                print "VOORUIT"
        else:
            #TODO: MoveState vooruit want er is geen emmer gevonden.
            print "VOORUIT"



