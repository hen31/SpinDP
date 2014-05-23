import threading
from time import strftime

from Logger import Logger


__author__ = 'Hendrik'


class SensorLogger:
    def __init__(self, sensor_name, logger):
        self.log_file = open(sensor_name + ".txt", "w")
        self.sensor_name = sensor_name
        self.logger = logger
        self.mutex = threading.Semaphore(1)

    def log_waarde(self, waarde):
        self.mutex.acquire()
        self.log_file.write(str(waarde) + "<;>")
        self.mutex.release()
        self.logger.logevent(self.sensor_name,   "waarde : " + str(waarde), self.logger.SENSOR_VALUES)

    def get_log(self):
        self.mutex.acquire()
        self.log_file = open(self.sensor_name + ".txt", "r")
        data = self.log_file.readlines()
        self.log_file = open(self.sensor_name + ".txt", "a")
        self.mutex.release()
        return data

