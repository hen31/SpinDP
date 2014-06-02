__author__ = 'Jeroen'

class Coordinate:

    #richtingen waar de spin naartoe kan kjken
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def __init__(self, x, y, teerbal_found, direction):
        self.x = x
        self.y = y
        self.found = teerbal_found
        self.direction = direction

    def toString(self):
        return "x:{} y:{} found:{} direction:{}".format(self.x,self.y,self.found,self.direction)