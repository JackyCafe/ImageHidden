'''
MsaImageLib/MsaLib
gerernate_screct_data.py
ImageHidden
Created by user at 2022/4/25
'''
import codecs



def generate_data(bit_count):
    binary_strings = []

    def genbin(n, bs=''):
        if len(bs) == n:
            binary_strings.append(bs)
        else:
            genbin(n, bs + '1')
            genbin(n, bs + '0')

    genbin(bit_count)
    return binary_strings


if __name__ == '__main__':
    str = generate_data(16)

    with codecs.open('../../script/embedded.csv', 'w', "utf-8") as f:
        for s in str:
            f.writelines(s)
