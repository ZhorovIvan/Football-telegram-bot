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

    def __init__(self) -> None:
        self.config = self.read_config()
        self.fApi = BettingApi()


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


    # Methods for team table
    def insert_row_to_team(self, chat_id, name) -> str:
        '''
        Get info from in format
        | chat_id | team_name |
        '''
        query = ("INSERT INTO team "
                "(chat_id, team_name) "
                "VALUES ({id}, '{n}')"
                .format(id=chat_id, n=name))
        return self.__execute_query(query)


    def get_rows_by_id_team(self, chat_id) -> list:
        '''
        Get data by chat id from team table
        '''
        query = ("SELECT * FROM team " 
                "WHERE chat_id = {id}"
                .format(id=chat_id))
        return self.__execute_select_query(query)


    def get_all_rows_team(self) -> list:
        '''
        Get all rows from team table
        '''
        query = "SELECT * FROM team" 
        return self.__execute_select_query(query)    


    def delete_by_name_id_team(self, chat_id, name) -> str:
        '''
        Clear row by name and chat_id in team table
        '''
        query = ("DELETE FROM team "
                "WHERE chat_id = {id} AND " 
                "team_name = '{n}'"
                .format(id=chat_id, n=name))
        return self.__execute_query(query)


    def clear_table_team(self) -> str:
        '''
        Delete all rows from team table
        '''
        query = ("TRUNCATE TABLE team")
        return self.execute_query(query)

    
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


    def clear_table_onexdata(self, name) -> str:
        '''
        Delete all rows from onexdata table
        '''
        query = ("TRUNCATE TABLE onexdata")
        return self.__execute_query(query)


    def get_rows_by_current_time_onexdata(self) -> list:
        '''
        Get rows where time is today from onexdata table
        '''
        cur_time = self.get_today_str()
        query = ("SELECT * FROM onexdata" 
                    "WHERE start_date LIKE '{d}%'"
                    .format(d=cur_time))
        return self.__execute_select_query(query)


    def get_rows_by_teams_name_onexdata(self, value) -> list:
        '''
        Get rows in the select where team1 or team2 
        equals a needed team from onexdata table
        '''
        query = ("SELECT * FROM onexdata WHERE" 
                "team1 = '{val}' or team1 = '{val}'"
                .format(val=value))
        return self.__execute_select_query(query)        


    def get_today_str(self) -> str:
        '''
        Get string of today in format yyyy-MM-dd
        '''
        now = datetime.now()
        return now.strftime("%Y-%m-%d")


    # Methods for league table
    def multi_insert_to_league(self) -> str:
        
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


    def __execute_select_query(self, query) -> list: 
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


    def __execute_query(self, query) -> str:
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


    def read_config(self) -> cp.ConfigParser:
        '''
        Read config.ini file
        '''
        config = cp.ConfigParser()
        config.read('config.ini')
        return config                           

t = MySQLStorage()

print(t.delete_by_name_id_team(1, '23123'))





