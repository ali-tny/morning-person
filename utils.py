import logging
from time import sleep
from random import random
from math import floor

def be_patient(min, max):
    random_sleep_time = floor(random()*(max-min))
    total_sleep_time = min + random_sleep_time
    logging.info('Sleeping for {} seconds'.format(total_sleep_time))
    sleep(total_sleep_time)
