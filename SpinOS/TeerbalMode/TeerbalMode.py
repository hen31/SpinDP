import SearchState
import MoveState
import FoundState
__author__ = 'Jeroen'

class TeerbalMode:

    alive = False

    def __init__(self):
        print "Hoi Hendrik!"
        self.aantal_gevonden = 0
        print self.aantal_gevonden;

        while self.aantal_gevonden < 3:

            if SearchState.SearchState().search_teerbal() == True:
                self.aantal_gevonden+=1
                print self.aantal_gevonden
                FoundState.FoundState().play_sound()
                if self.aantal_gevonden != 3:
                    MoveState.MoveState().check_for_obstacle()
            else:
                MoveState.MoveState().check_for_obstacle()


