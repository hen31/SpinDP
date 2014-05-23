import threading

__author__ = 'Jeroen'


class TeerbalMode:

    alive = True

    def __init__(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()


    def run(self):
        from SearchState import SearchState
        state = SearchState()
        state.doe_stap()

    def set_alive(self, bool):
        TeerbalMode.alive = bool


