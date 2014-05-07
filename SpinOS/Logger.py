__author__ = 'Hendrik'


class Logger:
    SENSOR_VALUES = -2
    INPUT_VALUES = -1
    MESSAGE = 0
    WARNING = 1
    ERROR = 2

    def __init__(self, min_priority):
        self.min_log_priority = min_priority

    def logevent(self, module, message, priority=0):
        if priority >= self.min_log_priority:
            print(str(module) + str(" - ") + str(message))

    def get_loglevel_string(self):
        if self.min_log_priority == Logger.SENSOR_VALUES:
            return "SENSOR_VALUES"
        elif self.min_log_priority == Logger.MESSAGE:
            return "MESSAGE"
        elif self.min_log_priority == Logger.WARNING:
            return "WARNING"
        elif self.min_log_priority == Logger.ERROR:
            return "ERROR"
        elif self.min_log_priority == Logger.INPUT_VALUES:
            return "INPUT_VALUES"
        else:
            return "UNDEFINED"
