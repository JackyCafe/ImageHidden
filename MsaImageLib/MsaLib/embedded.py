from numpy import ndarray

from MsaLib import Block, Point
from math import log2, floor, ceil
import numpy as np
from itertools import chain


class Embedded:
    block: Block
    key: str
    embedded_data: str
    '''以一個block 來處理，來源處丟入一個NXN 的block 
    '''

    def __init__(self, block: Block, data: str = " "):
        self.block = block
        # self.key = key
        self.embedded_data = data
        self.uniform_st_table = [['1000', '0010', '0100', '1000']
            , ['0110', '0001', '1100', '1010']
            , ['1101', '1101', '1111', '1001']
            , ['0001', '0101', '0110', '1111']]

    def set_hidden_data(self, data):
        self.embedded_data = data

    '''編碼 
        
    '''

    def encode(self):
        if not self.block.is_the_same_pixel():
            return self.normal_encode()
        else:
            return self.uniform_encode()

    '''
        區塊都一樣的編碼
    '''

    def uniform_encode(self):
        d_st_table = [[0, 1, 2, 0], [3, 0, 4, 2], [5, 6, 7, 4], [0, 5, 6, 7]]
        # d_st_table =[[0,1],[1,0]]
        self.block.block = self.block.block + d_st_table

        return self.block.block

    def uniform_encode_data(self):
        for s1 in self.uniform_st_table:
            for s in s1:
                self.embedded_data += s
        return self.embedded_data

    '''
        該pixel >平均值的話就採用avg+藏的資料
        小於平均值就用min+藏的資料
    '''

    def normal_encode(self) -> ndarray:
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

    '''st_table 找出block 中的平均值，與最小值。
       如果Pixel 值大於平均值 Pixel - average 後取log2 +1 計算藏的bit
       如果Pixel 值小於平均值 Pixel - min 後取log2 計算藏的bit  
       如果Pixel 等於平均值 藏2 個bit
    '''

    def st_table(self) -> np.ndarray:
        avg = int(self.block.avg())
        min = int(self.block.min())
        x = self.block.to_np()
        y = x.copy()
        mask = x > avg  # 找出array中>平均值的 index
        mask1 = (x == min)
        y[mask] -= avg
        y[np.bitwise_not(mask)] -= min
        y[mask1] = 4
        table = np.ceil(np.array(np.log2(y)))  # 無條件進入
        table[mask] += 1  # 大於平均值的多藏一碼
        return table

    def to_np(self):
        return np.array(self.block)
