from datetime import datetime
import threading
from Frameworks.football_telebot import TelegramBot
from Frameworks.mysql_storage import MySQLStorage


class Timer(threading.Thread):

    HOUR_FOR_START = 2
    MINUTE_FOR_START = 30


    def __init__(self, config) -> None:
        threading.Thread.__init__(self)
        self.bot = TelegramBot(config)
        self.mysql = MySQLStorage(config)
        self.config = config


    def run(self) -> None:
        while True:
            now = datetime.now()
            if self.is_start_time(now):
                self.fill_database()


    def fill_database(self) -> None:
        leagues = 
        pass


    def is_start_time(self, time) -> bool:
        '''
        Timer for start filling db out
        '''
        return time.hour == self.HOUR_FOR_START and time.minute == self.MINUTE_FOR_START