import telebot
import configparser as cp
import sys
#Path to Football api folder
sys.path.insert(0, 'C:\\Users\\jorov\\Desktop\\football-Bot\\API_FootballInfo')
import football

config = cp.ConfigParser()
config.read('config.ini')
API_TOKEN = config['TELEGRAM']['token']
bot = telebot.TeleBot(API_TOKEN)
fApi = football.BettingApi()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    sti = open('Images/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, 'Hi, {} is new football assistance'
                                       .format(bot.get_me().full_name),
                                       parse_mode='html')


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, '/club - three matches in future\n' + 
                                      '/events_today - show all football matches for today',
                                       parse_mode='html')


@bot.message_handler(commands=['club'])
def help_command(message):
    bot.send_message(message.chat.id, 'Write down yours')
    bot.register_next_step_handler(message, get_club)


def get_club(message):
    bot.send_message(message.chat.id, "test")


@bot.message_handler(commands=['events_today'])
def events_today_command(message):
    events = fApi.get_club_events()
    bot.send_message(message.chat.id, events, parse_mode='html')


bot.infinity_polling()