# pip install mysql-connector-python
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import logging
import configparser as cp
from Frameworks.onexbet import BettingApi



class MySQLStorage():
    '''
    Table schema 
    | id | team1 | team2 | start_date | title |
    '''     

    def __init__(self, config) -> None:
        self.config = config
        self.fApi = BettingApi(self.config)


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
        data = self.fApi.get_club_events()
        query = ("INSERT INTO onexdata "
                "(team1, team2, start_date, title) "
                "VALUES " + data)
        return self.__execute_query(query)


    def clear_table_onexdata(self) -> str:
        '''
        Delete all rows from onexdata table
        '''
        query = ("TRUNCATE TABLE onexdata")
        return self.__execute_query(query)


    def get_rows_by_current_time_onexdata(self) -> str:
        '''
        Get rows where time is today from onexdata table
        '''
        cur_time = self.get_today_str()
        query = ("SELECT * FROM onexdata" 
                "WHERE start_date LIKE '{d}%'"
                .format(d=cur_time))
        result = self.__execute_select_query(query)         
        return self.__form_str_onexdate_table(result)


    def get_rows_by_teams_name_onexdata(self, value : str) -> list:
        '''
        Get rows in the select where team1 or team2 
        equals a needed team from onexdata table
        '''
        query = ("SELECT * FROM onexdata WHERE " 
                "lower(team1) = '{val}' or lower(team1) = '{val}'"
                .format(val=value.lower()))        
        result = self.__execute_select_query(query)
        return self.__form_str_onexdate_table(result)     


    def get_today_str(self) -> str:
        '''
        Get string of today in format yyyy-MM-dd
        '''
        now = datetime.now()
        return now.strftime("%Y-%m-%d")


    # Methods for league table
    def multi_insert_to_league(self) -> str:      
        '''
        Insetr some rows to mysql database league table in format:
        data = (league1), (league2) 
        '''
        data = self.fApi.get_all_leagues()
        query = ("INSERT INTO league "
                "(league) "
                "VALUES " + data)
        return self.__execute_query(query)


    def get_row_from_league(self, name : str) -> list:
        '''
        Get row from league table
        '''
        query = ("SELECT * FROM league WHERE " 
                "league_name = '{val}'"
                .format(val=name))
        return self.__execute_select_query(query)


    def get_allrows_from_league(self) -> list:
        '''
        Get all rows from league table
        '''
        query = ("SELECT * FROM league")
        return self.__execute_select_query(query)                


    # Methods for chat table
    def insert_to_chat(self, data : str) -> str:      
        '''
        Insetr row to mysql database chat table
        '''
        query = ("INSERT INTO chat "
                "(chat_id) "
                "VALUES ({ci})"
                .format(ci=data))
        return self.__execute_query(query)


    def get_row_from_chat(self, data : str) -> list:
        '''
        Get row from chat table
        '''
        query = ("SELECT * FROM chat WHERE " 
                "chat_id = {val}"
                .format(val=data))
        return self.__execute_select_query(query)   


    # Methods for league_selection table
    def insert_to_ls(self, league : str, chat_id : str) -> str:      
        '''
        Insetr row to mysql database league_selection table in format:
        data = (chat_id, league_id)
        '''
        league_id = self.get_row_from_league(league)
        chat_id_field = self.get_row_from_chat(chat_id)
        query = ("INSERT INTO league_selection "
                "(chat_id, league_id) "
                "VALUES ({ci}, {li})"
                .format(ci=chat_id_field[0][0],
                         li=league_id[0][0]))
        return self.__execute_query(query)


    def get_rows_by_chatid_ls(self, chatid : str) -> str:
        '''
        Get rows from league_selection table 
        by id field from chat table
        '''
        chatid_field = self.get_row_from_chat(chatid)
        query = ("SELECT * FROM league_selection WHERE "
                 "chat_id = {ci}"
                 .format(ci=chatid_field[0]) )
        return self.__execute_query(query)


    def delete_by_chatid_ls(self, chatid : str) -> str:
        '''
        Delete data from league_selection table 
        by id field from chat table
        '''
        chat_id_field = self.get_row_from_chat(chatid)
        query = ("DELETE FROM league_selection "
                "WHERE chat_id = {ci}"
                .format(ci=chat_id_field[0][0]))
        return self.__execute_query(query)


    def delete_by_leaguename_ls(self, name : str):
        '''
        Delete data from league_selection table 
        by id field from league table
        '''
        league_id = self.get_row_from_league(name)
        query = ("DELETE FROM league_selection "
                "WHERE league_id = {li}"
                .format(li=league_id[0][0]))
        return self.__execute_query(query)     


    def get_allrows_from_ls(self) -> list:
        '''
        Get all rows from league_selection table
        '''
        query = ("SELECT * FROM league_selection")
        return self.__execute_select_query(query)


    def __form_str_onexdate_table(self, events : list) -> str:
        '''
        Formint a readable string all leagues
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


    def __execute_select_query(self, query : str) -> list: 
        try:
            con = self.create_connection()
            cursor = con.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except:
            return list()
        finally:
            con.close()             


    def __execute_query(self, query : str) -> str:
        try:
            con = self.create_connection()
            cursor = con.cursor(buffered=True)
            cursor.execute(query)
            con.commit()
            return 'seccsessfully'
        except:
            return 'unseccsessfully'    
        finally:
            con.close()  


#     def read_config(self) -> cp.ConfigParser:
#         '''
#         Read config.ini file
#         '''
#         config = cp.ConfigParser()
#         config.read('config.ini')
#         return config                           

# t = MySQLStorage()

# print(t.get_allrows_from_league())


