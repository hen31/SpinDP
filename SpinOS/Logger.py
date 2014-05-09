from ServerClient import ServerClient
from Command import  COMMAND
__author__ = 'Hendrik'


class Logger:
    SENSOR_VALUES = -2
    INPUT_VALUES = -1
    MESSAGE = 0
    WARNING = 1
    ERROR = 2

    def __init__(self, min_priority):
        self.min_log_priority = min_priority
        self.server = None

    def set_server(self, ser):
        self.server = ser

    def logevent(self, module, message, priority=0):
        if priority >= self.min_log_priority:
            print(str(module).upper() + str(" - ") + str(message))
            if self.server is not None:
                for c in self.server.clients:
                    if c.type == ServerClient.ANDROID_DASHBOARD:
                        c.send_message(COMMAND.encode_message(COMMAND.LOG_ENTRY, [str(module).upper() + str(" - ") + str(message)]))

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
