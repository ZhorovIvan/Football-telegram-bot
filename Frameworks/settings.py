import configparser as cp
import logging
import subprocess
import sys


def read_config() -> cp.ConfigParser:
    '''
    Read config.ini file
    '''
    config = cp.ConfigParser()
    config.read('config.ini')
    return config


def init_logger() -> logging:
    logger =logging.basicConfig(filename='log.log',
                        encoding='utf-8',
                        filemode='w',
                        level=logging.DEBUG)
    logging.info('Started')
    return logger


def preparation() -> None:
    install('threading')
    install('logging')
    install('configparser')
    install('json')


def install(package) -> None:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])