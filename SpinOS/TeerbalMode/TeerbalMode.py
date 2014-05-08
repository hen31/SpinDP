from os import getcwd
import SearchState
import MoveState
import FoundState
import os, sys
__author__ = 'Jeroen'

class TeerbalMode:

    alive = False

    def __init__(self):
        #print "Hoi Hendrik!"
        self.aantal_gevonden = 0
        self.image_path = getcwd()
        self.route = []

        print self.image_path
        print self.aantal_gevonden

        while self.aantal_gevonden < 3:

            if SearchState.SearchState(self.image_path).search_teerbal() == True:
                self.aantal_gevonden+=1
                print self.aantal_gevonden
                FoundState.FoundState(self.image_path).play_sound()
                if self.aantal_gevonden != 3:
                    MoveState.MoveState(self.image_path).check_for_obstacle()
            else:
                MoveState.MoveState(self.image_path).check_for_obstacle()


