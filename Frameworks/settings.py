import configparser as cp
import logging

def read_config() -> cp.ConfigParser:
    '''
    Read config.ini file
    '''
    config = cp.ConfigParser()
    config.read('config.ini')
    return config


def init_logger() -> None:
    logging.basicConfig(filename='log.log',
                                encoding='utf-8',
                                filemode='w',
                                level=logging.DEBUG)
    logging.info('Started')