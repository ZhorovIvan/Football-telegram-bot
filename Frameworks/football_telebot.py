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
    clubs_list = '🧨club list'
    close_button = '🔚close'

    #Buttons for second menu
    get_list_button = '📚get list'
    add_club_button = '📇add club'
    remove_club_button = '🗑remove club'
    remove_all_clubs_button = '🗑remove all clubs'
    return_back_button = '🔙return back'


    def __init__(self, config) -> None:
        threading.Thread.__init__(self)
        self.config = config
        self.chat_id = self.config['TELEGRAM']['chat_id']
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
            button3 = types.KeyboardButton(self.clubs_list)
            button4 = types.KeyboardButton(self.close_button)
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
            button1 = types.KeyboardButton(self.get_list_button)
            button2 = types.KeyboardButton(self.add_club_button)
            button3 = types.KeyboardButton(self.remove_club_button)
            button4 = types.KeyboardButton(self.remove_all_clubs_button)
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
                              self.clubs_list]

            list_menu = [self.get_list_button,
                        self.add_club_button,
                        self.remove_club_button,
                        self.remove_all_clubs_button,
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

            #Check if whether there are rows in the league table or not
            if not self.mysql.get_allrows_from_league():
                self.mysql.multi_insert_to_league()


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
            elif message.text == self.clubs_list:
                work_with_list(message)       


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
                answer = self.storage.get_teams()
                __send_message_cu(answer, message.chat.id)


            elif message.text == self.add_club_button:
                __send_message_cu('<b>Write club</b>', message.chat.id) 
                self.bot.register_next_step_handler(message,
                                                    __add_club_to_club_storage)     

            elif message.text == self.remove_club_button:
                __send_message_cu('<b>Write club</b>')
                self.bot.register_next_step_handler(message,
                                                    __remove_club_from_storage)          

            elif message.text == self.remove_all_clubs_button:
                __send_message_cu('clubs have been removed', message.chat.id)
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
            answer = self.storage.delete_team(message.text)
            self.send_message_cu(answer, message.chat.id)           


        def __add_club_to_club_storage(message) -> None:
            '''
            Add a new club to the club list
            '''
            answer = self.storage.add_team(message.text)
            __send_message_cu(answer, message.chat.id)


        def __onexbet_get_current_events(message) -> None:
            '''
            Print out a list of the top five leagues that are playing today 
            '''
            events = self.mysql.get_rows_by_current_time_onexdata()
            self.bot.reply_to(message,
                            text=events,
                            parse_mode='html')


        def __form_str_from_top_leagues(events) -> str:
            '''
            Formint a string from top leagues in the database 
            '''
            events_str = str()
            league_list = [club for club in self.config['TELEGRAM']['leagues'].split(',')]
            for event in events:
                if event[4] in league_list:
                    events_str += __form_club_str(event)
            return events_str if not events_str else 'There is not data'                                


        def __form_str_from_all_leagues(events) -> str:
            '''
            Formint a string from all leagues in the database
            '''
            events_str = str()
            for event in events:
                events_str += __form_club_str(event)
            return events_str if not events_str else 'There is not data'


        def __form_club_str(event) -> str:
            '''
            Create a line for printing
            '''
            return ('<b>{title}</b> {t1} vs {t2} time <b>{time}</b>\n'
                    .format(title=event[4],
                            t1=event[1],
                            t2=event[2],
                            time=event[3][:10]))

    
        def __send_message_cu(text, receiver_id) -> None:
            self.bot.send_message(receiver_id,
                                text,
                                parse_mode='html') 


        self.bot.infinity_polling()                           

    