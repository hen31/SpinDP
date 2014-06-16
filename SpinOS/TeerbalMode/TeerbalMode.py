import threading


__author__ = 'Jeroen'


class TeerbalMode:

    alive = True
    logger = None


    def __init__(self, logger):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        TeerbalMode.logger = logger

    def run(self):
        from SearchState import SearchState
        state = SearchState()
        state.doe_stap()


    def set_alive(self, bool):
        TeerbalMode.alive = bool


