import argparse
import logging
import os
import sys
from tunes import get_tune
from hardware import play_tune, record
from brain import process_video
from contact_mothership import upload
from utils import be_patient

logging.basicConfig(
    format="%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s",
    level=logging.INFO,
    filename=os.path.join(os.path.dirname(__file__), 'daily.log')
)
parser = argparse.ArgumentParser(description='Become a better person'\
                                             ' via the medium of dance')
parser.add_argument('--debug', type=bool, default=False)
parser.add_argument('--christmas', type=bool, default=False)
args = parser.parse_args()

logging.info('Debug is {}'.format(args.debug))

db_path = os.environ.get('MORNING_PERSON_DB_PATH')
create_endpoint = os.environ.get('MORNING_PERSON_CREATE_ENDPOINT')
token = os.environ.get('MORNING_PERSON_REST_AUTH_TOKEN')

artist, name, url = get_tune(db_path, is_christmas=args.christmas)
if not args.debug:
    be_patient(min=0, max=2*60)
    play_tune(url)

if not args.debug:
    be_patient(min=30, max=60*2.5)

vid_fp, gif_fp, proc_vid_fp = record()

awakeness, happiness = process_video(vid_fp, gif_fp, proc_vid_fp)

process_metrics = (awakeness, happiness)
song_info = (artist, name, url)
upload(process_metrics, song_info, proc_vid_fp, create_endpoint, token)

logging.info('C\'est finit!')
