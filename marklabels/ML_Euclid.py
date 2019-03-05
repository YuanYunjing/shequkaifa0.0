# -*- coding:utf-8 -*-

"""
@author:Yuan
@file:ML_Euclid.py
@time:2018/2/28 13:41
"""

'''
欧几里得距离
得到
多标签

'''
import sys
sys.path.append('../tool/')
from numpy import *
import pymysql
import featureVec as fv
import readwrite as rw


def dict2list(dic):
    ''' 将字典转化为列表 '''
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst


def writecag2mysql(sqlstr, val):
    ms = pymysql.connect(host='localhost', user='root', passwd='123456', db='shequkaifa', charset='utf8')
    cur = ms.cursor()

    count = cur.execute(sqlstr, val)
    ms.commit()
    cur.close()
    ms.close()
    return count


# 得到标签及其对应训练样本集字典
# axis: [-1, axis]
def labelset(dataSet, labels, count, axis):
    ls = {}
    for i in range(count):
        label = labels[i].replace('  ', '')
        if label in ls.keys():
            ls[label] = append(ls[label], dataSet[i])
        else:
            ls[label] = array([dataSet[i]])

    # 对数组进行整形
    for k, v in ls.items():
        ls[k] = ls[k].reshape((-1, axis))

    return ls


# 多标签分类
# 参数： newInput：带训练文本的特征向量（一条文本） ls:标签及其对应训练样本集字典 d：用来区分该文本是否隶属某个类的阈值
# 返回值： 该文本的所有可能标签（已完成标签排序）
def mlknn(newInput, ls, d):
    labellist = []
    len = math.sqrt(sum(newInput ** 2))
    if len == 0:
        return ''
    mindist = {}
    for label, dataSet in ls.items():
        numSamples = dataSet.shape[0]

        # 计算欧式距离
        diff = tile(newInput, (numSamples, 1)) - dataSet  # Subtract element-wise
        squaredDiff = diff ** 2  # squared for the subtract
        squaredDist = sum(squaredDiff, axis=1)  # sum is performed by row
        distance = squaredDist ** 0.5
        # print(distance)

        # 得到待测文本与该标签下最近的一个文本的距离
        mindistance = distance[argmin(distance)]
        mindist[label] = mindistance

    # 通过阈值d留下可能性较大的一个或几个label(也可能没有label留下)
    reallabel = {}
    for k, v in mindist.items():
        if v < d:
            reallabel[k] = v

    # 对留下的几个label排序，距离近的在前，远的在后
    list_sorted = sorted(dict2list(reallabel), key=lambda x: x[1], reverse=False)

    for item in list_sorted:
        labellist.append(item[0])
    return labellist


def getTrains2fit(datasql, resultsql):
    # 训练集 词向量空间、词向量矩阵
    result = fv.getdataset2('select cid, segcontent, category from content_category')
    counttrain = result[0]
    conlisttrain = result[2]  # 文本列表
    caglist = result[3]  # 类别列表
    print('训练集标签列表：')
    print(caglist)
    rw._writebunchobj('../data/训练集标签列表', caglist)
    tfidfmeritrain = fv.gettfidfMeriVoc1(conlisttrain)  # 获得tfidf词向量空间
    tspace = tfidfmeritrain[0]  # 训练集词向量空间
    print('训练集词向量空间：')
    print(tspace)
    trainmeri = tfidfmeritrain[1]  # 向量矩阵
    print('训练集词向量矩阵：')
    print(trainmeri)
    rw._writebunchobj('../data/训练集词向量矩阵', trainmeri)
    axis = tfidfmeritrain[2]

    # 应用集 词向量空间中的词向量矩阵
    result1 = fv.getdataset2(datasql)
    count = result1[0]
    cidlist = result1[1]
    conlist = result1[2]
    # 数据结构 tfidf[i][j]表示i类文本中的tf-idf权重
    tfidfmerisoft = fv.gettfidfMerisoft1(conlist, tspace)

    softdict = {}
    for i in range(count):
        labels = mlknn(tfidfmerisoft[i], labelset(trainmeri, caglist, counttrain, axis), 1.27)
        softdict[cidlist[i]] = labels

    for k, v in softdict.items():
        strv = ' '.join(v)
        print(k, strv)
        writecag2mysql(resultsql, (strv, k))


# if __name__ == '__main__':
#     group = array([[1.0, 0.9], [1.0, 1.0], [0.1, 0.2], [0.0, 0.1]])
#     labels = [1, 1, 0, 0]
#     newInput = array([0.3, 0.1])
#     numSamples = group.shape[0]
#     preres = mlknn(newInput, labelset(group, labels, 4, 2), 2)
#     print(preres)
