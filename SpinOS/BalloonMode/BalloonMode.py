__author__ = 'Robert'

import threading

class BalloonMode:

    alive = True
    logger = None

    def __init__(self, logger):
        self.set_alive(True)
        BalloonMode.logger = logger
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        from CardState import CardState
        state = CardState()
        state.doe_stap([])

    def set_alive(self, value):
        BalloonMode.alive = value

    def process_command(self, command, message):
        pass