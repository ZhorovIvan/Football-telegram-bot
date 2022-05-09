import telebot
import configparser as cp
import threading
from Frameworks.onexbet import BettingApi
from Frameworks.club_storage import ClubStorage
from telebot import types


class TelegramBot(threading.Thread):

    def __init__(self) -> None:
        threading.Thread.__init__(self)
        self.config = self.read_config()
        self.chat_id = self.config['TELEGRAM']['chat_id']
        self.bot = telebot.TeleBot(self.config['TELEGRAM']['token'])
        self.storage = ClubStorage()
        self.fApi = BettingApi()


    def run(self) -> None:
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message) -> None:
            sti = open('Images/welcome.webp', 'rb')
            self.bot.send_sticker(message.chat.id, sti)
            self.bot.send_message(message.chat.id,
                            'Hi, {} is new football assistance'
                            .format(self.bot.get_me().full_name),
                            parse_mode='html')


        @self.bot.message_handler(commands=['help'])
        def help_command(message) -> None:
            self.bot.send_message(message.chat.id,
                                '/1xbet - Open menu',
                                parse_mode='html')

        
        @self.bot.message_handler(commands=['1xbet'])
        def onexbet_command(message) -> None:           
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
                list_button_menu(message)
            elif message.text == 'close':
                close_menu(message)
              

        def main_button_memu(message) -> None:
            if message.text == 'club':                     
                self.bot.send_message(message.chat.id,
                                    '<b>Choose club</b>',
                                    parse_mode='html')
                self.bot.register_next_step_handler(message, onexbet_get_club_games)
            elif message.text == 'current':
                self.bot.send_message(message.chat.id,
                                    '<b>Waiting...</b>',
                                    parse_mode='html')            
                onexbet_get_current_events(message)
            elif message.text == 'club list':
                work_with_list(message)       


        def onexbet_get_club_games(message) -> None:
            self.bot.send_message(message.chat.id,
                                    '<b>Waiting...</b>',
                                    parse_mode='html')
            matches = self.fApi.get_club_events(message.text)
            markup = types.ReplyKeyboardRemove(selective = False)
            self.bot.send_message(message.chat.id,
                                matches,
                                reply_markup = markup,
                                parse_mode='html')    


        def list_button_menu(message) -> None:
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
            Add club to club list
            '''
            answer = self.storage.add_team(message.text)
            self.bot.send_message(message.chat.id,
                                answer,
                                parse_mode='html')   


        def onexbet_get_current_events(message) -> None:
            events = self.fApi.get_today_matches()
            if len(events) > 4095:
                for x in range(0, len(events), 4095):
                    self.bot.reply_to(message,
                                    text=events[x:x+4095],
                                    parse_mode='html')
            else:
                self.bot.reply_to(message,
                                text=events,
                                parse_mode='html')
            

        self.bot.infinity_polling()


    def read_config(self) -> cp:
        '''
        read config.ini file
        '''
        config = cp.ConfigParser()
        config.read('config.ini')
        return config