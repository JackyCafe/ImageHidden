'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/12/2 下午9:44
# @Author : yhlin
# @Site : 
# @File : msaLib.py
# @Software: PyCharm
'''
import cv2
from MsaLib.block import Block
from MsaLib.point import Point


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

    def get_block_locate(self) -> list:
        self.locates = []
        for i in range(0, self.W, self.cols):
            for j in range(0, self.H, self.rows):
                p = Point(i, j)
                self.locates.append(p)
        return self.locates

    def get_block(self, index):
        x: int = self.locates[index].x
        y: int = self.locates[index].y
        block = [[0 for x in range(self.cols)] for y in range(self.rows)]
        for i in range(x, x + 4):
            for j in range(y, y + 4):
                # block = Block(self.image[i][j], i-x, j-y)
                block[i - x][j - y] = self.image[i][j]
        block_obj = Block(block, x, y)
        return block_obj

    def storage_block(self):
        self.blocks = []
        for i,l in enumerate(self.locates):
            block_obj = self.get_block(i)
            self.blocks.append(block_obj)
        return self.blocks




    # def get_block(self, index):
    #     x: int = self.locates[index].x
    #     y: int = self.locates[index].y
    #     block = [[0 for x in range(self.cols)] for y in range(self.rows)]
    #     for i in range(x, x + 4):
    #         for j in range(y, y + 4):
    #             block[i-x][j-y] = self.image[i][j]
    #     return block

    # def storage_block(self):
    #     self.locates = self.get_block_locate()
    #     for i, l in enumerate(self.locates):
    #         self.blocks.append(self.get_block(i))
    #     return self.blocks
