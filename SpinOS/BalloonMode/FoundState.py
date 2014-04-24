__author__ = 'Robert'

class FoundState:

    def __init__(self):
        pass

    def doe_stap(self, parameters):
        if BalloonMode.alive == True:
            SearchState.getinstance().doestap()
        return
