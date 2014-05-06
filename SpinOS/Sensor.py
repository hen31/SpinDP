import threading
import time
from SensorLogger import SensorLogger
from Logger import Logger

__author__ = 'Ruben'

class Sensor(threading.Thread):
    alive = True

    def __init__(self, logger):
        self.logger = logger
        self.sensorlogger = SensorLogger('MPU6050',logger)

    def run(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def getValue(self):
        pass