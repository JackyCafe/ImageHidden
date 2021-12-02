'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/12/2 下午9:42
# @Author : yhlin
# @Site : 
# @File : point.py
# @Software: PyCharm
'''

class Point:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + "," + str(self.y)