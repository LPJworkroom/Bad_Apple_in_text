import math
import os
import time
from pathlib import Path
from PIL import Image
from threading import Lock, Thread
import numpy as np


class Frame2Txt:
    black, white = '█', ' '
    LETTER_W_H_RATIO = 0.5  # in console char's width/height

    imageWidth, imageHeight = 0, 0
    row, column, cellHeight, cellWidth = 0, 0, 0, 0

    lock = Lock()  # mutex for count and image
    total = 0  # total of images
    count = 0
    image = ''
    outputArr = []  # array store processed image

    startTime = 0  # record when start

    def __init__(self, row=60):
        self.row = row
        with open('output.txt', 'w', encoding='utf8') as output:
            #  get total amount of images
            while os.path.isfile('frame%d.jpg' % self.total):
                self.total += 1
            self.total-=1
            print(self.total)
            self.outputArr = [''] * self.total

            self.image = self.readImage('frame0.jpg')
            image = self.image  # alias for self.image
            self.imageWidth, self.imageHeight = image.size
            self.cellHeight = int(math.ceil(self.imageHeight / row))
            self.cellWidth = int(self.cellHeight * self.LETTER_W_H_RATIO)
            self.column = int(math.ceil(self.imageWidth / self.cellWidth))

            print('%d*%d' % (self.imageHeight, self.imageWidth))
            print(self.column, self.cellHeight, self.cellWidth)
            output.write('row=%d\n' % row)
            self.count = 0
            self.startTime = time.time()
            self.processImageMono()

            # threadPool = [Thread(target=self.processImageConcurrent) for i in range(8)]
            # for th in threadPool:
            #     th.start()
            # self.processImageConcurrent()

            # finished process images,write from outputArr to file
            output.write(''.join(self.outputArr))
            print('finished')

    def processImage(self, imageArr, index):
        # process one image,write into outputArr
        output = []  # output string
        for i in range(self.row):
            for j in range(self.column):
                char = self.black if self.darker(row=i, col=j, image_arr=imageArr) \
                    else self.white
                output.append(char)
            output.append('\n')

        self.outputArr[index] = ''.join(output)
        print(str(index) + ' ok')
        print('%f secs,%f sec per image' % (
            (time.time() - self.startTime), (time.time() - self.startTime) / self.count))

    def processImageMono(self):
        while self.count<self.total:
            imageArr = np.array(self.image)
            index = self.count
            self.count += 1
            self.image = self.readImage('frame%d.jpg' % self.count)
            self.processImage(imageArr, index)

    def processImageConcurrent(self):
        while self.count<self.total:
            self.lock.acquire()  # ask for image and count
            imageArr = np.array(self.image)
            index = self.count
            self.count += 1
            self.image = self.readImage('frame%d.jpg' % self.count)
            self.lock.release()

            self.processImage(imageArr, index)

    # run on CPU
    def darker(self, row, col, image_arr):
        # target = cellWidth * cellHeight * 255 * 3 / 2
        target = 0
        colorSum = 0
        imageWidth, imageHeight = self.image.size
        for i in range(row * self.cellHeight, min(row * self.cellHeight + self.cellHeight, imageHeight)):
            for j in range(col * self.cellWidth, min(col * self.cellWidth + self.cellWidth, imageWidth)):
                try:
                    target += 255 * 3 / 2
                    colorSum += sum(image_arr[i][j])
                except Exception as e:
                    print(e)
                    print(i, j, self.cellWidth, self.cellHeight)
                    # exit(-1)
        return colorSum > target

    @staticmethod
    def readImage(path):
        try:
            print('path:' + path)
            image = Image.open(path)
            return image
        except Exception as e:
            print(e)
            return False


if __name__ == '__main__':
    f = Frame2Txt()
