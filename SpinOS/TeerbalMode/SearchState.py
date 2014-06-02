from TeerbalMode import TeerbalMode
from TeerbalVision import TeerbalVision


__author__ = 'Jeroen'


class SearchState:

    AANTAL_ZOEKEN = 3

    def __init__(self):
        self.index = 0

    def doe_stap(self):
        aantal_gevonden = 0
        from MoveState import MoveState
        nextState = MoveState()
        #zoeken todat je X aantal teerballen hebt gevonden
        while aantal_gevonden != SearchState.AANTAL_ZOEKEN:
            if TeerbalMode.alive == True:
                array = TeerbalVision.foto_array()
                print "AANTALGEVONDE:{}".format(aantal_gevonden)
                print "KOLOM:{}".format(self.index)
                #variabele die representeerd of er een teerbal is gevonden in het gezichtsveld van de spin
                found_row = self.checkRij(array[self.index])
                #als er een teerbal is gevonden moet de spin er heen lopen, dit wordt gedaan in de MoveState
                if found_row == True:
                    #variable die representeed of de spin bij de gevonden teerbal staat
                    found_teerbal = nextState.doe_stap(found_row, array[self.index])
                    if found_teerbal:
                        aantal_gevonden +=1
                #als er geen teerbal is gevonden moet de spin opzij bewegen
                else:
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
