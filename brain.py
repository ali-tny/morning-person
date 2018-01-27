import logging
from datetime import datetime
import os
import numpy as np
import cv2
import imageio
import moviepy.editor as mpy
import imutils

def process_video(video_fp, gif_fp, proc_vid_chrome_fp, proc_vid_safari_fp):
    logging.info('Processing...')
    cap = cv2.VideoCapture(video_fp)
    grays = []
    while (cap.isOpened()):
        ret,img = cap.read()
        if img is None:
            break
        try:
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            grays.append(gray.copy())
        except:
            gray = img

    avg = None
    # For apoorva's house, delta_thresh = 5, min_area = 36000
    delta_thresh = 2
    min_area = 10000
    processed = []
    last_boxes = np.array([[0,0,0,0]])
    movement_size = 0 
    awake = 0
    for img in grays:
        gray = img.copy()
        
        if avg is None:
            avg = gray.copy().astype("float")
            continue

        cv2.accumulateWeighted(gray, avg, 0.5)
        frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
        
        thresh = cv2.threshold(frame_delta, delta_thresh, 255,
            cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
     
        is_awake = False
        w, h = 0, 0
        for c in cnts:
            if cv2.contourArea(c) < min_area:
                continue
     
            (x, y, w, h) = cv2.boundingRect(c)
            x = np.clip(x+50, 0, 600)
            y = np.clip(y-50, 0, y)
            w = np.clip(w-50, 0, w)
            h = np.clip(h-50, 0, h)
            last_boxes = np.append(last_boxes, np.array([[x,y,w,h]]), axis=0)
            if len(last_boxes)>0:
                avgs = last_boxes[-20:].mean(axis=0).astype(int)
                x_avg, y_avg, w_avg, h_avg = avgs
            
            cv2.rectangle(gray, (x_avg, y_avg), (x_avg + w_avg, y_avg + h_avg), 
                          (255, 0, 0), 2)
            text = 'morning_person'
            font_scale = 1.5
            font = cv2.FONT_HERSHEY_SIMPLEX
            color = (255,0,0)
            linetype = 5
            cv2.putText(gray, text, (x_avg,y_avg+h_avg+30), font, font_scale,
                color, linetype)
            is_awake = True
            
        if is_awake:
            awake += 1
        if len(cnts) > 0:
            movement_size += w*h
            
        text = datetime.now().strftime("%I:%M %p")
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        color = (0,0,0)
        linetype = 5
        cv2.putText(gray, text, (gray.shape[1]-250,50), font, font_scale, color, 
                    linetype)
        small = cv2.resize(gray, (0,0), fx=0.5, fy=0.5) 
        processed.append(small)
        
    awakeness = awake / len(processed)
    happiness = movement_size / ((600 ** 2)*len(processed))

    reduce_factor = 3
    smaller = [frame for i, frame in enumerate(processed) 
               if i % reduce_factor == 0]
    imageio.mimsave(gif_fp, smaller, fps=np.floor(23 / reduce_factor), 
                    subrectangles=True)

    convert(gif_fp, proc_vid_chrome_fp, 'libx264')
    convert(gif_fp, proc_vid_safari_fp, 'mpeg4')

    logging.info('Process outputs - awakeness:{} happiness:{}'.format(
        awakeness,
        happiness
    ))

    return awakeness, happiness

def convert(gif_fp, proc_vid_fp, codec):
    convert_sh = "/usr/local/bin/ffmpeg -i {} -vcodec {} {} -y".format(
        gif_fp,
        codec,
        proc_vid_fp
    )
    os.system(convert_sh)
