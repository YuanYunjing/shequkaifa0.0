# -*- coding:utf-8 -*-

"""
@author:Yuan
@file:classifier.py
@time:2018/3/24 16:18
"""

import sys
sys.path.append('../tool/')
import featureVec as fv
from sklearn.naive_bayes import MultinomialNB
import pymysql


def writecag2mysql(sqlstr, val):
    ms = pymysql.connect(host='localhost', user='root', passwd='123456', db='shequkaifa', charset='utf8')
    cur = ms.cursor()

    count = cur.execute(sqlstr, val)
    ms.commit()
    cur.close()
    ms.close()
    return count


def addClassifier(datasql, resultsql):

    # 训练集 词向量空间、词向量矩阵
    result = fv.getdataset2('select cid, oldsegcontent, sentimentscore from content_category')
    counttrain = result[0]
    conlisttrain = result[2]  # 文本列表
    caglist = result[3]  # 类别列表
    tfidfmeritrain = fv.gettfidfMeriVoc(conlisttrain)  # 获得tfidf词向量空间
    tspace = tfidfmeritrain[0]  # 训练集词向量空间
    trainmeri = tfidfmeritrain[1]  # 向量矩阵
    axis = tfidfmeritrain[2]

    # 应用集 词向量空间中的词向量矩阵
    result1 = fv.getdataset2(datasql)
    count = result1[0]
    cidlist = result1[1]
    conlist = result1[2]
    # 数据结构 tfidf[i][j]表示i类文本中的tf-idf权重
    if count != 0:
        tfidfmerisoft = fv.gettfidfMerisoft(conlist, tspace)

        classier = MultinomialNB(alpha=0.001).fit(trainmeri, caglist)
        cat = classier.predict(tfidfmerisoft)
        print(cat)
        resultdict = {}
        for i in range(len(cat)):
            resultdict[cidlist[i]] = cat[i]
        print(resultdict)

        for k, v in resultdict.items():
            writecag2mysql(resultsql, (v, k))


