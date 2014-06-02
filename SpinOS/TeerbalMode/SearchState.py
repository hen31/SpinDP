from TeerbalMode import TeerbalMode
from TeerbalVision import TeerbalVision


__author__ = 'Jeroen'


class SearchState:

    #aantal teerballen dat moet worden gezocht
    AANTAL_ZOEKEN = 3

    def __init__(self):
        self.index = 0

    def doe_stap(self):
        #aantal teerballen dat is gevonden
        aantal_gevonden = 0
        from MoveState import MoveState
        nextState = MoveState()
        #zoeken todat je X aantal teerballen hebt gevonden
        while aantal_gevonden != SearchState.AANTAL_ZOEKEN:
            if TeerbalMode.alive == True:
                #een array met foto's puur bedoelt voor testen
                array = TeerbalVision.foto_array()
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

    #kijken of er in de rij een teerbal ligt dat, straks is dit 1 foto nu nog een array
    def checkRij(self,imgpath):
        index = 0
        while index < len(imgpath):
            #kijken of er een teerbal ligt
            if TeerbalVision.find_teerbal(imgpath[index], False):
                return True
            index+=1
        return False
