import threading
import Command

__author__ = 'Hendrik'


class ManualMode:
    alive = False

    def __init__(self):
        self.mutex = threading.Semaphore(1)

    def process_command(self, command, parameters):
        self.mutex.acquire()
        if command == Command.MOVE:
            angle  = parameters[0]
            force  = parameters[1]
        elif command == Command.MOVE_INTERNAL:
            angle  = parameters[0]
            force  = parameters[1]
            pass
        elif command == Command.MOVE_HEIGHT:
            height = parameters[0]
            pass
        self.mutex.release()