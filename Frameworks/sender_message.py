from datetime import datetime
import threading
from time import sleep
from Frameworks.football_telebot import TelegramBot
import configparser as cp
import logging


class Timer(threading.Thread):

    def __init__(self) -> None:
        threading.Thread.__init__(self)
        self.bot = TelegramBot()
        self.config = cp.ConfigParser()
        self.config.read('config.ini')


    def run(self) -> None:
        while True:
            now = datetime.now()
            if False:
                self.bot.send_messge('1')
                sleep(1)
                print('Its time to run the code')

                
    def is_start_time(self, time) -> bool:
        return time.hour == 2 and time.minute == 30
