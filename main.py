import logging
from Frameworks.football_telebot import TelegramBot
from Frameworks.sender_message import Timer


def main() -> None:
    logging.basicConfig(filename='log.log',
                                encoding='utf-8',
                                filemode='w',
                                level=logging.DEBUG)
    logging.info('Started')

    process1 = Timer()
    process2 = TelegramBot()

    process1.start()
    process2.start()
 

if __name__ == "__main__":
    main()