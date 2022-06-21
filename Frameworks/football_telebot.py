import telebot
import threading
from Frameworks.mysql_storage import MySQLStorage
from telebot import types


class TelegramBot(threading.Thread):
    '''
    Football bot
    It can print some football events info
    All information containts in MySQL db
    API for working https://docs.betting-api.com/1xbet/index.html#api-Football-FootballLineAll
    Telebot documentation https://github.com/eternnoir/pyTelegramBotAPI
    '''
    #Buttons for main menu
    club_button = '⚽️club' 
    current_events = '🚀current events' 
    favorite_list = '🧨my event list'
    close_button = '🔚close'
    all_league_button = '🥅all leagues'

    #Buttons for second menu
    get_list_button = '📚get list'
    add_league_button = '📇add league'
    remove_league_button = '🗑remove league'
    remove_all_leagues_button = '🗑remove all leagues'
    return_back_button = '🔙return back'


    def __init__(self, config) -> None:
        threading.Thread.__init__(self)
        self.config = config
        self.bot = telebot.TeleBot(self.config['TELEGRAM']['token'])
        self.mysql = MySQLStorage(self.config)


    def run(self) -> None:
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message) -> None:           
            sti = open('Images/welcome.webp', 'rb')
            self.bot.send_sticker(message.chat.id, sti)
            __send_message_cu('Hi, {} is new football assistance'
                                .format(self.bot.get_me().full_name),
                                message.chat.id)
            __fill_database(message.chat.id)                    


        @self.bot.message_handler(commands=['help'])
        def help_command(message) -> None:
            __send_message_cu('/1xbet - Open general 1xmenu',message.chat.id)


        @self.bot.message_handler(commands=['1xbet'])
        def onexbet_command(message) -> None:
            '''
            Create general onexbet menu
            '''         
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton(self.club_button)
            button2 = types.KeyboardButton(self.current_events)
            button3 = types.KeyboardButton(self.favorite_list)
            button4 = types.KeyboardButton(self.close_button)
            button5 = types.KeyboardButton(self.all_league_button)
            markup.add(button1, button2, button3, button4, button5)

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
            button1 = types.KeyboardButton(self.get_list_button)
            button2 = types.KeyboardButton(self.add_league_button)
            button3 = types.KeyboardButton(self.remove_league_button)
            button4 = types.KeyboardButton(self.remove_all_leagues_button)
            button5 = types.KeyboardButton(self.return_back_button)
            button6 = types.KeyboardButton(self.close_button)          
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
            main_menu_list = [self.club_button,
                              self.current_events,
                              self.favorite_list,
                              self.all_league_button]

            list_menu = [self.get_list_button,
                        self.add_league_button,
                        self.remove_league_button,
                        self.remove_all_leagues_button,
                        self.return_back_button]

            if message.text in main_menu_list:
                __main_button_memu(message)
            elif message.text in list_menu:
                __second_button_menu(message)
            elif message.text == self.close_button:
                __close_menu(message)


        def __fill_database(chatid) -> None:
            '''
            Add a chat id to data base
            Filling db out if the league table and the 
            onexbet table is empty
            '''
            #Check if whether there is chat id in the chat table or not 
            if not self.mysql.get_row_from_chat(chatid):
               self.mysql.insert_to_chat(chatid)

            #Check if whether there are rows in the onexdata table or not
            if not self.mysql.get_rows_by_current_time_onexdata():
                self.mysql.multi_insert_to_onexdata()


        def __main_button_memu(message) -> None:
            '''
            Action for working with mysql data
            '''
            if message.text == self.club_button:
                __send_message_cu('<b>Choose club</b>', message.chat.id)
                self.bot.register_next_step_handler(message,
                                                    __onexbet_get_club_games)
            elif message.text == self.current_events:            
                __onexbet_get_current_events(message)
            elif message.text == self.favorite_list:
                work_with_list(message)
            elif message.text == self.all_league_button:
                __print_all_leagues(message)      


        def __print_all_leagues(message):
            leagues = self.mysql.get_allrows_from_league()
            __send_message_cu(leagues, message.chat.id)


        def __onexbet_get_club_games(message) -> None:
            '''
            Get a name from the console
            '''
            matches = self.mysql.get_rows_by_teams_name_onexdata(message.text)
            __send_message_cu(matches, message.chat.id)


        def __second_button_menu(message) -> None:
            '''
            Action for working with club_storage
            '''
            if message.text == self.get_list_button:               
                answer = self.mysql.get_rows_by_chatid_ls(message.chat.id)
                __send_message_cu(answer, message.chat.id)

            elif message.text == self.add_league_button:
                __send_message_cu('<b>Write league</b>', message.chat.id) 
                self.bot.register_next_step_handler(message,
                                                    __add_club_to_club_storage)     

            elif message.text == self.remove_league_button:
                __send_message_cu('<b>Write league</b>', message.chat.id)
                self.bot.register_next_step_handler(message,
                                                    __remove_club_from_storage)          

            elif message.text == self.remove_all_leagues_button:
                answer = self.mysql.delete_by_chatid_ls(message.chat.id)
                __send_message_cu(answer, message.chat.id)
            else:
                onexbet_command(message)
                return


        def __close_menu(message) -> None:
            '''
            Close menu function
            '''
            markup = types.ReplyKeyboardRemove(selective = False)
            self.bot.send_message(message.chat.id,
                                '<b>Close menu</b>',
                                reply_markup=markup,
                                parse_mode='html')            


        def __remove_club_from_storage(message) -> None:
            '''
            Remove club by name from club storage
            '''
            answer = self.mysql.delete_by_leaguename_chatid_ls(message.text,
                                                               message.chat.id)
            __send_message_cu(answer, message.chat.id)           


        def __add_club_to_club_storage(message) -> None:
            '''
            Add a new club to the club list
            '''
            answer = self.mysql.insert_to_ls(message.text, message.chat.id)
            __send_message_cu(answer, message.chat.id)


        def __onexbet_get_current_events(message) -> None:
            '''
            Print out a list of the top five leagues that are playing today 
            '''
            events = self.mysql.get_rows_by_current_time_onexdata()
            self.bot.reply_to(message,
                            text=events,
                            parse_mode='html')


        def __send_message_cu(text, receiver_id) -> None:
            self.bot.send_message(receiver_id,
                                text,
                                parse_mode='html') 


        self.bot.infinity_polling()