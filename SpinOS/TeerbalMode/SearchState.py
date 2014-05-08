from SimpleCV import *
import FoundState
import MoveState
__author__ = 'Jeroen'

class SearchState:

    def __init__(self):
        pass

    def search_teerbal(self):
        image_path = ["C:\\Users\\Jeroen\\Documents\\GitHub\\SpinDP\\SpinOS\\TeerbalMode\\TestImages\\teerbal.jpg", "C:\\Users\\Jeroen\\Documents\\GitHub\\SpinDP\\SpinOS\\TeerbalMode\\TestImages\\vooruit.png"]
        rand = random.randrange(0,2)
        self.image = Image("C:\\Users\\Jeroen\\Documents\\GitHub\\SpinDP\\SpinOS\\TeerbalMode\\TestImages\\teerbal.jpg")

        if rand == 0:
            print "FOTO: TEERBAL"
        else:
            print "FOTO: GEEN TEERBAL"

        (r,g,b) = self.image.splitChannels()
        r.show()
        time.sleep(5)
        g.show()
        time.sleep(5)
        b.show()
        time.sleep(5)
        bin_image = self.image.hueDistance(color=Color.BLACK)#binarize(20)
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
            blobs[-1].draw()
            bin_image.show()

            if len(blobs) >= 1:
                return True
            else:
                return False
        return False