__author__ = 'Hendrik'


class COMMAND:
    IDENTIFY = -2
    RECIEVED = -1
    TO_MANUAL = 0
    TO_BALLOON_MODE = 1
    TO_TEERBAL_MODE = 2
    TO_DANCE_MODE = 3
    SEND_SENSOR_DATA = 4
    SEND_START_TIME = 5
    KILL = 6
    MOVE = 7
    MOVE_INTERNAL = 8
    MOVE_HEIGHT = 9


    def __init__(self):
        pass
    @staticmethod
    def decode_message(recieved_string):
        recieved_string.replace("\n", "")
        splitter = '<;>'
        result = recieved_string.split(splitter)
        result[0] = int(result[0])
        return result
    @staticmethod
    def encode_message(command, parameters):
        if len(parameters) > 0:
            encoded_string = str(command) + "<;>"
            for x in xrange(0, len(parameters)):
                if x > len(parameters)-1:
                    encoded_string += str(parameters[x]) + "<;>"
                else:
                    encoded_string += str(parameters[x])
        else:
            encoded_string = str(command)

        return encoded_string
