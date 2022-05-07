import telebot
import configparser as cp
import sys
#Path to Football api folder
sys.path.insert(0, 'C:\\Users\\jorov\\Desktop\\football-Bot\\API_FootballInfo')
import onexbet
from telebot import types


config = cp.ConfigParser()
config.read('config.ini')
API_TOKEN = config['TELEGRAM']['token']
bot = telebot.TeleBot(API_TOKEN)
fApi = onexbet.BettingApi()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    sti = open('Images/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id,
                    'Hi, {} is new football assistance'
                    .format(bot.get_me().full_name),
                    parse_mode='html')


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id,
                    '/1xbet - GET info from onexbet\n', 
                     parse_mode='html')

 
@bot.message_handler(commands=['1xbet'])
def onexbet_command(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Club')
    button2 = types.KeyboardButton('Current')

    markup.add(button1, button2)

    bot.send_message(message.chat.id,
                    'Choose option',
                    reply_markup=markup)


@bot.message_handler(content_types=['text'])
def onexbet_choose_branch(message):
    markup = types.ReplyKeyboardRemove(selective = False)
    if message.chat.type == 'private':
        if message.text == 'Club':          
            bot.send_message(message.chat.id,
                    'Choose club',
                    reply_markup = markup,
                    parse_mode='html')
            bot.register_next_step_handler(message, onexbet_get_club_games)
        if message.text == 'Current':
            bot.send_message(message.chat.id,
                    'Waiting...',
                    reply_markup = markup,
                    parse_mode='html')            
            onexbet_get_current_events(message)


def onexbet_get_club_games(message):
    matches = fApi.get_club_events(message.text)
    markup = types.ReplyKeyboardRemove(selective = False)
    bot.send_message(message.chat.id,
                     matches,
                     reply_markup = markup,
                     parse_mode='html')


def onexbet_get_current_events(message):
    events = fApi.get_today_matches()
    if len(events) > 4095:
        for x in range(0, len(events), 4095):
            bot.reply_to(message,
                         text=events[x:x+4095],
                         parse_mode='html')
    else:
        bot.reply_to(message,
                     text=events,
                     parse_mode='html')
                  



bot.infinity_polling()      