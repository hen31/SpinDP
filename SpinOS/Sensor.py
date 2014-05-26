import threading
import time
from Logger import Logger

__author__ = 'Ruben'

class Sensor(threading.Thread):
    alive = True

    def __init__(self, logger):
        self.logger = logger
        self.thread = threading.Thread(target=self.run)

    def run(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass