# -*- coding:utf-8 -*-

"""
@author:Yuan
@file:ML_main.py
@time:2018/2/28 16:07
"""

'''
主函数
应用欧几里得距离
进行多标签分类

'''

import time
import ML_Euclid as ME


if __name__ == '__main__':
    start = time.clock()

    ME.getTrains2fit('select cid, totalword_nv4mw   from content_copy1',           # 修改参数
                     'update content_copy1 set labels = %s where cid = %s')  # 修改参数

    # ME.getTrains2fit('select cid, segcontent from content_test',  # 修改参数
    #                 'update content_test set labels = %s where cid = %s')  # 修改参数

    elapsed = (time.clock() - start)
    print('Time used:', elapsed)
