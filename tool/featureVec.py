# -*- coding:utf-8 -*-

"""
@author:Yuan
@file:featureVec.py
@time:2018/1/26 10:43
"""
import time
import numpy as np
import pymysql
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
import math
import readwrite as rw
from sklearn.datasets.base import Bunch
'''
特征向量
'''


# 获得要构建向量的list
# 返回结果为 记录数量， 记录唯一标识， 记录文本
def getdataset(sqlstr):

    conlist = []
    cidlist = []
    ms = pymysql.connect(host='localhost', user='root', passwd='123456', db='shequkaifa', charset='utf8')
    cur = ms.cursor()

    count = cur.execute(sqlstr)

    for i in range(count):
        res = cur.fetchone()  # 获得列表
        if len(res) == 2:
            cidlist.append(res[0])
            conlist.append(res[1])  # 选取列多时，可改以拼接
        elif len(res) == 3:
            cidlist.append(res[0])
            conlist.append(res[1] + res[2])  # 选取列多时，可改以拼接
        # print(res[1])
        # print(res[2])
        # print(set(res[1]+res[2]))

    return count, cidlist, conlist


def getdataset2(sqlstr):

    conlist = []
    cidlist = []
    caglist = []
    ms = pymysql.connect(host='localhost', user='root', passwd='123456', db='shequkaifa', charset='utf8')
    cur = ms.cursor()

    count = cur.execute(sqlstr)


    for i in range(count):
        res = cur.fetchone()  # 获得列表
        if len(res) == 2:
            cidlist.append(res[0])
            conlist.append(res[1])  # 选取列多时，可改以拼接

        elif len(res) == 3:
            cidlist.append(res[0])
            conlist.append(res[1])  # 选取列多时，可改以拼接
            caglist.append(res[2])
        elif len(res) == 1:
            conlist.append(res[0])



    return count, cidlist, conlist, caglist


# 获得tfidf矩阵（所有文章的特征向量构成的矩阵）训练集
def gettfidfMeri(clist):

    stpwrdlst = rw._readfile('../data/hlt_stop_words.txt').splitlines()

    vectorizer = CountVectorizer(stop_words=stpwrdlst)  # 维度从59293降到59012
    X = vectorizer.fit_transform(clist)
    word = vectorizer.get_feature_names()
    print(word)

    transformer = TfidfTransformer()
    # 将词频矩阵X统计成TF-IDF值
    tfidf = transformer.fit_transform(X)
    print(len(tfidf.toarray()[0]))
    print(tfidf)

    # 数据结构 tfidf[i][j]表示i类文本中的tf-idf权重
    return tfidf.toarray()



# date 2018/3/22
# 构建类别向量空间
def catspace(catlist):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(catlist)

    print(vectorizer.vocabulary_)
    return X.toarray(), vectorizer.vocabulary_


# 获得tfidf词向量空间
def gettfidfMeriVoc(clist):

    stpwrdlst = rw._readfile('../data/hlt_stop_words2.txt').splitlines()

    vectorizer = CountVectorizer(stop_words=stpwrdlst)  # 维度从59293降到59012
    X = vectorizer.fit_transform(clist)
    # word = vectorizer.get_feature_names()
    # print(word)

    transformer = TfidfTransformer()
    # 将词频矩阵X统计成TF-IDF值！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！可将重组句子中的重要词重复出现，以提高词频
    tfidf = transformer.fit_transform(X)
    tfidfspace = Bunch(tdm=[], vocabulary={})
    tfidfspace.tdm = tfidf
    tfidfspace.vocabulary = vectorizer.vocabulary_
    weidu = len(tfidfspace.vocabulary)
    print(weidu)

    # 数据结构 tfidf[i][j]表示i类文本中的tf-idf权重
    return tfidfspace, tfidf.toarray(), weidu


# 获得tfidf词向量空间
def gettfidfMeriVoc1(clist):

    stpwrdlst = rw._readfile('../data/hlt_stop_words.txt').splitlines()

    vectorizer = CountVectorizer(stop_words=stpwrdlst)  # 维度从59293降到59012
    X = vectorizer.fit_transform(clist)
    # word = vectorizer.get_feature_names()
    # print(word)

    transformer = TfidfTransformer()
    # 将词频矩阵X统计成TF-IDF值！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！可将重组句子中的重要词重复出现，以提高词频
    tfidf = transformer.fit_transform(X)
    tfidfspace = Bunch(tdm=[], vocabulary={})
    tfidfspace.tdm = tfidf
    tfidfspace.vocabulary = vectorizer.vocabulary_
    weidu = len(tfidfspace.vocabulary)
    print(weidu)


    # 数据结构 tfidf[i][j]表示i类文本中的tf-idf权重
    return tfidfspace, tfidf.toarray(), weidu






# 获得tfidf矩阵（所有文章的特征向量构成的矩阵）应用集
# 使应用集应用训练集的词向量空间
def gettfidfMerisoft(clist, tfidfspace):

    stpwrdlst = rw._readfile('../data/hlt_stop_words2.txt').splitlines()

    vectorizer = CountVectorizer(stop_words=stpwrdlst, vocabulary=tfidfspace.vocabulary)  # 维度从59293降到59012
    X = vectorizer.fit_transform(clist)
    word = vectorizer.get_feature_names()
    # for w in word:
    #     print(w)
    print(word)

    transformer = TfidfTransformer()
    # 将词频矩阵X统计成TF-IDF值
    tfidf = transformer.fit_transform(X)
    # print(len(tfidf.toarray()[0]))

    # 数据结构 tfidf[i][j]表示i类文本中的tf-idf权重
    return tfidf.toarray()

def gettfidfMerisoft1(clist, tfidfspace):

    stpwrdlst = rw._readfile('../data/hlt_stop_words.txt').splitlines()

    vectorizer = CountVectorizer(stop_words=stpwrdlst, vocabulary=tfidfspace.vocabulary)  # 维度从59293降到59012
    X = vectorizer.fit_transform(clist)
    word = vectorizer.get_feature_names()
    # for w in word:
    #     print(w)
    # print(word)

    transformer = TfidfTransformer()
    # 将词频矩阵X统计成TF-IDF值
    tfidf = transformer.fit_transform(X)
    print('应用集词向量矩阵：')
    print(tfidf.toarray())
    rw._writebunchobj('../data/应用集词向量矩阵', tfidf.toarray())
    # print(len(tfidf.toarray()[0]))

    # 数据结构 tfidf[i][j]表示i类文本中的tf-idf权重
    return tfidf.toarray()




# 每个cid对应的文章转换成其对应的特征向量并保存其特征向量长度
# 文章数， 文章唯一标识， 文章内容
def cidperVec(count, cidlist, conlist):
    # 所有文章的词向量矩阵
    tfidfresult = gettfidfMeri(conlist)

    # 字典中存放cid及其对应的文章特征向量及其向量的长度
    condict = {}
    for i in range(count):
        len = math.sqrt(sum(tfidfresult[i] ** 2))
        if len != 0:
            condict[cidlist[i]] = [tfidfresult[i], len, conlist[i]]

    return condict

# 每个cid对应的文章转换成其对应的特征向量并保存其特征向量长度
# 文章数， 文章唯一标识， 所有文章的词向量矩阵
def cidperVector(count, cidlist, conlist, tfidfresult):
    # 字典中存放cid及其对应的文章特征向量及其向量的长度
    condict = {}
    for i in range(count):
        len = math.sqrt(sum(tfidfresult[i] ** 2))
        if len != 0:
            condict[cidlist[i]] = [tfidfresult[i], len, conlist[i]]

    return condict


# 计算两个向量的相关性
def similarity(v1, v2, len1, len2):
    # if len1 == 0 or len2 == 0:
    #     return
    sl = sum(v1 * v2)
    mul = len1*len2
    res = sl/mul
    return res


# 目标：获得n个向量的相关性
# 向量个数为count
# 每个向量的唯一标识为cidlist
# 每个向量的内容为conlist
def writesimilaritem(count, cidlist, conlist):

    condict = cidperVec(count, cidlist, conlist)

    # 字典中存放两个cid的相关性
    sldict = {}
    for i in range(count):
        for j in range(i + 1, count):
            if condict[cidlist[i]][1] == 0 or condict[cidlist[j]][1] == 0:
                continue
            sldict[(cidlist[i], cidlist[j])] = similarity(condict[cidlist[i]][0], condict[cidlist[j]][0],
                                                          condict[cidlist[i]][1], condict[cidlist[j]][1])

    # 该字典中存储相关性第一次比较后，同一个句子，和他之后的所有句子中相关性最大的一条
    # Out：{(2, 4): 0.098250146180823714, (4, 63): 0.69217719371623188, (7, 61): 0.11392964410825167,...}
    dict1 = {}
    for i in range(count):
        max = 0
        anotherdot = 0

        for k, v in sldict.items():
            if k[0] == cidlist[i]:
                if v > max:
                    max = v
                    anotherdot = k[1]
        dict1[(cidlist[i], anotherdot)] = max   # 长度为count


    # 去0
    new_dict1 = {}
    for k, v in dict1.items():
        if k[1] != 0:
            new_dict1[k] = v

    # 对于如下项，保留相关性大的一个：
    #     （2,4）（4,63）
    for i in range(1, count):
        k1 = ()
        k2 = ()
        for k, v in new_dict1.items():
            if k[1] == cidlist[i]:
                k1 = k
            if k[0] == cidlist[i]:
                k2 = k
        if k1 == () or k2 == ():
            continue
        if new_dict1[k1] > new_dict1[k2]:
            new_dict1.pop(k2)
        else:
            new_dict1.pop(k1)

    rw._writebunchobj('../data/dict1data', new_dict1)



