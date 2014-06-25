__author__ = 'Robert'

import threading
from SimpleCV import Image
import time

class TeelbalMode:

    alive = True
    movementHandler = None
    spinOS = None

    teerballen_found = 0

    def __init__(self, movement_handler, logger, spin_os):
        TeelbalMode.movementHandler = movement_handler
        TeelbalMode.logger = logger
        TeelbalMode.spinOS = spin_os

        TeelbalMode.logger.logevent("TeelbalMode", "TeelbalMode opstarten...", 0)

        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        next = SearchState()
        next.doe_stap([])

    def set_alive(self, value):
        TeelbalMode.alive = value

    def process_command(self, command, message):
        pass


class TeelbalVision:

    IMAGE_URL = "http://raspberrypi:8080/?action=snapshot"

    BINARIZE_THRESHOLD = 100
    MIN_AREA = 1000
    MAX_AREA = 12000
    RECTANGLE_TOLERANCE = 0.4

    def __init__(self):
        pass

    #Methode die een Image returned van de IMAGE_URL
    @staticmethod
    def get_image():
        return Image(TeelbalVision.IMAGE_URL)

    @staticmethod
    def find_teerbal(img):
        black = img.colorDistance((0,0,0))

        bin = black.binarize(TeelbalVision.BINARIZE_THRESHOLD)

        blackBlobs = bin.findBlobs()

        if blackBlobs is not None and len(blackBlobs) > 0:

            goodBlobs = []

            for blackBlob in blackBlobs:
                if blackBlob.isRectangle(TeelbalVision.RECTANGLE_TOLERANCE) and blackBlob.area() > TeelbalVision.MIN_AREA and blackBlob.area() < TeelbalVision.MAX_AREA:
                    goodBlobs.append(blackBlob)

            #Grootste area en y
            goodBlobs = sorted(goodBlobs, key=lambda x: (x.y, x.area()))

            if not goodBlobs or len(goodBlobs) < 0:
                return False

            goodBlob = goodBlobs[-1]

            return goodBlob

        else:
            return False


class SearchState:

    DEFAULT_TURN = True #true voor links draaien, false voor rechts

    def __init__(self):
        pass

    def doe_stap(self, parameters):
        while TeelbalMode.teerballen_found < 1:
            TeelbalMode.logger.logevent("TeelbalMode SearchState", "Teerbal zoeken...", 0)

            img = TeelbalVision.get_image()
            teerbal = TeelbalVision.find_teerbal(img)

            while not teerbal and TeelbalMode.alive:
                TeelbalMode.logger.logevent("TeelbalMode SearchState", "Teerbal nog niet gevonden, draaien", 0)
                #Draaien en kijken of we nu wel een teerbal vinden
                TeelbalMode.movementHandler.move_one_turn(SearchState.DEFAULT_TURN) #links??
                img = TeelbalVision.get_image()
                teerbal = TeelbalVision.find_teerbal(img)

            if not TeelbalMode.alive:
                return

            next = MoveState()
            next.doe_stap([teerbal])

class MoveState:

    SCREEN_CENTER = 230 #640 / 2
    REACHED_AREA = 8000

    def __init__(self):
        pass

    def doe_stap(self, parameters):
        TeelbalMode.logger.logevent("TeelbalMode MoveState", "Teerbal gevonden, ernaar toe lopen", 0)
        blob = parameters[0]

        move_to_center = self.move_to_center(blob, MoveState.SCREEN_CENTER)
        if not move_to_center:
            TeelbalMode.logger.logevent("TeelbalMode MoveState", "Teerbal kwijt...", 0)
            return False

        TeelbalMode.logger.logevent("TeelbalMode MoveState", "Teelbal in het midden, lopen")

        while blob.area() < MoveState.REACHED_AREA and TeelbalMode.alive:
            for i in xrange(0, 5):
                TeelbalMode.movementHandler.move_one_step()

            img = TeelbalVision.get_image()
            teerbal = TeelbalVision.find_teerbal(img)
            if not teerbal:
                return False

            self.move_to_center(teerbal, MoveState.SCREEN_CENTER)

        if not TeelbalMode.alive:
            return False

        TeelbalMode.logger.logevent("TeelbalMode MoveState", "Bij teerbal, #yolo", 0)
        TeelbalMode.spinOS.play_sound(5)
        TeelbalMode.teerballen_found += 1


    def move_to_center(self, blob, center):
        TeelbalMode.logger.logevent("TeelbalMode MoveState", "Teerbal naar het midden draaien", 0)

        verschil = self.diff_to_center(blob, center)

        while abs(verschil) > 50 and TeelbalMode.alive: #100 px marge voor het midden
            print "Blob nog niet in het midden"
            if verschil > 0:
                #naar links draaien
                TeelbalMode.movementHandler.move_one_turn(True)
            else:
                #naar rechts draaien
                TeelbalMode.movementHandler.move_one_turn(False)

            img = TeelbalVision.get_image()
            teerbal = TeelbalVision.find_teerbal(img)

            if not teerbal:
                return False

            blob = teerbal

            verschil = self.diff_to_center(blob, center)

        if not TeelbalMode.alive:
            return False

        return True

    def diff_to_center(self, blob, center):
        blobCenter = float(blob.bottomLeftCorner()[0]) + float(float(blob.width()) / float(2))
        return int(center) - int(blobCenter)

img = Image("C:\Users\Robert\Desktop\\192.168.10.jpg")
teerbal = TeelbalVision.find_teerbal(img)
teerbal.show()
time.sleep(5)