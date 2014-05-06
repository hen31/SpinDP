from SimpleCV import *

__author__ = 'Jeroen'


image1 = Image("testTeerbal.png")
image1.show()
time.sleep(2)
image2 = image1.colorDistance(color=Color.BLACK).binarize()
image2 = image2.erode(2)
image2 = image2.invert()
image2.show()
time.sleep(2)













class SearchState:

    def __init__(self):
        image1.show()
        time.sleep(2)
        image2 = image1.colorDistance(color=Color.BLACK).binarize()
        image2 = image2.erode(2)
        image2 = image2.invert()
        image2.show()
        time.sleep(2)


