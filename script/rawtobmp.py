'''
script
rawtobmp.py
ImageHidden
Created by user at 2022/5/14
'''
from os import listdir
from os.path import join
from pathlib import Path

import cv2
import numpy as np
import rawpy

rows = 512
cols = 512


def raw2bmp(file):
    file_name = Path(file).stem
    try:
        fd = open(file, 'rb')
        f = np.fromfile(fd, dtype=np.uint8, count=rows * cols)
        im = f.reshape((rows, cols))  # notice row, column format
        cv2.imwrite('../orginal/' + file_name + '.bmp', im)
    except Exception as e:
        print(file)




if __name__ == '__main__':
    path = listdir('../raw/')
    # raw2bmp('../raw/Alan512.raw')
    for f in path:
        file = join('../raw/', f)
        raw2bmp(file)