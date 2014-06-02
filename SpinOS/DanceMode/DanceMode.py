import threading

__author__ = 'levi'


class DanceMode:
    alive = True
    movementHandler = None
    logger = None

    def __init__(self, movementHandler, logger):
        DanceMode.movementHandler = movementHandler
        DanceMode.logger = logger

        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        pass

    def set_alive(self, value):
        DanceMode.alive = value

    def process_command(self, command, message):
        pass