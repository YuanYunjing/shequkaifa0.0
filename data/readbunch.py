# -*- coding:utf-8 -*-

"""
@author:Yuan
@file:readbunch.py
@time:2018/4/22 21:05
"""

import sys
sys.path.append('../tool/')
import readwrite as rw

r1 = rw._readbunchobj('../data/训练集标签列表')
r2 = rw._readbunchobj('../data/训练集词向量矩阵')
r3 = rw._readbunchobj('../data/应用集词向量矩阵')

print(r1)
print(r2)
print(r3)

