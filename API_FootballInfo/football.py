import requests
import configparser

class BettingApi():

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.read_config()


    def read_config(self):
        self.config.read("config.ini")


    def get_club_events(self, club_name):
        resp = self.get_response(self.config["FOOTBALL"]["events_url"])
        for x in resp:
            if x['team1'].lower() == 'barcelona': 
                print(x['team1'] + ' vs ' +  x['team2'] + ' date ' + x['date_start'][:10])

        
    def get_response(self, url):
        headers = {
            "Authorization": self.config["FOOTBALL"]["auth"]
        }
        return requests.request("GET", url, headers=headers).json()


test = BettingApi()

test.get_club_events('f')