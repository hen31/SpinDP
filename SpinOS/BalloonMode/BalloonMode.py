__author__ = 'Robert'

import threading

class BalloonMode:

    alive = True
    logger = None

    def __init__(self, logger):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        self.logger = logger

    def run(self):
        from CardState import CardState
        state = CardState()
        state.doe_stap([])