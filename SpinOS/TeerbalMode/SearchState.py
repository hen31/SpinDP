from SimpleCV import *
import FoundState
import MoveState
import os, sys
__author__ = 'Jeroen'


image = Image(os.path.join(os.path.dirname(__file__) + "/TestImages",'4cm.jpg'))
image.show()
time.sleep(1)
(h,s,v) = image.splitChannels()
h.show()
time.sleep(2)
s.show()
time.sleep(2)
h = h.binarize(95)
h.show()
time.sleep(2)
blobs = h.findBlobs(1,2000)
blobs[-1].show()
print blobs
time.sleep(2)



class SearchState:

    def __init__(self):
        #self.image_path = image_path
        pass

    def search_teerbal(self):

        image_paths = [os.path.join(os.path.dirname(__file__) + "/TestImages",'teerbal.png'), os.path.join(os.path.dirname(__file__) + "/TestImages",'vooruit.png')]
        rand = random.randrange(0,2)

        self.image = Image(image_paths[rand])



        if rand == 0:
            print "FOTO: TEERBAL"
        else:
            print "FOTO: GEEN TEERBAL"

        (h,s,v)= self.image.splitChannels()
        bin_image = h.binarize(30)
        blobs = bin_image.findBlobs(1,2000)

        if blobs:
            return True
        else:
            return False