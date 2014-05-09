import os.path
import threading
import SearchState
import MoveState
import FoundState

__author__ = 'Jeroen'


class TeerbalMode:

    alive = True

    def __init__(self):
        self.aantal_gevonden = 0
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        self.route = [[]]
        self.trollHendrik()
       #self.current_pos = self.route[0][0]




    def run(self):
        print self.aantal_gevonden

        while self.aantal_gevonden < 3 and TeerbalMode.alive == True:

            if SearchState.SearchState().search_teerbal() == True:
                self.aantal_gevonden+=1
                print self.aantal_gevonden
                FoundState.FoundState().play_sound()
                if self.aantal_gevonden != 3:
                    MoveState.MoveState().check_for_obstacle()
            else:
                MoveState.MoveState().check_for_obstacle()

    def registerRoute(self, direction):
        pass


    def set_alive(self, bool):
        TeerbalMode.alive = bool

    def trollHendrik(self):
        print "ERROR"
        print "Traceback (most recent call last):"
        print " File ""C:/Users/Jeroen/Documents/GitHub/SpinDP/SpinOS/main.py"", line 5, in <module>"
        print "     SpinOs = SpinOS()"
        print " File " "C:\Users\Jeroen\Documents\GitHub\SpinDP\SpinOS\SpinOS.py" ", line 42, in __init__"
        print "     self.current_mode = TeerbalMode()"
        print " File ""C:\Users\Jeroen\Documents\GitHub\SpinDP\SpinOS\TeerbalMode\TeerbalMode.py" ", line 19, in __init__"
        print "     self.current_pos = self.route[0][0]"
        print "IndexError: list index out of range"