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

import cv2

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
    base_keys = base_keys * repeat_time * repeat_time
    base_keys.append(base_key)
    return base_keys * repeat_time * repeat_time


if __name__ == '__main__':
    block_size = 4
    # image = MsaImage("../images/didh_ambtc_s1_Baboon512.raw.bmp", block_size, block_size)
    image = MsaImage("../images/didh_ambtc_s1_Alan512.raw.bmp", block_size, block_size)
    locates = image.get_block_locate()
    key = "0101101011000011"
    embedded_data = ""
    s1: Block
    s2: Block
    # embedded_data ，要隱藏的資料
    with open("embedded.csv", "r") as f:
        embedded_data = f.read()
    b1 = image.get_block(0)
    s2 = b1.clone()
    keys = generate_key(image, key)
    s1_blocks = []
    s2_blocks = []

    '''get one block by index'''
    for i, l in enumerate(locates):
        b1 = image.get_block(i)
        b2 = b1.clone()
        e1 = Embedded(b1, key)
        len = int(e1.st_table().sum())  # 要丟入的資料長度
        data = embedded_data[0:len]  # 要嵌入的資料量
        e1.set_hidden_data(data)
        source = e1.encode()  # 將e1嵌入b1
        b1 = Block(source, b1.x, b1.y) #嵌入資料
        s1 = b1.clone()
        s2 = b2.clone()
        '''如果key為1時將資料交換'''
        for k in keys[i]:
            for x in range(4):
                for y in range(4):
                    if int(k) == 1:
                        s1.block[x][y] = b2.block[x][y]
                        s2.block[x][y] = b1.block[x][y]
        s1_blocks.append(s1)
        s2_blocks.append(s2)

    '''重建測試'''

    s1_img = MsaImage.reconstruct_image(s1_blocks)
    s2_img = MsaImage.reconstruct_image(s2_blocks)
    psnr_s1 = image.PSNR(s1_img)
    psnr_s2 = image.PSNR(s2_img)
    logging.info("psnr:" + str(psnr_s1))
    logging.info("psnr:" + str(psnr_s2))

    cv2.imwrite("s1.png", s1_img)
    cv2.imwrite("s2.png", s1_img)

    cv2.waitKey(0)
