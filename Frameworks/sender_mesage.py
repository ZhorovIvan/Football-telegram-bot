from datetime import datetime
import threading
from time import sleep
import configparser as cp
import logging


class Timer(threading.Thread):


    def __init__(self) -> None:
        threading.Thread.__init__(self)
        self.config = self.read_config()


    def run(self) -> None:
        while True:
            now = datetime.now()
            if self.is_start_time(now):
                print('Its time to run the code')


    def read_config(self) -> cp:
        config = cp.ConfigParser()
        return config.read('config.ini')

    
    def is_start_time(self, time) -> bool:
        return time.hour == self.config["TIMER"]["hours"] and\
        time.minute == self.config["TIMER"]["minutes"]
