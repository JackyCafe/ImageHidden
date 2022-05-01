from numpy import ndarray

from MsaLib import Block
from math import log2, floor, ceil
import numpy as np
from itertools import chain


class Embedded:
    block: Block
    key: str
    embedded_data: str

    def __init__(self, block: Block, key: str, data: str = " "):
        self.block = block
        self.key = key
        self.embedded_data = data

    def set_hidden_data(self, data):
        self.embedded_data = data

    '''編碼 
        該pixel >平均值的話就採用avg+藏的資料
        小於平均值就用min+藏的資料
    '''
    def encode(self) -> ndarray:
        st_table = self.st_table()
        source = self.block.block
        avg = int(self.block.avg())
        min = int(self.block.min())
        w = st_table.shape[0]
        h = st_table.shape[1]
        str = ""
        for i in range(w):
            for j in range(h):
                str = self.embedded_data[0:int(st_table[i][j])]
                if source[i][j] > avg:
                    source[i][j] = avg + int(str, 2)
                else:
                    if str == '':  str = '0'
                    source[i][j] = min + int(str, 2)
                self.embedded_data = self.embedded_data[int(st_table[i][j]):]
        return source

    def st_table(self) -> np.ndarray:
        table = self.block.to_np()
        avg = int(self.block.avg())
        min = int(self.block.min())
        x = self.block.to_np()
        y = x.copy()
        mask = x > avg
        mask1 = (x == min)
        y[mask] -= avg
        y[np.bitwise_not(mask)] -= min
        y[mask1] = 2

        table = np.ceil(np.array(np.log2(y)))
        table[mask] += 1

        return table

    def to_np(self):
        return np.array(self.block)
