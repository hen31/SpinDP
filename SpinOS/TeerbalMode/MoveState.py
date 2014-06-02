from TeerbalMode import TeerbalMode
from SimpleCV import *
from TeerbalVision import TeerbalVision
from FoundState import FoundState
from Coordinate import Coordinate


__author__ = 'Jeroen'

class MoveState:


    def __init__(self):
        self.x = 0
        self.y = 0
        self.found = False
        #vatiabele die het aantal stappen die de spin heeft gemaakt in een bepaalde rij bij houdt
        self.aantal_stappen = 0
        #variabele met de afgelegde route
        self.route_list = []
        #variabele met de posities van de gevonden teerballen
        self.pos_list = []
        #riching waar de spin naar kijkt
        self.facing = Coordinate.NORTH


    def doe_stap(self, found, foto_array):
        index = 0
        gevonden = False

        #als er een teerbal is gesignaleerd
        if found:
            while TeerbalMode.alive and not gevonden:
                #variabelene die bij houden of de teerbal gevonden is en of het een mogelijke duplicaat is
                (gevonden, duplicaat) = TeerbalVision.find_teerbal(foto_array[index], True)
                index+=1
                #als de teerbal is gevonden en evt. een duplicaat is
                if gevonden and duplicaat:
                    #kijken of de teerbal al eerder is gevonden
                    dupe = self.check_duplicate(gevonden, duplicaat)
                    #als de teerbal een duplicaat is moet de spin teruglopen zonder een geluid te maken en vervolgens zijn
                    #zoektocht voortzetten
                    if dupe:
                        self.turn_right()
                        self.turn_right()
                        self.walk_forward(False)
                        self.walk_back()
                        return False
                    #als de gevonden teerbal geen duplicaat is deze verwerken
                    else:

                        FoundState.play_sound()
                        self.move_row(gevonden)
                        return True
                #als de gevonden teerbal geen duplicaat is deze verwerken
                else:
                    if gevonden:

                        FoundState.play_sound()
                    self.move_row(gevonden)
            if not TeerbalMode.alive:
                return
            return True
        else:
            self.move_column(gevonden)

    #methode die kijkt of de gevonden teerbal een duplicaat is door te kijken of de al gevonden teerballen een buurman-loctie
    #hebben
    def check_duplicate(self, found,  buren_gevonden):
        if buren_gevonden:
            locatie = Coordinate(self.x,self.y,buren_gevonden, self.facing)
            if self.pos_list is not None:
                for elements in self.pos_list:
                    if locatie.x-1 == elements.x and locatie.y == elements.y:
                        return True
        return False

    #methode die de spin vooruit laat lopen en de coordinaten van de spin aanpassen
    def walk_forward(self,found):
        self.route_list.append(Coordinate(self.x,self.y,found, self.facing))

        if self.facing == Coordinate.NORTH:
            self.y +=1
        if self.facing == Coordinate.EAST:
            self.x +=1
        if self.facing == Coordinate.SOUTH:
            self.y -=1
        if self.facing == Coordinate.WEST:
            self.x -=1

    #methode die de spin naar links laat draaien
    def turn_left(self):
        if self.facing == Coordinate.NORTH:
            self.facing = Coordinate.WEST
        elif self.facing == Coordinate.WEST:
            self.facing = Coordinate.SOUTH
        elif self.facing == Coordinate.SOUTH:
            self.facing = Coordinate.EAST
        elif self.facing == Coordinate.EAST:
            self.facing = Coordinate.NORTH

    #methode die spin naar rechts laat draaien
    def turn_right(self):
        if self.facing == Coordinate.NORTH:
            self.facing = Coordinate.EAST
        elif self.facing == Coordinate.EAST:
            self.facing = Coordinate.SOUTH
        elif self.facing == Coordinate.SOUTH:
            self.facing = Coordinate.WEST
        elif self.facing == Coordinate.WEST:
            self.facing = Coordinate.NORTH

    #methode die de spin een kolom laat opschuiven
    def move_column(self, found):
        self.turn_right()
        self.walk_forward(found)
        self.turn_left()

    #methode die de spin laat teruglopen naar de begin rij
    def walk_back(self):
        for i in xrange(0,self.aantal_stappen-1):
            self.walk_forward(False)

        self.turn_left()
        self.walk_forward(False)
        self.turn_left()
        self.aantal_stappen = 0

    #methode die de spin een rij laat opschuiven
    def move_row(self, found):
        #als de teerbal is gevonden moet de spin weer terug lopen naar de start positie om een kolom verder te zoeken
        if found:
            self.pos_list.append(Coordinate(self.x,self.y,found,self.facing))
            self.turn_right()
            self.turn_right()

            #eerst een stap vooruit doen om de locatie van de teerbal in te vullen op de routekaart!
            self.walk_forward(found)
            self.walk_back()
        #als er geen teerbal is gevonden doorlopen en verder zoeken
        else:
            self.walk_forward(found)
            self.aantal_stappen +=1









