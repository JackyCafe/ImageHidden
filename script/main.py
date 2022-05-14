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
        logging.FileHandler("result.log"),
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


'''資料隱藏
'''
def data_hidden(file: str):
    block_size = 4
    file_name = Path(file).stem
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

    ''' '''
    for i, l in enumerate(locates):
        b1 = image.get_block(i)
        b2 = b1.clone()
        e1 = Embedded(b1) # 建立一個Embedded 物件，
        len = int(e1.st_table().sum())  # 讀取e1的stable來計算要丟入的資料長度
        data = embedded_data[0:len]  # 要嵌入的資料量
        embedded_datas+=data
        e1.set_hidden_data(data)
        source = e1.encode()  # 將e1嵌入b1
        b1 = Block(source, b1.x, b1.y)  # 嵌入資料
        s1 = b1.clone()
        s2 = b2.clone()
        '''如果key為1時將資料交換'''
        for x in range(0,4):
            for y in range(0,4):
                if keys[i][x*4+y]=="1":
                    s1.block[x][y] = b2.block[x][y]
                    s2.block[x][y] = source[x][y]
                elif keys[i][x*4+y]=="0":
                    s1.block[x][y] = source[x][y]
                    s2.block[x][y] = b2.block[x][y]
        b1_blocks.append(b1)
        s1_blocks.append(s1)
        s2_blocks.append(s2)

    with open('../embedded_data/' + file_name + ".csv", 'w') as f:
        f.write(embedded_datas)
    size = Path('../embedded_data/' + file_name + ".csv").stat().st_size
    size = int(size/1024)
    '''重建測試'''
    b1_img = MsaImage.reconstruct_image(b1_blocks)
    s1_img = MsaImage.reconstruct_image(s1_blocks)
    s2_img = MsaImage.reconstruct_image(s2_blocks)
    psnr_b1 = image.PSNR(b1_img)
    psnr_s1 = int(image.PSNR(s1_img))
    psnr_s2 = image.PSNR(s2_img)
    print(file_name + "s1 psnr:" + str(psnr_s1))
    print(file_name + "s2 psnr:" + str(psnr_s2))
    # logging.info(file_name + "b1 psnr:" + str(psnr_b1))
    logging.info(file_name +",psnr"+str(psnr_s1)+", size:"+str(size)+"kb" )
    # logging.info(file_name + "s2 psnr:" + str(psnr_s2))



    cv2.imwrite('../process_images/' + file_name + "_b1.png", b1_img)
    cv2.imwrite('../process_images/' + file_name + "_s1.png", s1_img)
    cv2.imwrite('../process_images/' + file_name + "_s2.png", s1_img)


if __name__ == '__main__':
    path = listdir('../images/')
    for f in path:
        file = join('../images/', f)
        data_hidden(file=file)

    print("done")