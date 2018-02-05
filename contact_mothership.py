import boto3
import os
import logging
from datetime import datetime
import requests
from retrying import retry

# Add a dash of exponential backoff
@retry(wait_exponential_multiplier=1000, wait_exponential_max=20000,
       stop_max_attempt_number=5)
def upload(process_metrics, song_info, proc_vid_fp, create_endpoint, token):
    awakeness, happiness = process_metrics
    song_artist, song_name, song_url = song_info
    logging.info('Uploading to S3')
    video_url = upload_to_s3(proc_vid_fp)
    logging.info('Uploading to mothership')
    url = create_endpoint
    today = datetime.now()
    payload = {
        'recognised_pct':awakeness,
        'happy_pct':happiness,
        'song_url':song_url,
        'song_name':'{} - {}'.format(song_artist, song_name),
        'date':today.strftime('%Y-%m-%d %H:%M'),
        'video_url':video_url,
    }
    headers = {
        "Authorization":"Token {}".format(token)
    }

    try:
        r = requests.post(url=url, data=payload, headers=headers)
    except Exception as e:
        logging.error('Upload error', exc_info=1)
        raise e
    if r.status_code != 201:
        logging.error('Upload with status code {}'.format(r.status_code))
        raise Exception(r.status_code)
    return r

def upload_to_s3(proc_vid_fp):
    now = datetime.now()
    key = now.strftime('%Y/%m/%d-%H-%M-%S.mp4')
    bucket = 'morning-person-images'
    res = boto3.resource('s3')
    data = open(proc_vid_fp, 'rb')
    try:
        res.Bucket(bucket).put_object(Key=key, Body=data)
        return "http://{}.s3.amazonaws.com/{}".format(bucket, key)
    except:
        logging.error('S3 upload error', exc_info=1)

