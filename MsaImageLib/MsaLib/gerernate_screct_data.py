'''
MsaImageLib/MsaLib
gerernate_screct_data.py
ImageHidden
Created by user at 2022/4/25
'''
import codecs

# def generate_data(bit_count):
#     binary_strings = []
#
#     def genbin(n, bs=''):
#         if len(bs) == n:
#             binary_strings.append(bs)
#         else:
#             genbin(n, bs + '1')
#             genbin(n, bs + '0')
#
#     genbin(bit_count)
#     return binary_strings
import random


def generate_data():
    binary_strings =[]
    for j in range(1):
        str = ''
        for i in range(4096):
            if random.randint(0, 100) % 2 == 0:
                str += '0'
            else:
                str += '1'
        binary_strings.append(str)
    return binary_strings

if __name__ == '__main__':
    str = generate_data()

    with codecs.open('../../script/embedded.csv', 'w', "utf-8") as f:
        for s in str:
            f.writelines(s)
