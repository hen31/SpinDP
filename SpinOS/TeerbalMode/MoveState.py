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
        self.aantal_stappen = 0
        self.route_list = []
        self.pos_list = []
        self.facing = Coordinate.NORTH


    def doe_stap(self, found, foto_array):
        index = 0
        gevonden = False
        if found:
            while TeerbalMode.alive and not gevonden:
                (gevonden, buren) = TeerbalVision.find_teerbal(foto_array[index], True)

                index+=1
                if gevonden:
                    self.check_duplicate(gevonden)
                self.move_row(gevonden)
            if not TeerbalMode.alive:
                return
            FoundState.play_sound()
        else:
            self.move_column(gevonden)

    def check_duplicate(self, gevonden):
        if gevonden:
            locatie = Coordinate(self.x,self.y,gevonden, self.facing)
            if self.pos_list is not None:
                for elements in self.pos_list:
                    if locatie.x-1 == elements.x and locatie.y == elements.y:
                        print "possible DUPE found x:{}y:{} dupe? x:{}y:{}".format(locatie.x,locatie.y,elements.x,elements.y)
                    else:
                        print "NO DUPE found x:{}y:{} dupe? x:{}y:{}".format(locatie.x,locatie.y,elements.x,elements.y)


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

    def turn_left(self):
        if self.facing == Coordinate.NORTH:
            self.facing = Coordinate.WEST
        elif self.facing == Coordinate.WEST:
            self.facing = Coordinate.SOUTH
        elif self.facing == Coordinate.SOUTH:
            self.facing = Coordinate.EAST
        elif self.facing == Coordinate.EAST:
            self.facing = Coordinate.NORTH

    def turn_right(self):
        if self.facing == Coordinate.NORTH:
            self.facing = Coordinate.EAST
        elif self.facing == Coordinate.EAST:
            self.facing = Coordinate.SOUTH
        elif self.facing == Coordinate.SOUTH:
            self.facing = Coordinate.WEST
        elif self.facing == Coordinate.WEST:
            self.facing = Coordinate.NORTH

    def check_start_row(self):
        self.turn_right()


    def move_column(self, found):
        # self.pos_list.append(Coordinate(self.x,self.y,found,self.facing))
        # print Coordinate(self.x,self.y,found, self.facing).toString()
        self.turn_right()
        self.walk_forward(found)
        self.turn_left()

    def walk_back(self):
        for i in xrange(0,self.aantal_stappen-1):
            self.walk_forward(False)

        self.turn_left()
        self.walk_forward(False)
        self.turn_left()
        self.aantal_stappen = 0

    def move_row(self, found):
        if found:
            #als de teerbal is gevonden moet de spin weer terug lopen naar de start positie om een kolom verder te zoeken
            self.pos_list.append(Coordinate(self.x,self.y,found,self.facing))
            self.turn_right()
            self.turn_right()
            #print self.aantal_stappen
            self.walk_forward(found)
            self.walk_back()
        else:
            self.walk_forward(found)
            self.aantal_stappen +=1









