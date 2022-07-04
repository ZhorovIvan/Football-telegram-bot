from datetime import datetime
import threading


class Timer(threading.Thread):

    HOUR_FOR_START = 2
    MINUTE_FOR_START = 30


    def __init__(self, config, mysql, bet_api, logger) -> None:
        threading.Thread.__init__(self)
        self.mysql = mysql
        self.config = config
        self.bet_api = bet_api
        self.logger = logger


    def run(self) -> None:
        while True:
            try:
                now = datetime.now()
                if self.__is_start_time(now):
                    self.fill_database()
                    self.logger.info('Data was added successfully')
            except Exception as e:
                self.logger.error(e)


    def fill_database(self) -> None:
        leagues_from_db = self.mysql.get_allrows_from_league(is_string_type=False)
        leagues_from_onex_db = self.bet_api.get_leagues()

        new_leagues = str()
        for league in leagues_from_db:
            if not self.__has_new_league(league, leagues_from_onex_db):
                new_leagues += '({lg}),'.format(lg=league) 
        if not new_leagues:
            self.mysql.multi_insert_to_onexdata(new_leagues)


    def __has_new_league(self, league : str, league_list : list) -> bool:
        for lg in league_list:
            if league == lg:
                return True
        return False        


    def __is_start_time(self, time : datetime) -> bool:
        '''
        Timer for start filling db out
        '''
        return time.hour == self.HOUR_FOR_START and time.minute == self.MINUTE_FOR_START