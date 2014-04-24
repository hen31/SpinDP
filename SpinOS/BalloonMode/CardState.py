__author__ = 'Robert'

from BalloonMode import BalloonMode
from SearchState import SearchState

class CardState:

    def __init__(self):
        pass

    def doe_stap(self, parameters):
        if BalloonMode.alive:
            recognize = self.recognize_card()
            if recognize == False:
                nextState = SearchState()
                nextState.doe_stap([recognize])

    def recognize_card(self):
        print "Ik ga nu een kaart herkennen. Joepie! :)"
        return ["kleur1", "kleur2", "kleur3"]