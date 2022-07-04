<<<<<<< HEAD
import configparser as cp

config = cp.ConfigParser()
config.read('config.ini')

print(config['TELEGRAM']['token'] == '1918073988:AAHaAem6Y4U_bko3SESMTxa8wvgjy51X2r4')
=======
from Frameworks import settings, fill_db_table, football_telebot, mysql_storage, onexbet

def main() -> None:
    global logger
    settings.init_logger

    logger = settings.init_logger()

    settings.preparation()

    config = settings.read_config()
    mysql = mysql_storage.MySQLStorage(config)
    bet_api = onexbet.BettingApi(config)
    
    process1 = fill_db_table.Timer(config, mysql, bet_api, logger)
    process2 = football_telebot.TelegramBot(config, mysql)

    process1.start()
    process2.start()
 

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.fatal(e)
>>>>>>> 048dda2 (test version)
