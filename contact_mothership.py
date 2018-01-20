import os
from datetime import datetime
import requests
from retrying import retry

# Add a dash of exponential backoff
@retry(wait_exponential_multiplier=1000, wait_exponential_max=20000,
       stop_max_attempt_number=5)
def upload(process_metrics, song_info, gif_fp, create_endpoint, token):
    awakeness, happiness = process_metrics
    song_artist, song_name, song_url = song_info
    logging.info('Uploading')
    url = create_endpoint
    today = datetime.now()
    payload = {
        'recognised_pct':awakeness,
        'happy_pct':happiness,
        'song_url':song_url,
        'song_name':'{} - {}'.format(song_artist, song_name),
        'date':today.strftime('%Y-%m-%d %H:%M'),
    }
    files = {
        'image':open(gif_fp, 'rb')
    }
    headers = {
        "Authorization":token
    }

    try:
        r = requests.post(url=url, data=payload, files=files, headers=headers)
    except Exception as e:
        logging.error('Upload error', exc_info=1)
        raise e
    if r.status_code != 400:
        logging.error('Upload with status code {}'.format(r.status_code))
        raise Exception(r.status_code)
