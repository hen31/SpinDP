from TeerbalMode import SearchState

__author__ = 'Jeroen'

class TeerbalMode:

    alive = False;

    def __init__(self):
        self.currentState = SearchState;


    def process_command(self, command, parameters):
        print "teerbal process_command"

