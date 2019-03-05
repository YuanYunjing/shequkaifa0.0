# -*- coding:utf-8 -*-

"""
@author:Yuan
@file:SA_main.py
@time:2018/3/29 15:47
"""
'''
主函数
进行情感分析
'''



import time
import code2
import classifier

if __name__ == '__main__':
    start = time.clock()

    resultsql = 'update content_copy1 set score = %s where cid = %s'

    # 基于词典进行句子评分
    code2.getScore("select cid, totalword_nv4mw from content_copy1 where labels != ''", resultsql)

    # 基于分类器对评分为0的句子进行情感分类
    classifier.addClassifier('select cid, totalword_nv4mw from content_copy1 where score = 0', resultsql)

    elapsed = (time.clock() - start)
    print('Time used:', elapsed)

