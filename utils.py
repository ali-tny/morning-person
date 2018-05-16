import logging
import os
from time import sleep
from random import random
from math import floor
from datetime import date

def be_patient(min, max):
    random_sleep_time = floor(random()*(max-min))
    total_sleep_time = min + random_sleep_time
    logging.info('Sleeping for {} seconds'.format(total_sleep_time))
    sleep(total_sleep_time)

def is_birthday():
    today = date.today()
    is_bday_month = today.month == os.environ.get('BDAY_MONTH')
    is_bday_day = today.day == os.environ.get('BDAY_DAY')
    return is_bday_month and is_bday_day
