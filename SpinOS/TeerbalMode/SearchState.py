from SimpleCV import *
from TeerbalMode import TeerbalMode
from TeerbalVision import TeerbalVision
import os

__author__ = 'Jeroen'


class SearchState:

    LEFT_X = 170
    LEFT_Y = 0
    RIGHT_X = 470
    RIGHT_Y= 480

    def __init__(self):
        self.index = 0

    def doe_stap(self):
        aantal_gevonden = 0
        from MoveState import MoveState
        nextState = MoveState()
        while aantal_gevonden != 3:
            if TeerbalMode.alive == True:
                array = TeerbalVision.foto_array()
                found_row = self.checkRij(array[self.index])
                if found_row == True:
                    aantal_gevonden +=1
                    nextState.doe_stap(found_row, array[self.index])
                else:
                    nextState.doe_stap(found_row, array[self.index])
                self.index +=1
        for e in nextState.pos_list:
            print e.toString()

    def checkRij(self,imgpath):
        index = 0
        while index != len(imgpath):
            if TeerbalVision.find_teerbal(imgpath[index]):
                return True
            index+=1
        return False
