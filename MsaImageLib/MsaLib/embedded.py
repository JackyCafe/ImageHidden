from MsaLib import Block
from math import log2, floor
import numpy as np


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

    def encode(self):
        st_table = self.st_table()
        print(st_table)

    def st_table(self):
        table = self.block.block
        avg = self.block.avg()
        min = self.block.min()
        print(str(avg) + "," + str(min))

        x = self.block.to_np()
        w = x.shape[0]
        h = x.shape[1]
        for i in range(w):
            for j in range(h):
                if x[i][j] > avg:
                    x[i][j] = x[i][j] - floor(avg)
                    table[i][j] = log2(x[i][j]) + 1
                elif x[i][j] == min:
                    x[i][j] = 0
                    table[i][j] = 1
                else:
                    x[i][j] = x[i][j] - min
                    table[i][j] = log2(x[i][j])
        return table

    def to_np(self):
        return np.array(self.block)
