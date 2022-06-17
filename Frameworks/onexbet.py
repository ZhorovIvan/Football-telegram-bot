import json
import requests
import configparser as cp
import logging


class BettingApi():
    '''
    GET info from API 1xBet
    https://docs.betting-api.com/1xbet/index.html#api-Football-FootballLineAll
    '''

    def __init__(self, config) -> None:
        self.config = config


    def get_club_events(self) -> str:
        '''
        Get all the information on the clubs performance over the three matches ahead
        '''   
        response = self.__get_response(self.config["FOOTBALL"]["events_url"])
        data_for_insert_to_onexdata = str()
        for frame in response:
            data_for_insert_to_onexdata += self.__get_info_for_onexdata(frame)
        return data_for_insert_to_onexdata[:-1]


    def __get_info_for_onexdata(self, frame) -> str:
        '''
        Get data for inseting
        '''
        try:    
            team1 = frame['team1'].replace("'", "")
            team2 = frame['team2'].replace("'", "")
            date_start = frame['date_start'].replace("'", "")
            title = frame['title'].replace("'", "")
            data = ("('{t1}', '{t2}', '{dt}', '{ti}' ),"
                    .format(t1=team1, t2=team2, dt=date_start, ti=title))
            return data 
        except KeyError as e:
            logging.warning('get_club_events: not found element {}'.format(str(e)))
        except Exception as e:
            logging.error(str(e))        
        return ''


    def __get_response(self, url) -> json:
        '''
        GET responce
        '''
        headers = {
            "Authorization": self.config["FOOTBALL"]["auth"]
            }
        return requests.request("GET", url, headers=headers).json()