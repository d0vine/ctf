#!/usr/bin/env python
import os
import sys
import cv2

def process_img(img_path):
    img = cv2.imread(img_path)
    rows, cols, _ = img.shape

    avg = 0.0
    for i in range(0, rows):
        for j in range(0, cols):
            pixel = img[i,j]
            avg += float(pixel[0]+pixel[1]+pixel[2])/3.0

    avg = avg / float(rows*cols)
    if avg < 55:
        return '.'
    else:
        return '-'

ll = os.listdir('frames')
for f in ll:
    sys.stdout.write(process_img('frames/{}'.format(f)))
    sys.stdout.flush()
print
