__author__ = 'Hendrik'


class Logger:
    MESSAGE = 0
    WARNING = 1
    ERROR = 2

    def __init__(self, min_priority):
        self.min_log_priority = min_priority

    def logevent(self, module, message, priority=0):
        if priority >= self.min_log_priority:
            print(str(module)+ str(" - ") + str(message))