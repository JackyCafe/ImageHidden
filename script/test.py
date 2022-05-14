'''
MsaImageLib/MsaLib
test.py
ImageHidden
Created by user at 2022/5/14
'''
from os import path, listdir
from os.path import join

from MsaLib import MsaImage

block_size = 4


def test(file = None):

    image_obj = MsaImage(file, block_size, block_size)
    locates = image_obj.get_block_locate()
    count = 0
    for i, l in enumerate(locates):
        b1 = image_obj.get_block(i)
        if b1.is_the_same_pixel():
            count += 1

    print(file+','+str(count))


def test1(file):
    image_obj = MsaImage(file, block_size, block_size)
    locates = image_obj.get_block_locate()
    b1 = image_obj.get_block(7)
    print(b1)
    print(b1.is_the_same_pixel())


if __name__ == '__main__':
    # test1('../orginal/Lena512.bmp')
    test('../orginal/Lena512.bmp')
    # path = listdir('../orginal/')
    #
    # for f in path:
    #     file = join('../orginal/', f)
    #     test(file)
