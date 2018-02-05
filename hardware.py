import logging
import os
from datetime import datetime

def play_tune(url):
    logging.info('Playing song')
    func_fp = get_bash_functions_path()
    play_song = '/bin/bash -c "source {}; youtube {}"'.format(func_fp, url)
    os.system(play_song + ' &')

def record():
    vid_fp, gif_fp, proc_vid_fp = get_media_paths()
    func_fp = get_bash_functions_path()
    record = '/bin/bash -c "source {}; video {}"'.format(func_fp, vid_fp)
    logging.info('Recording!')
    os.system(record)
    return vid_fp, gif_fp, proc_vid_fp

def get_media_paths():
    today = datetime.now()
    dir_template= os.path.join(os.path.dirname(__file__), 'media/%Y/%m/%d/')
    media_dir = today.strftime(dir_template)
    if not os.path.isdir(media_dir):
        os.makedirs(media_dir)
    vid_fname = today.strftime("%H-%M.mp4")
    gif_fname = today.strftime("%H-%M.gif")
    proc_vid_fname = today.strftime("%H-%M_proc.mp4")
    gif_fp = os.path.join(media_dir, gif_fname)
    vid_fp = os.path.join(media_dir, vid_fname)
    proc_vid_fp = os.path.join(media_dir, proc_vid_fname)
    return vid_fp, gif_fp, proc_vid_fp

def get_bash_functions_path():
    return os.path.join(os.path.dirname(__file__), 'eyes_and_ears.sh')

