import logging
from Frameworks.football_telebot import TelegramBot
from Frameworks.fill_db_table import Timer
from Frameworks.settings import read_config, init_logger


def main() -> None:
    init_logger()
    config = read_config()

    process1 = Timer(config)
    process2 = TelegramBot(config)

    process1.start()
    process2.start()
 

if __name__ == "__main__":
    # try:
        main()
    # except Exception as e:
    #     logging.fatal(e)