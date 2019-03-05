# -*- coding:utf-8 -*-

"""
@author:Yuan
@file:labelscore.py
@time:2018/3/29 19:57
"""

import pymysql
import numpy as np

# 获得每个社区各个标准的所有分值列表及平均分值
def getDatas():

    ms = pymysql.connect(host='localhost', user='root', passwd='123456', database='shequkaifa', charset='utf8')
    cur = ms.cursor()
    count = cur.execute('select sq_name, score, labels from shequscore_copy1_copy')
    result = cur.fetchall()
    # 定义社区字典 item为  社区名：{}
    # eg:'金融街融汇': {'小区居民': [array([ 2.8, -1. ,  0.1,  1.2, -0.6, -0.6, -0.3,  0.4, -0.3, -0.6]), 0.10999999999999996]...
    shequdict = {}
    for row in result:
        sq_name = row[0]
        score = row[1]
        labels = row[2]
        if sq_name == None:
            continue
        if sq_name in shequdict.keys():
            for label in labels.split(' '):
                if label == '':
                    continue
                if label in shequdict[sq_name].keys():  # 如果该标签已存在于该社区下
                    scorearray = shequdict[sq_name][label][0]
                    shequdict[sq_name][label][0] = np.append(scorearray, score)     # 为该标签添加本次获得的分值
                else:
                    shequdict[sq_name][label] = []  # 为该标签定义一个list：list[0]存储所有score list[1]
                    shequdict[sq_name][label].append(np.array([score]))
        else:
            shequdict[sq_name] = {}
            for label in labels.split(' '):
                if label == '':
                    continue
                shequdict[sq_name][label] = []
                shequdict[sq_name][label].append(np.array([score]))

    for k_name, v_name in shequdict.items():
        for k_label, v_label in v_name.items():
            v_label.append(np.average(v_label[0]))

    return shequdict


# 为overall.py提供数据
def getDatas4or(shequdict):
    sqdict = {}
    flag = 1
    ms = pymysql.connect(host='localhost', user='root', passwd='123456', database='shequkaifa', charset='utf8')
    for k_name, v_name in shequdict.items():
        for k_label, v_label in v_name.items():
            if k_name in sqdict.keys():

                sqdict[k_name][0] = np.append(sqdict[k_name][0], k_label)
                sqdict[k_name][1] = np.append(sqdict[k_name][1], v_label[1])
            else:
                sqdict[k_name] = []
                sqdict[k_name].append(np.array([k_label]))
                sqdict[k_name].append(np.array([v_label[1]]))
    # print(sqdict)
    for k, v in sqdict.items():
        print(k)
        strlabels = ''
        for i in range(len(v[0])):
            if i == 0:
                strlabels += v[0][i]
            else:
                strlabels += (',' + v[0][i])
        print(strlabels)
        strscores = ''
        for j in range(len(v[1])):
            if j == 0:
                strscores += str(v[1][j])
            else:
                strscores += (',' + str(v[1][j]))
        print(strscores)
        cur = ms.cursor()
        count = cur.execute('insert into labels_score values(%s, %s, %s, %s)',
                            (flag, k, strlabels, strscores))

        ms.commit()
        flag += 1
    return sqdict


def getDatas4el(shequdict):
    flag = 1
    for k_name, v_name in shequdict.items():
        print(k_name)

        ms = pymysql.connect(host='localhost', user='root', passwd='123456', database='shequkaifa', charset='utf8')
        for k_label, v_label in v_name.items():
            print(k_label)
            evaluatedict = {}
            evaluatedict['好评'] = 0
            evaluatedict['差评'] = 0
            evaluatedict['中评'] = 0
            for score in v_label[0]:
                if score > 0:
                    evaluatedict['好评'] += 1
                elif score < 0:
                    evaluatedict['差评'] += 1
                else:
                    evaluatedict['中评'] += 1
            print(evaluatedict.keys())
            perlist = []
            for v_num in evaluatedict.values():
                perlist.append(str(v_num/v_label[0].size * 100)+'%')
            print(perlist)

            flag += 1

            # cur = ms.cursor()
            # count = cur.execute('insert into label_score_percent values(%s, %s, %s, %s, %s, %s)',
            #                     (flag, k_name, k_label, perlist[0], perlist[1], perlist[2]))
            #
            # ms.commit()
    print(str(flag) + ' had been inserted.')
    # cur.close()
    ms.close()


getDatas4el(getDatas())



