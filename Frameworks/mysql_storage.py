# pip install mysql-connector-python
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import logging
from Frameworks.onexbet import BettingApi


class MySQLStorage():
    '''
    Work with all tables
    '''

    def __init__(self, config) -> None:
        self.config = config
        self.bet_api = BettingApi(self.config)
        self.connection = self.create_connection()


    def create_connection(self) -> mysql.connector:
        '''
        Get connection
        '''
        try:
            mydb = mysql.connector.connect(
                        host = self.config['MYSQL']['localhost'],
                        port = self.config['MYSQL']['port'],
                        user = self.config['MYSQL']['user_name'],
                        password = self.config['MYSQL']['password'],
                        database = self.config['MYSQL']['db_name']          
                    )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.ERROR("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logging.ERROR("Database does not exist")
            else:
                logging.ERROR(err)           
        return mydb


    # Methods for onexdata table
    def multi_insert_to_onexdata(self) -> str:   
        '''
        Insetr some rows to mysql database onexdata table in format:
        data = (team1, team2, start_date, title), 
               (team1, team2, start_date, title) 
        '''
        data = self.bet_api.get_club_events()
        query = '''
                INSERT 
                INTO onexdata (team1, team2, start_date, title)
                VALUES 
                ''' + data
        return self.__execute_query(query)


    def clear_table_onexdata(self) -> str:
        '''
        Delete all rows from onexdata table
        '''
        query = '''TRUNCATE TABLE onexdata'''
        return self.__execute_query(query)


    def get_rows_by_current_time_onexdata(self) -> str:
        '''
        Get rows where time is today from onexdata table
        '''
        cur_time = self.__get_today_str()
        query = '''
                SELECT * 
                FROM onexdata 
                WHERE start_date LIKE '{d}%'       
                '''.format(d=cur_time)

        result = self.__execute_select_query(query)         
        return self.__form_str_onexdate_table(result)


    def get_rows_by_teams_name_onexdata(self, value : str) -> str:
        '''
        Get rows in the select where team1 or team2 
        equals a needed team from onexdata table
        '''
        query = '''
                SELECT *
                FROM onexdata
                WHERE lower(team1) = '{val}' or lower(team1) = '{val}'                   
                '''.format(val=value.lower())
        result = self.__execute_select_query(query)
        return self.__form_str_onexdate_table(result)     


    # Methods for league table
    def multi_insert_to_league(self, data : str) -> str:      
        '''
        Insetr some rows to mysql database league table in format:
        data = (league1), (league2) 
        '''
        
        query = ("INSERT INTO league "
                "(league) "
                "VALUES " + data)
        return self.__execute_query(query)


    def get_allrows_from_league(self, is_string_type : bool) -> str:
        '''
        Get all rows from league table
        '''
        query = '''
                SELECT * 
                FROM league
                '''
        result = self.__execute_select_query(query)
        if is_string_type:
            return self.__form_league_str(result)
        return result


    def get_row_from_league(self, name : str) -> list:
        '''
        Get row from league table by league name
        '''
        query = ("SELECT * FROM league WHERE " 
                "league_name = '{val}'"
                .format(val=name))
        return self.__execute_select_query(query)          


    # Methods for chat table
    def insert_to_chat(self, data : str) -> str:      
        '''
        Insetr row to mysql database chat table
        '''

        query = '''
                INSERT
                INTO chat (chat_id)    
                VALUES ({ci})
                '''.format(ci=data)
        return self.__execute_query(query)


    def get_row_from_chat(self, chatid : str) -> list:
        '''
        Get row from chat table
        '''
        query = '''
                SELECT * 
                FROM chat 
                WHERE chat_id = {val}                
                '''.format(val=chatid)
        return self.__execute_select_query(query)   


    # Methods for league_selection table
    def insert_to_ls(self, league : str, chat_id : str) -> str:      
        '''
        Insetr row to mysql database league_selection table in format:
        data = (chat_id, league_id)
        '''
        try:
            # Get id value from league table(0 index - first element)
            league_id = self.get_row_from_league(league)[0][0]
        except:
            return 'League is not correct. Try selecting from a list of leagues' 
        chat_id_field = self.get_row_from_chat(chat_id)[0][0]
        # Check whether there is a league in the league table or not
        query = '''
                INSERT
                INTO league_selection (chat_id, league_id)
                VALUES ({ci}, {li}) 
                '''.format(ci=chat_id_field,
                           li=league_id)
        return self.__execute_query(query)


    def get_rows_by_chatid_ls(self, chatid : str) -> str:
        '''
        Get rows from league_selection table 
        by id field from chat table
        '''
        query = '''
                SELECT league.league_name
                FROM league_selection 
                INNER JOIN chat 
                ON league_selection.chat_id = chat.id
                INNER JOIN league 
                ON league_selection.league_id = league.id
                WHERE chat.chat_id = {ci}
                '''.format(ci=chatid)
        result = self.__execute_select_query(query)
        return self.__form_str_leagues_list(result)


    def delete_by_chatid_ls(self, chatid : str) -> str:
        '''
        Delete data from league_selection table 
        by id field from chat table
        '''
        # Get chat_id value from chat table(0 index - first element)
        chat_id_field = self.get_row_from_chat(chatid)[0][0]
        query = '''
                DELETE 
                FROM league_selection
                WHERE chat_id = {ci}
                '''.format(ci=chat_id_field)
        return self.__execute_query(query)


    def delete_by_leaguename_chatid_ls(self, league : str, chatid : str) -> str:
        '''
        Delete data from league_selection table 
        by id field and chatid one from league table
        '''
        # Get id value from league table(0 index - first element)
        league_id = self.get_row_from_league(league)[0][0]
        # Get chat_id value from chat table(0 index - first element)
        chat_id_field = self.get_row_from_chat(chatid)[0][0]
        query = '''
                DELETE 
                FROM league_selection 
                WHERE league_id = {li} and chat_id = {ci}
                '''.format(li=league_id,
                           ci=chat_id_field)
        return self.__execute_query(query)     


    def get_allrows_from_ls(self) -> list:
        '''
        Get all rows from league_selection table
        '''
        query = '''
                SELECT * 
                FROM league_selection
                '''
        return self.__execute_select_query(query)


    def __get_today_str(self) -> str:
        '''
        Get string of today in format yyyy-MM-dd
        '''
        now = datetime.now()
        return now.strftime("%Y-%m-%d")


    def __form_league_str(self, leagues : list) -> str:
        '''
        Formint a readable string all leagues
        '''
        if not leagues:
            return 'The leagues table is empty'
        else:
            # 1 - is second element in the leagues table
            result = '\n'.join(
                [league_name[1] for league_name in leagues]
                )
            return result


    def __form_str_leagues_list(self, list_leagues : list) -> str:
        return 'There is not data' if not list_leagues else '\n'.join(
            # list_leagues - row from league_selection table
            # [0] - first element of chat table
            [str(league[0]) for league in list_leagues]
        )


    def __form_str_onexdate_table(self, events : list) -> str:
        '''
        Formint a readable string all events
        '''
        if not events:
            return 'There are not events today'    
        events_str = str()
        for event in events:
            events_str += self.__form_club_str(event)
        return events_str


    def __form_club_str(self, event : str) -> str:
        '''
        Create a line for printing
        '''
        return ('<b>{title}</b> {t1} vs {t2} time <b>{time}</b>\n'
                            .format(title=event[4],
                                    t1=event[1],
                                    t2=event[2],
                                    time=event[3][:10]))    


    def __execute_select_query(self, query : str) -> str: 
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except:
            return list()
            


    def __execute_query(self, query : str) -> str:
        try:
            cursor = self.connection.cursor(buffered=True)
            cursor.execute(query)
            self.connection.commit()
            return 'seccsessfully'
        except:
            return 'unseccsessfully'    