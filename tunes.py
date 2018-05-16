import logging
from datetime import datetime, timedelta
import sqlite3 as sql
from utils import is_birthday

def get_tune(db_path, is_christmas):
    logging.info('Getting song info')
    today = datetime.now()
    db = sql.connect(db_path)
    c = db.cursor()
    week_ago = today - timedelta(days=7)
    xmas_filter = '= 1' if is_christmas else 'IS NULL'
    c.execute('''
    SELECT
        url, name, artist_name
    FROM songs
    WHERE
        (DATE(last_played_date) < DATE('{}')
        OR last_played_date IS NULL)
        AND retired_date IS NULL
        AND christmas {}
    ORDER BY RANDOM()
    LIMIT 1;
    '''.format(week_ago.strftime('%Y-%m-%d'), xmas_filter))
    song = c.fetchone()
    song_url = song[0]
    song_name = song[1]
    song_artist = song[2]

    update_last_played(db, song_url, today)
    logging.info('Today\'s song: {} - {}'.format(song_artist, song_name))
    return song_artist, song_name, song_url

def update_last_played(db, song_url, date):
    c = db.cursor()
    c.execute('''
    UPDATE songs SET last_played_date = '{}' WHERE url = '{}'
    '''.format(date.strftime('%Y-%m-%d'), song_url))
    db.commit()

