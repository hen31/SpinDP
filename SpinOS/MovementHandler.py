import threading

__author__ = 'Ruben'

class MovementHandler:

    def __init__(self):
        self.mutexMove = threading.Semaphore(1)
        self.mutexHeight = threading.Semaphore(1)
        self.mutexIntenal = threading.Semaphore(1)

    def move(self, degreesMove, powerMove, degreesTurn, powerTurn):
        self.mutexMove.acquire()

        self.mutexMove.release()

    def move_height(self, height):
        self.mutexHeight.acquire()

        self.mutexHeight.release()

    def move_internal(self, degrees, power):
        self.mutexIntenal.acquire()

        self.mutexIntenal.release()

    def die(self):
        self.mutexIntenal.acquire()
        self.mutexHeight.acquire()
        self.mutexIntenal.acquire()
        pass