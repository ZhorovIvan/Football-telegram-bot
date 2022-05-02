import requests
import configparser
import re
import logging


class BettingApi():

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        

    def get_club_events(self, club_name):
        #English name pattern 
        pattern = '[A-z -]+'       
        response = self.get_response(self.config["FOOTBALL"]["events_url"])
        search_in = 'team1' if re.match(pattern, club_name) else 'team1_rus'
        events_data = str()
        for frame in response:
            try:
                if frame[search_in].lower() == club_name: 
                    events_data += '{} vs {} date {} coeficent (lose {} win {})\n'.format(
                        frame['team1'], frame['team2'], frame['date_start'][:10], 
                        frame['markets']['win1']['v'], frame['markets']['win2']['v']
                    )
            except KeyError:
                logging.warning('get_club_events: not found element {}'.format(str(e)))
        return events_data


    def get_today_matches(self):
        response = self.get_response(self.config["FOOTBALL"]["today_events_url"])
        today_matches = str()
        for frame in response:
            try:
                today_matches += '<b>{}</b>   {} vs {} date {} coeficent (lose {} win {})\n'.format(
                        frame['title'], frame['team1'], frame['team2'], 
                        frame['date_start'][:10], frame['markets']['win1']['v'], 
                        frame['markets']['win2']['v']
                    )
            except KeyError as e:
                logging.warning('get_today_matches: not found element {}'.format(str(e)))
        return today_matches


    def get_response(self, url):
        headers = {
            "Authorization": self.config["FOOTBALL"]["auth"]
        }
        return requests.request("GET", url, headers=headers).json()
    


# test = BettingApi()

# print(test.get_today_matches())