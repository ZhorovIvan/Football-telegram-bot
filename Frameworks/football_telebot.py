import telebot
import configparser as cp
import threading
from Frameworks.onexbet import BettingApi
from Frameworks.club_storage import ClubStorage
from Frameworks.mysql_storage import MySQLStorage
from telebot import types


class TelegramBot(threading.Thread):
    '''

    '''

# List top 5 legues 
    LIGUE_LIST = ['Spain. La Liga', 
            'England. National League',
            'Italy. Serie A',
            'France. Ligue 1',
            'Germany. Bundesliga']


    def __init__(self) -> None:
        threading.Thread.__init__(self)
        self.config = self.read_config()
        self.chat_id = self.config['TELEGRAM']['chat_id']
        self.bot = telebot.TeleBot(self.config['TELEGRAM']['token'])
        self.mysql = MySQLStorage()
        self.storage = ClubStorage()


    def run(self) -> None:
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message) -> None:
            '''
            
            '''
            sti = open('Images/welcome.webp', 'rb')
            self.bot.send_sticker(message.chat.id, sti)
            self.bot.send_message(message.chat.id,
                            'Hi, {} is new football assistance'
                            .format(self.bot.get_me().full_name),
                            parse_mode='html')


        @self.bot.message_handler(commands=['help'])
        def help_command(message) -> None:
            '''

            '''
            self.bot.send_message(message.chat.id,
                                '/1xbet - Open menu',
                                parse_mode='html')

        
        @self.bot.message_handler(commands=['1xbet'])
        def onexbet_command(message) -> None:
            '''
            Create general onexbet menu
            '''         
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('club')
            button2 = types.KeyboardButton('current')
            button3 = types.KeyboardButton('club list')
            button4 = types.KeyboardButton('close')
            markup.add(button1, button2, button3, button4)

            self.bot.send_message(message.chat.id,
                                '<b>Choose option</b>',
                                allow_sending_without_reply=False,
                                reply_markup=markup,
                                parse_mode='html')


        @self.bot.message_handler(commands=['button'])
        def work_with_list(message) -> None:
            '''
            Create second menu to work with the club_storage
            '''
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('get list')
            button2 = types.KeyboardButton('add club')
            button3 = types.KeyboardButton('remove club')
            button4 = types.KeyboardButton('remove all clubs')
            button5 = types.KeyboardButton('return back')
            button6 = types.KeyboardButton('close')          
            markup.add(button1, button2, button3, button4, button5, button6)

            self.bot.send_message(message.chat.id,
                                '<b>Choose action</b>',
                                reply_markup = markup,
                                parse_mode='html')    


        @self.bot.message_handler(content_types=['text'])
        def onexbet_choose_branch(message) -> None:
            '''
            Choose a step to analyse
            '''
            main_menu_list = ['club',
                            'current',
                            'club list']

            list_menu = ['get list',
                        'add club',
                        'remove club',
                        'remove all clubs',
                        'return back']

            if message.text in main_menu_list:
                main_button_memu(message)
            elif message.text in list_menu:
                second_button_menu(message)
            elif message.text == 'close':
                close_menu(message)
              

        def main_button_memu(message) -> None:
            '''
            Action for working with mysql data
            '''
            if message.text == 'club':                  
                self.bot.send_message(message.chat.id,
                                    '<b>Choose club</b>',
                                    parse_mode='html')
                self.bot.register_next_step_handler(message, onexbet_get_club_games)
            elif message.text == 'current':            
                onexbet_get_current_events(message)
            elif message.text == 'club list':
                work_with_list(message)       


        def onexbet_get_club_games(message) -> None:
            '''
            Get a name from the console
            '''
            markup = types.ReplyKeyboardRemove(selective = False)
            matches = self.mysql.get_rows_by_team_name(message.text)           
            matches_str = form_str_from_all_leagues(matches)
            self.bot.send_message(message.chat.id,
                                matches_str,
                                reply_markup = markup,
                                parse_mode='html')


        def second_button_menu(message) -> None:
            '''
            Action for working with club_storage
            '''
            if message.text == 'get list':
                answer = self.storage.get_teams()
                self.bot.send_message(message.chat.id,
                            answer,
                            parse_mode='html')

            elif message.text == 'add club':
                self.bot.send_message(message.chat.id,
                                '<b>Write club</b>',
                                parse_mode='html')  
                self.bot.register_next_step_handler(message, add_club_to_club_storage)     

            elif message.text == 'remove club':
                self.bot.send_message(message.chat.id,
                            '<b>Write club</b>',
                            parse_mode='html')
                self.bot.register_next_step_handler(message, remove_club_from_storage)          

            elif message.text == 'remove all clubs':
                self.storage.delete_all_teams()
                self.bot.send_message(message.chat.id,
                            'clubs have been removed',
                            parse_mode='html')
            else:
                onexbet_command(message)
                return              


        def close_menu(message) -> None:
            '''
            Close menu function
            '''
            markup = types.ReplyKeyboardRemove(selective = False)
            self.bot.send_message(message.chat.id,
                                '<b>Close menu</b>',
                                reply_markup=markup,
                                parse_mode='html')            


        def remove_club_from_storage(message) -> None:
            '''
            Remove club by name from club storage
            '''
            answer = self.storage.delete_team(message.text)
            self.bot.send_message(message.chat.id,
                                answer,
                                parse_mode='html')            


        def add_club_to_club_storage(message):
            '''
            Add a club to the club list
            '''
            answer = self.storage.add_team(message.text)
            self.bot.send_message(message.chat.id,
                                answer,
                                parse_mode='html')   


        def onexbet_get_current_events(message) -> None:
            '''
            Print out a list of the top five leagues that are playing today 
            '''
            events = self.mysql.get_rows_by_time()
            events_str = form_str_from_top_leagues(events)

            self.bot.reply_to(message,
                            text=events_str,
                            parse_mode='html')


        def form_str_from_top_leagues(self, events):
            '''
            Formint a string from top leagues in the database 
            '''
            events_str = str()
            for event in events:
                if event[4] in self.LIGUE_LIST:
                    events_str += ('<b>{title}</b> {t1} vs {t2} {time}\n'
                                  .format(event[4], event[1] , event[2], event[3][10:]))
            return events_str if events_str == '' else 'There is not data'                                


        def form_str_from_all_leagues(events):
            '''
            Formint a string from all leagues in the database
            '''
            events_str = str()
            for event in events:
                events_str += ('<b>{title}</b> {t1} vs {t2} {time}\n'
                                .format(event[4], event[1] , event[2], event[3][10:]))
            return events_str if events_str == '' else 'There is not data'             


        self.bot.infinity_polling()


    def read_config(self) -> cp:
        '''
        read config.ini file
        '''
        config = cp.ConfigParser()
        config.read('config.ini')
        return config