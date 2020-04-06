import cv2
import numpy as np
import math
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--image', required=True, help='path of the image to analyse')
parser.add_argument('-o','--output', default='.', help='output directory of the analysis')
parser.add_argument('-hs','--hstep', type=int, default=50, help='step for the H component')
parser.add_argument('-ss','--sstep', type=int, default=50, help='step for the S component')
parser.add_argument('-vs','--vstep', type=int, default=50, help='step for the V component')
args = parser.parse_args()

os.makedirs(args.output)

img = cv2.imread(args.image)
frame = np.copy(img)
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

for h in range(0, 255, args.hstep):
    for s in range(0, 255, args.sstep):
        for v in range(0, 255, args.vstep):
            mask = cv2.inRange(hsv, (h, s, v), (h+args.hstep, s+args.sstep, v+args.vstep))
            x,y = mask.shape
            if len(np.nonzero(mask.reshape((x*y)))[0]) > 2500:
                zone = cv2.bitwise_and(frame, frame, mask=mask)
                combo = cv2.addWeighted(frame, 0.3, zone, 0.7, 0)
            
                cv2.imwrite(args.output + '/' + str(h) + '_' + str(s) + '_' + str(v) + '_' + args.image, combo)
