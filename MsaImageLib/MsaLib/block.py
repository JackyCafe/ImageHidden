'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/12/2 下午10:08
# @Author : yhlin
# @Site : 
# @File : block.py
# @Software: PyCharm
'''
import math
import string

import numpy as np
from numpy import log2


class Block:
    x: int
    y: int
    data = {}
    key = "0"  #

    # average: float

    # def __init__(self, block: list[list[int]], x: int, y: int) -> None:
    def __init__(self, block: list[list[int]], x: int, y: int) -> None:
        self.block = np.array(block)
        self.x = x
        self.y = y

    def get_block_info(self) -> tuple:
        self.data['X'] = self.x
        self.data['Y'] = self.y
        self.data['data'] = self.block
        self.data['block_avg'] = self.block.mean()
        self.data['block_min'] = self.block.min()

        return self.data

    def avg(self) -> float:
        return self.block.mean()

    def min(self) -> float:
        return self.block.min()

    # 複製一份區塊
    def clone(self) -> float:
        return Block(self.block.copy(), self.x, self.y)

    # block encode
    # def encode(self, key: str = " "):
    #     st_table = self.st_table()

    # def st_table(self):
    #     st_table = self.block
    #     x = self.to_np()
    #     w = x.shape[0]
    #     h = x.shape[1]
    #     for i in range(w):
    #         for j in range(h):
    #             if x[i][j] > math.floor(self.avg()):
    #                 x[i][j] = x[i][j] - self.avg()
    #             else:
    #                 x[i][j] = x[i][j] - self.min()
    #             if x[i][j] == 0:
    #                 st_table[i][j] = 0
    #             else:
    #                 st_table[i][j] = log2(x[i][j])
    #     return st_table

    def decode(self):
        ...

    def to_np(self):
        return np.array(self.block)

    def __str__(self):
        return f"x:{self.x}, y:{self.y}, block:{self.block} "
