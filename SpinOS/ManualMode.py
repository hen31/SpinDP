import threading
import Command

__author__ = 'Hendrik'


class ManualMode:
    alive = False

    def __init__(self, movementHandler):
        self.mutex = threading.Semaphore(1)
        self.handler = movementHandler

    def process_command(self, command, parameters):
        self.mutex.acquire()
        if command == Command.MOVE:
            angleMove  = parameters[0]
            forceMove  = parameters[1]
            angleTurn  = parameters[2]
            forceTurn  = parameters[3]
            self.handler.move()
        elif command == Command.MOVE_INTERNAL:
            angle  = parameters[0]
            force  = parameters[1]
            pass
        elif command == Command.MOVE_HEIGHT:
            height = parameters[0]
            pass
        self.mutex.release()