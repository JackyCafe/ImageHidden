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
from MsaLib.embedded import Embedded
from MsaLib.image import Image
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

'''一張512*512 的影像 如果被切成4*4 的block 的話，會有128*128 個block
    每個block 塞一個key值，如果是key 值為0 的話，該block s1 需與s2 交換
'''


def generate_key(img: MsaImage, base_key: str) -> str:
    cols = img.W
    base_keys = []
    repeat_time = int(cols / img.cols)
    base_keys.append(base_key)
    return base_keys * repeat_time * repeat_time


if __name__ == '__main__':
    block_size = 4
    image = MsaImage("../images/didh_ambtc_s1_Baboon512.raw.bmp", block_size, block_size)
    locates = image.get_block_locate()
    key = "01011010"
    embedded_data = ""
    s1: Block
    s2: Block
    #embedded_data ，要隱藏的資料

    with open("embedded.csv", "r") as f:
        embedded_data = f.readlines()
    b1 = image.get_block(8)
    s2 = b1.clone()
    keys = generate_key(image, key)
    e1 = Embedded(b1, key)
    len = e1.st_table().sum() #要丟入的
    pos = e1.encode()
    print(pos)

    '''get one block by index
    for i, l in enumerate(locates):
        print(image.get_block(i).get_block_info())
        logging.info(image.get_block(i).get_block_info())
        '''

    '''get all block information'''
    # for block in image.storage_block():
    #     print(block.get_block_info(),block.avg())
