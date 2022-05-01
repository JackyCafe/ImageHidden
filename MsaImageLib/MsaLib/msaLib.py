'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/12/2 下午9:44
# @Author : yhlin
# @Site : 
# @File : msaLib.py
# @Software: PyCharm
'''
import math

import cv2

from MsaLib.block import Block
from MsaLib.image import Image
from MsaLib.point import Point
import json
import numpy as np


class MsaImage:
    W: int
    H: int
    locates = []
    blocks = [tuple]
    cols: int
    rows: int

    def __init__(self, filename, x: int, y: int):
        self.image = cv2.imread(filename)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

        self.W = self.image.shape[0]
        self.H = self.image.shape[1]
        self.cols = x
        self.rows = y

    '''
    將一張影像依x,y大小分割成小的block,
    並把位置記錄在p的物件，位置從(0,0),(0,4)...開始
    存放在locates 的list 
    '''

    def get_block_locate(self) -> list:
        self.locates = []
        for i in range(0, self.W, self.cols):
            for j in range(0, self.H, self.rows):
                p = Point(i, j)
                self.locates.append(p)
        return self.locates

    '''丟入第幾個index,會去locates中找出其x,y
    '''

    def get_block(self, index) -> Block:
        x: int = self.locates[index].x
        y: int = self.locates[index].y
        # 宣告block 大小
        block = [[0 for x in range(self.cols)] for y in range(self.rows)]
        for i in range(x, x + self.cols):
            for j in range(y, y + self.rows):
                # block = Block(self.image[i][j], i-x, j-y)
                block[i - x][j - y] = self.image[i][j]
        block_obj = Block(block, x, y)
        return block_obj

    '''重建影像'''

    @classmethod
    def reconstruct_image(cls, blocks, cols=512, rows=512, w=4, h=4) -> Image:
        dst: Image
        dst = np.zeros([rows,cols],dtype=int)
        for block in blocks:
            x = block.get_block_info()['X']
            y = block.get_block_info()['Y']
            for i in range(w):
                for j in range(h):
                    dst[x+i][y+j] =block.block[i][j]
        return dst
         # for x in cols:
        #     for y in rows :
        #         dst[x][y] = blocks

        #
        # for i,l in enumerate(blocks):
        #     print(i)

    '''計算2影像的ＰＳＮＲ'''

    def PSNR(self, dest: Image) -> float:
        sousum: float
        M: int
        N: int
        M = self.image.shape[0]
        N = self.image.shape[1]
        sum = 0
        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):
                sum += (self.image[i][j] / 255 - dest[i][j] / 255) ** 2
        rmse = math.sqrt(sum / (M * N))
        if rmse < 1.0e-10:
            rmse = 1
        psnr = 20 * math.log10(1 / rmse)
        return psnr
