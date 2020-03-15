import os
import sys
import threading
from pathlib import Path
from time import sleep, time


def outputAll():
    f = open('output.txt', 'r', encoding='utf8')
    row = int(f.readline().replace('row=', '').rstrip())
    print(row)

    frame = ''
    frames = []
    for i, line in enumerate(f):
        if i % row == 0 and i != 0:  # new frame
            frames.append(frame)
            frame = ''
        else:
            frame += line
    f.close()

    nowFrame = iter(frames)
    timer = threading.Timer(1 / 30, printFrame, [nowFrame])
    timer.start()


def printFrame(frameIter):
    begTime = time()
    count, aborted, internalSum = 0, 0, 0
    frameRate = 30
    while True:
        try:
            now = time()
            passed = now - begTime
            targetTime = count / frameRate
            if targetTime < passed:  # too slow
                count += 1
                aborted += 1
                next(frameIter)
                print('aborted')
                continue
            print(next(frameIter), end='')
            count += 1
            internal = time() - now
            internalSum+=internal
            # instead of sleep stable time,count time passed and calculate right time
            if 1 / frameRate < internal:  # print too slow,sleep no time
                continue
            sleep(max(1 / frameRate - internal, 0.0))
        except StopIteration:
            print('print all frame ok')
            print('total %d frames,%d aborted,%f average print time' % (count, aborted, internalSum/count))
            break
        except Exception as e:
            print(e)


if __name__ == '__main__':
    outputAll()
