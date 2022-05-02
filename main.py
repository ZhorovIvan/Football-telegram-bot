import logging
from API_FootballInfo import football


def main():
    logging.basicConfig(filename='log.log', encoding='utf-8', filemode='w', level=logging.DEBUG)
    logging.info('Started')

    logging.info('Finished')
    pass


if __name__ == "__main__":
    main()