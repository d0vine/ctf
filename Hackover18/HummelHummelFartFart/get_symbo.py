#!/usr/bin/env python
import sys
import cv2

img = cv2.imread(sys.argv[1])
rows, cols, _ = img.shape

avg = 0.0
for i in range(0, rows):
    for j in range(0, cols):
        pixel = img[i,j]
        avg += float(pixel[0]+pixel[1]+pixel[2])/3.0

avg = avg / float(rows*cols)
if avg < 55:
    sys.stdout.write('-')
else:
    sys.stdout.write('.')
# print 'avg: {}'.format(avg)
