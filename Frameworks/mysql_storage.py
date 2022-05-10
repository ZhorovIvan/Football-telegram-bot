# pip install mysql-connector-python
import mysql.connector
import configparser as cp
from mysql.connector import errorcode
from datetime import datetime
import logging


class MySQLStorage():

    '''
    Table schema 
    | id | team1 | team2 | data_start | title |
    '''     

    def __init__(self) -> None:
        self.config = self.read_config()


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


    def multi_insert_to_db(self, data) -> None:
        '''
        Insetr some rows to mysql database in format:
        data = (team1, team2, start_date, title), 
               (team1, team2, start_date, title) 
        '''
        try:
            con = self.create_connection()
            cursor = con.cursor()
            add_club_data = ("INSERT INTO onexdata "
                            "(team1, team2, start_date, title) "
                            "VALUES " + data)
            cursor.execute(add_club_data)
            con.commit()
        finally:
            con.close()


    def clear_table(self) -> None:
        '''
        Delete all rows from onexdata table
        '''
        try:
            con = self.create_connection()
            cursor = con.cursor()
            clear_query = ("TRUNCATE TABLE onexdata")
            cursor.execute(clear_query)
            con.commit()
        finally:
            con.close()


    def get_rows_by_time(self) -> list:
        '''
        Get rows where time is today
        '''
        try:
            con = self.create_connection()
            cursor = con.cursor()
            clear_query = ("SELECT * FROM onexdata WHERE data_start = '{}'"
                                            .format(self.get_today_str()))
            cursor.execute(clear_query)
            result = cursor.fetchall()
            return result
        finally:
            con.close()


    def get_rows_by_team_name(self, value) -> list:
        '''
        Get rows in the select where team1 or team2 equals a needed team
        '''
        try:
            con = self.create_connection()
            cursor = con.cursor()
            clear_query = ("SELECT * FROM onexdata WHERE team1 = '{val}' or team1 = '{val}'"
                                                                        .format(val=value))
            cursor.execute(clear_query)
            result = cursor.fetchall()
            return result
        finally:
            con.close()        


    def get_today_str(self) -> str:
        '''
        Get string of today in format yyyy-MM-dd
        '''
        now = datetime.now()
        return now.strftime("%Y-%m-%d")


    def read_config(self) -> cp:
        '''
        read config.ini file
        '''
        config = cp.ConfigParser()
        config.read('config.ini')
        return config