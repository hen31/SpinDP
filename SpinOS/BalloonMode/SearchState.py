__author__ = 'Robert'

from BalloonMode import BalloonMode

class SearchState:

    def __init__(self):
        self.colors = []
        self.currentColor = 0

    def doe_stap(self, parameters):
        if BalloonMode.alive:
            self.colors = parameters[0]

    def find_balloon(self):
        #vind de ballon
        return