import threading
from PotenHoog import PotenHoog
from Aftikken import Aftikken
from Einde import Einde
from PushUps import PushUps
from Rondje import Rondje
from Wippen import Wippen
from ZijwaartseWipLoop import ZijwaartseWipLoop
from Zwaaien import Zwaaien
from Logger import Logger

__author__ = 'levi'


class DanceMode:
    alive = True
    movementHandler = None
    logger = None

    def __init__(self, movementHandler, logger):
        DanceMode.movementHandler = movementHandler
        DanceMode.logger = logger

        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        DanceMode.logger.logevent("DanceMode", "Beginnen met dansen", Logger.MESSAGE)
        danceOrder = [Aftikken(), PushUps(), Zwaaien(), PotenHoog(), Wippen(), Rondje(), ZijwaartseWipLoop(), Einde()]
        for dance in danceOrder:
            if DanceMode.alive:
                DanceMode.logger.logevent("DanceMode", dance.__class__ + " dansen", Logger.MESSAGE)
                dance.run()

    def set_alive(self, value):
        DanceMode.alive = value

    def process_command(self, command, message):
        pass