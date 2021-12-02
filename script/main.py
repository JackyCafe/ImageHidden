'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/12/2 下午9:59
# @Author : yhlin
# @Site : 
# @File : main.py
# @Software: PyCharm
'''
from MsaLib.msaLib import MsaImage

if __name__ == '__main__':
    image = MsaImage("../images/lena5.jpg", 4, 4)
    locates = image.get_block_locate()

    '''get one block by index'''
    # for i, l in enumerate(locates):
    #     print(i, image.get_block(i).get_block_info())

    '''get all block information'''
    for block in image.storage_block():
        print(block.get_block_info(),block.avg())


