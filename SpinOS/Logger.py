from ServerClient import ServerClient
from Command import  COMMAND
__author__ = 'Hendrik'


class Logger:
    SENSOR_VALUES = -2
    INPUT_VALUES = -1
    MESSAGE = 0
    WARNING = 1
    ERROR = 2
    #min priority aanvankelijk van deze waarde worden berichten wel of niet getoond
    def __init__(self, min_priority):
        self.min_log_priority = min_priority
        self.server = None
    #server object zetten
    def set_server(self, ser):
        self.server = ser
    #loggen van een event, module is van waar gelogd wordt message is het bericht en priority is wat is de prioriteit dat het getoond wordt
    def logevent(self, module, message, priority=0):
        if priority >= self.min_log_priority:
            print(str(module).upper() + str(" - ") + str(message))
            if self.server is not None:
                for c in self.server.clients:
                    if c.type == ServerClient.ANDROID_DASHBOARD:
                        c.send_message(COMMAND.encode_message(COMMAND.LOG_ENTRY, [str(module).upper() + str(" - ") + str(message)]))

    #log level omzetten in een string
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
