__author__ = 'Robert'

from BalloonMode import BalloonMode
from BalloonVision import BalloonVision
from FoundState import FoundState
from SimpleCV import *

class MoveState:

    def __init__(self):
        pass

    def doe_stap(self, parameters):
        #parameters 0 = color, 1 = blob
        if BalloonMode.alive:
            move = self.move_to_balloon(parameters[0], parameters[1])

            if move is not False:
                foundState = FoundState()
                foundState.doe_stap([parameters[0]])
        return

    def move_to_balloon(self, color, blob):
        #Draaien zodat de ballon in het midden van de camera staat
        #Midden van het beeld
        center = 640 / 2

        verschil = center - blob.x
        while abs(verschil) > 20 and BalloonMode.alive: #20 px marge voor het midden
            print "Blob nog niet in het midden"
            if verschil > 0:
                #TODO: 5 graden naar links draaien
                pass
            else:
                #TODO: 5 graden naar rechts draaien
                pass

            img = BalloonVision.get_image()
            search = BalloonVision.find_balloon(color, img)

            blob = search[1]

            if search[0]:
                verschil = center - blob.x

        if not BalloonMode.alive:
            return False

        #loop naar de ballon
        #lopen moet nog worden gemaakt
        print "Ik ga nu lopen. Maar dat kan ik nog niet :-("

        area = 0
        while area < 2000 and BalloonMode.alive: #2000???
            last_area = area
            #TODO: vooruit lopen
            img = BalloonVision.get_image()
            search = BalloonVision.find_balloon(color, img)
            if search[0]:
                area = search[1].area()
        if not BalloonMode.alive:
            return False

        return True