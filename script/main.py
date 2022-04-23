'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/12/2 下午9:59
# @Author : yhlin
# @Site : 
# @File : main.py
# @Software: PyCharm
'''
import sys

from MsaLib import Block
from MsaLib.msaLib import MsaImage
import logging
import json

from MsaLib.numpy_encoder import NumpyEncoder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("lena5.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


if __name__ == '__main__':
    image = MsaImage("../images/didh_ambtc_s1_Baboon512.raw.bmp", 4, 4)

    locates = image.get_block_locate()

    # block = image.get_block(1)
    # s1 = block.get_block_info()
    # s2 = block.get_block_info()
    s1: Block
    s2: Block
    s1 = image.get_block(8)
    s2 = s1.clone()
    s1.encode()




    '''get one block by index
    for i, l in enumerate(locates):
        print(image.get_block(i).get_block_info())
        logging.info(image.get_block(i).get_block_info())
        '''

    '''get all block information'''
    # for block in image.storage_block():
    #     print(block.get_block_info(),block.avg())


