'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/12/2 下午10:08
# @Author : yhlin
# @Site : 
# @File : block.py
# @Software: PyCharm
'''
import numpy as np


class Block:
    x: int
    y: int
    data = {}

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
        return Block(self.block.copy(),self.x,self.y)

    # block encode
    def encode(self):
        print(self.to_np())
        # for i in range(self[0]):
        #     for j in range(self[1]):
        #         print(self[i][j])

    def decode(self):
        ...

    def to_np(self):
        return np.array(self)

    def __str__(self):
        return f"x:{self.x}, y:{self.y}, block:{self.block} "
