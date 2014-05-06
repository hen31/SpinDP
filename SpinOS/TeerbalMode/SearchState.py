from SimpleCV import *

__author__ = 'Jeroen'

class SearchState:

    def __init__(self, image):
        self.image = image

    def search_teerbal(self):
        self.image = Image("teerbal raar.png")
        self.image.show()
        time.sleep(0.5)
        bin_image = self.image.colorDistance(color=Color.BLACK).binarize()
        bin_image.erode(2)
        bin_image.show()
        time.sleep(2)

        blobs = bin_image.findBlobs()
        print blobs
        for b in blobs:
            index = index +1
        print index

        blobs = blobs.filter(blobs.area() > 100)
        print blobs


        lager = blobs.below(1)
        print lager
        index = 0
        for l in lager:
            lager[index].show()
        index = index+1

        print index

        #blobs.draw()



