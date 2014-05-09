import os.path
from os import getcwd
import SearchState
import MoveState
import FoundState

__author__ = 'Jeroen'


class TeerbalMode:

    alive = False

    def __init__(self):
        #print "Hoi Hendrik!"
        self.aantal_gevonden = 0
        #self.image_path = getcwd()

        self.route = []


        #self.image_path = os.path.dirname(os.path.abspath(__file__))

        #print self.image_path
        print self.aantal_gevonden

        while self.aantal_gevonden < 3:

            if SearchState.SearchState().search_teerbal() == True:
                self.aantal_gevonden+=1
                print self.aantal_gevonden
                FoundState.FoundState().play_sound()
                if self.aantal_gevonden != 3:
                    MoveState.MoveState().check_for_obstacle()
            else:
                MoveState.MoveState().check_for_obstacle()


    def set_alive(self, bool):
        pass