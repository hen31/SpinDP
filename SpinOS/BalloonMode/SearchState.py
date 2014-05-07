__author__ = 'Robert'

from BalloonMode import BalloonMode
import SimpleCV

class SearchState:

    def __init__(self):
        self.colors = []
        self.current_color = 0

    def doe_stap(self, parameters):
        if BalloonMode.alive:
            self.colors = parameters[0]
            print "Ik ga een ballon zoeken. Dit is de volgorde van kleuren:"
            print self.colors;

    def find_balloon(self):
        cam = SimpleCV.Camera()
        return