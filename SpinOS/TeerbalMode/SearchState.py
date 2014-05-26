from SimpleCV import *
from TeerbalMode import TeerbalMode
from TeerbalVision import TeerbalVision
import os

__author__ = 'Jeroen'


class SearchState:

    def __init__(self):
        self.index = 0

    def doe_stap(self):
        aantal_gevonden = 0
        from MoveState import MoveState
        nextState = MoveState()
        while aantal_gevonden != 3:
            if TeerbalMode.alive == True:
                array = TeerbalVision.foto_array()
                print "AANTALGEVONDE:{}".format(aantal_gevonden)
                print "KOLOM:{}".format(self.index)
                found_row = self.checkRij(array[self.index])
                if found_row == True:
                    #print self.checkRij(array[self.index])
                    aantal_gevonden +=1
                    nextState.doe_stap(found_row, array[self.index])
                else:
                    print found_row
                    nextState.doe_stap(found_row, array[self.index])
                self.index +=1
        for e in nextState.pos_list:
            print e.toString()

    def checkRij(self,imgpath):
        index = 0
        while index < len(imgpath):
            if TeerbalVision.find_teerbal(imgpath[index], False):
                return True
            index+=1
        return False
