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
from os import listdir
from os.path import join

import cv2

from MsaLib import Block
from MsaLib.embedded import Embedded
from MsaLib.image import Image
from MsaLib.msaLib import MsaImage
import logging
import json

from MsaLib.numpy_encoder import NumpyEncoder
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    # format="%(asctime)s [%(levelname)s] %(message)s",
    format="",
    handlers=[
        logging.FileHandler("../result/orginal_4.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

'''一張512*512 的影像 如果被切成4*4 的block 的話，會有128*128 個block
    每個block 塞一個key值，如果是key 值為1 的話，該block s1 需與s2 交換
'''


def generate_key(img: MsaImage, base_key: str) -> str:
    cols = img.W
    base_keys = []
    embedded_datas = ""
    repeat_time = int(cols / img.cols)
    base_keys = base_keys * repeat_time * repeat_time
    base_keys.append(base_key)
    return base_keys * repeat_time * repeat_time


'''資料隱藏主要程式
'''


def data_hidden(file: str, block_size=4):
    block_size = block_size
    file_name = Path(file).stem
    #將image 依block 拆成block X block
    image = MsaImage(file, block_size, block_size)
    locates = image.get_block_locate()
    key = "1001011010100101"
    embedded_datas = ""
    s1: Block
    s2: Block
    # embedded_data ，要隱藏的資料
    with open("embedded.csv", "r") as f:
        embedded_data = f.read()
    keys = generate_key(image, key)
    '''建立一個blocks 來依序存放所有的block 
    '''
    b1_blocks = []
    s1_blocks = []
    s2_blocks = []
    c1 = 0
    c2 = 0
    ''' '''
    for i, l in enumerate(locates):

        b1 = image.get_block(i)  # get_block 返回一個block物件
        b2 = b1.clone()
        e1 = Embedded(b1)  # 建立一個Embedded 物件，
        len = int(e1.st_table().sum())  # 讀取e1的stable來計算要丟入的資料長度

        if not b1.is_the_same_pixel():
            data = embedded_data[0:len]  # 要嵌入的資料量
            c1 += 1
        else:
            data = e1.uniform_encode_data()
            c2 += 1

        embedded_datas += data
        e1.set_hidden_data(data)
        source = e1.encode()  # 將e1嵌入b1

        '''todo 
        test uniform block'''
        b1 = Block(source, b1.x, b1.y)  # 嵌入資料
        s1 = b1.clone()
        s2 = b2.clone()
        # 如果key為1時將資料交換
        for x in range(0, block_size):
            for y in range(0, block_size):
                if keys[i][x * block_size + y] == "1":
                    s1.block[x][y] = b2.block[x][y]
                    s2.block[x][y] = source[x][y]
                elif keys[i][x * block_size + y] == "0":
                    s1.block[x][y] = source[x][y]
                    s2.block[x][y] = b2.block[x][y]
        b1_blocks.append(b1)
        s1_blocks.append(s1)
        s2_blocks.append(s2)

    print(f"block 中 pixel 畫素不同 {c1}")
    print(f"block 中 pixel 畫素相同 {c2}")
    with open('../embedded_data/' + file_name + ".csv", 'w') as f:
        f.write(embedded_datas)
    size = Path('../embedded_data/' + file_name + ".csv").stat().st_size
    size = int(size) * 8
    # 重建測試
    b1_img = MsaImage.reconstruct_image(b1_blocks, w=block_size, h=block_size)
    s1_img = MsaImage.reconstruct_image(s1_blocks, w=block_size, h=block_size)
    s2_img = MsaImage.reconstruct_image(s2_blocks, w=block_size, h=block_size)
    psnr_b1 = image.PSNR(b1_img)
    psnr_s1 = int(image.PSNR(s1_img))
    psnr_s2 = image.PSNR(s2_img)
    print(file_name + "s1 psnr:" + str(psnr_s1))
    print(file_name + "s2 psnr:" + str(psnr_s2))
    # logging.info(file_name + "b1 psnr:" + str(psnr_b1))
    logging.info(
        file_name + "," + str(psnr_s1) + "," + str(psnr_s2) + "," + str(size))
    # logging.info(file_name + "s2 psnr:" + str(psnr_s2))

    cv2.imwrite('../process_images/' + file_name + "_b1.png", b1_img)
    cv2.imwrite('../process_images/' + file_name + "_s1.png", s1_img)
    cv2.imwrite('../process_images/' + file_name + "_s2.png", s1_img)


if __name__ == '__main__':
    is_test = False

    if is_test:
        file = '../orginal/lena.bmp'
        data_hidden(file, block_size=2)
    else:
        path = listdir('../orginal/')
        logging.info(
            "file_name, psnr_s1,psnr_s2,embedded size(bits)")
        for f in path:
            file = join('../orginal/', f)
            data_hidden(file=file,block_size=4)

    print("done")
