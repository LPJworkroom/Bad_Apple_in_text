import cv2 as cv
import os
import numpy
from pathlib import Path
from cv2.cv2 import VideoCapture


def run():
    captured: VideoCapture = cv.VideoCapture('bad_apple.mp4')
    success, image = captured.read()
    count = 0
    # print(image)
    while success:
        cv.imwrite('frame%d.jpg' % count, image)
        success, image = captured.read()
        count += 1


if __name__ == '__main__':
    run()
