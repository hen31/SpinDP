import threading
from Command import COMMAND
from Logger import Logger

__author__ = 'Hendrik'


class ManualMode:
    alive = False

    def __init__(self, movementHandler, logger):
        self.mutex = threading.Semaphore(1)
        self.handler = movementHandler
        self.logger = logger

    def set_alive(self, bool):
        pass

    def process_command(self, command, parameters):
        self.mutex.acquire()
        if command == COMMAND.MOVE:
            angleMove  = parameters[0]
            forceMove  = parameters[1]
            angleTurn  = parameters[2]
            forceTurn  = parameters[3]
            self.logger.logevent("MANUAL MODE", "Move [" + str(angleMove)+"," + str(forceMove)+"," + str(angleTurn) + "," + str(forceTurn) + "]", Logger.INPUT_VALUES)
            self.handler.move(angleMove, forceMove, angleTurn, forceTurn)
        elif command == COMMAND.MOVE_INTERNAL:
            angle = parameters[0]
            force = parameters[1]
            self.logger.logevent("MANUAL MODE", "Move Internal [" + str(angle)+"," + str(force) + "]", Logger.INPUT_VALUES)
            self.handler.move_internal(angle, force)
        elif command == COMMAND.MOVE_HEIGHT:
            height = parameters[0]
            self.logger.logevent("MANUAL MODE", "Move height [" + str(height) + "]", Logger.INPUT_VALUES)
            self.handler.move_height(height)
        self.mutex.release()