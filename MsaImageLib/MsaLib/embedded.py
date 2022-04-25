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

    def encode(self) -> int:
        st_table = self.st_table()
        return int(st_table.sum())

    def st_table(self) ->np.ndarray:
        table = self.block.to_np()
        avg = int(self.block.avg())
        min = int(self.block.min())
        x = self.block.to_np()
        y = x.copy()
        mask = x > avg
        mask1 = (x == min)
        y[mask] -= avg
        y[np.bitwise_not(mask)] -= min
        y[mask1] = 1
        table = np.ceil(np.array(np.log2(y)))
        table[mask] += 1
        print(table)
        # w = x.shape[0]
        # h = x.shape[1]
        # for i in range(w):
        #     for j in range(h):
        #         if x[i][j] > avg:
        #             x[i][j] = x[i][j] - floor(avg)
        #             table[i][j] = log2(x[i][j]) + 1
        #         elif x[i][j] == min:
        #             x[i][j] = 0
        #             table[i][j] = 1
        #         else:
        #             x[i][j] = x[i][j] - min
        #             table[i][j] = log2(x[i][j])
        return table

    def to_np(self):
        return np.array(self.block)
