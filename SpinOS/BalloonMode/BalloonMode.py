__author__ = 'Robert'

from CardState import CardState
from FoundState import FoundState
from MoveState import MoveState
from SearchState import SearchState

import threading

class BalloonMode:

    alive = True

    def __init__(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        state = CardState()
        state.doe_stap()