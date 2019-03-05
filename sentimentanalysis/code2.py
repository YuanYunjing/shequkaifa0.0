# -*- coding:utf-8 -*-

"""
@author:Yuan
@file:code2.py
@time:2018/3/23 19:10
"""

import pymysql
import code1 as cd
import numpy as np
import time

# 1.读取情感词典和待处理文件
# 情感词典
print("reading...")
posdict = cd.read_lines("./emotion_dict/pos_all_dict.txt")
negdict = cd.read_lines("./emotion_dict/neg_all_dict.txt")
# 程度副词词典
mostdict = cd.read_lines('./degree_dict/most.txt')  # 权值为2
verydict = cd.read_lines('./degree_dict/very.txt')  # 权值为1.5
moredict = cd.read_lines('./degree_dict/more.txt')  # 权值为1.25
ishdict = cd.read_lines('./degree_dict/ish.txt')  # 权值为0.5
insufficientdict = cd.read_lines('./degree_dict/insufficiently.txt')  # 权值为0.25
inversedict = cd.read_lines('./degree_dict/inverse.txt')  # 权值为-1

# 情感级别
emotion_level1 = "悲伤。在这个级别的人过的是八辈子都懊丧和消沉的生活。这种生活充满了对过去的懊悔、自责和悲恸。在悲伤中的人，看这个世界都是灰黑色的。"
emotion_level2 = "愤怒。如果有人能跳出冷漠和内疚的怪圈，并摆脱恐惧的控制，他就开始有欲望了，而欲望则带来挫折感，接着引发愤怒。愤怒常常表现为怨恨和复仇心里，它是易变且危险的。愤怒来自未能满足的欲望，来自比之更低的能量级。挫败感来自于放大了欲望的重要性。愤怒很容易就导致憎恨，这会逐渐侵蚀一个人的心灵。"
emotion_level3 = "淡定。到达这个能级的能量都变得很活跃了。淡定的能级则是灵活和无分别性的看待现实中的问题。到来这个能级，意味着对结果的超然，一个人不会再经验挫败和恐惧。这是一个有安全感的能级。到来这个能级的人们，都是很容易与之相处的，而且让人感到温馨可靠,这样的人总是镇定从容。他们不会去强迫别人做什么。"
emotion_level4 = "平和。他感觉到所有的一切都生机勃勃并光芒四射，虽然在其他人眼里这个世界还是老样子，但是在这人眼里世界却是一个。所以头脑保持长久的沉默，不再分析判断。观察者和被观察者成为同一个人，观照者消融在观照中，成为观照本身。"
emotion_level5 = "喜悦。当爱变得越来越无限的时候，它开始发展成为内在的喜悦。这是在每一个当下，从内在而非外在升起的喜悦。这个能级的人的特点是，他们具有巨大的耐性，以及对一再显现的困境具有持久的乐观态度，以及慈悲。同时发生着。在他们开来是稀松平常的作为，却会被平常人当成是奇迹来看待。"
# 情感波动级别
emotion_level6 = "情感波动很小，个人情感是不易改变的、经得起考验的。能够理性的看待周围的人和事。"
emotion_level7 = "情感波动较大，周围的喜悦或者悲伤都能轻易的感染他，他对周围的事物有敏感的认知。"


# 2.程度副词处理，根据程度副词的种类不同乘以不同的权值
def match(word, sentiment_value):
    if word in mostdict:
        sentiment_value *= 2.0
    elif word in verydict:
        sentiment_value *= 1.75
    elif word in moredict:
        sentiment_value *= 1.5
    elif word in ishdict:
        sentiment_value *= 1.2
    elif word in insufficientdict:
        sentiment_value *= 0.5
    elif word in inversedict:
        # print "inversedict", word
        sentiment_value *= -1
    return sentiment_value


# 3.情感得分的最后处理，防止出现负数
# Example: [5, -2] →  [7, 0]; [-4, 8] →  [0, 12]
def transform_to_positive_num(poscount, negcount):
    pos_count = 0
    neg_count = 0
    if poscount < 0 and negcount >= 0:
        neg_count += negcount - poscount
        pos_count = 0
    elif negcount < 0 and poscount >= 0:
        pos_count = poscount - negcount
        neg_count = 0
    elif poscount < 0 and negcount < 0:
        neg_count = -poscount
        pos_count = -negcount
    else:
        pos_count = poscount
        neg_count = negcount
    return pos_count, neg_count


# 求单条微博语句的情感倾向总得分
def single_review_sentiment_score(weibo_sent):
    single_review_senti_score = []
    cuted_review = cd.cut_sentence(weibo_sent)  # 句子切分，单独对每个句子进行分析
    sen_len = len(cuted_review)
    stm_num = 0

    for sent in cuted_review:
        seg_sent = cd.segmentation(sent)  # 分词
        seg_sent = cd.del_stopwords(seg_sent)[:]

        i = 0  # 记录扫描到的词的位置
        s = 0  # 记录情感词的位置
        poscount = 0  # 记录该分句中的积极情感得分
        negcount = 0  # 记录该分句中的消极情感得分

        # 默认每一个分句中只有一个情感词
        for word in seg_sent:  # 逐词分析
            print(word)
            if word in posdict:  # 如果是积极情感词
                print("posword:", word)
                poscount += 1  # 积极得分+1
                for w in seg_sent[s:i]:
                    poscount = match(w, poscount)
                # print "poscount:", poscount
                s = i + 1  # 记录情感词的位置变化
                stm_num += 1

            elif word in negdict:  # 如果是消极情感词
                print("negword:", word)
                negcount += 1
                for w in seg_sent[s:i]:
                    negcount = match(w, negcount)
                # print "negcount:", negcount
                s = i + 1
                stm_num += 1

            # 如果是感叹号，表示已经到本句句尾
            elif word == "！" or word == "!":
                for w2 in seg_sent[::-1]:  # 倒序扫描感叹号前的情感词，发现后权值+2，然后退出循环
                    if w2 in posdict:
                        poscount += 2
                        break
                    elif w2 in negdict:
                        negcount += 2
                        break
            i += 1
        # print "poscount,negcount", poscount, negcount
        single_review_senti_score.append(transform_to_positive_num(poscount, negcount))  # 对得分做最后处理
    pos_result, neg_result = 0, 0  # 分别记录积极情感总得分和消极情感总得分
    for res1, res2 in single_review_senti_score:  # 每个分句循环累加
        pos_result += res1
        neg_result += res2
    # print pos_result, neg_result
    result = pos_result - neg_result  # 该条微博情感的最终得分
    if stm_num == 0:
        result = 0
    else:
        result = round(result/stm_num, 1)
    return result

# 获得对应数据集得分，写入数据库
def getScore(datasql, resultsql):
    ms = pymysql.connect(host='localhost', user='root', passwd='123456', database='shequkaifa', charset='utf8')
    cur = ms.cursor()
    count = cur.execute(datasql)
    contents = cur.fetchall()
    cur.close()
    cur2 = ms.cursor()
    for content in contents:
        cid = content[0]
        score = single_review_sentiment_score(content[1])
        print(cid, score)
        cur2.execute(resultsql, (score, cid))
        ms.commit()

    cur2.close()
    ms.close()


if __name__ == '__main__':
    print(single_review_sentiment_score('给 物业 提个 意见 ： 小区 一到 下雪 就 没人 清理 ， 扫 也 是 猫 盖 屎 似地 ， 路上 很 滑 ， 行人 摔跤 ， 汽车 打滑 ， 现在 物业 的 功能 好像 只 停留 在 催交 物业费 了 。 小区 的 物业 是不是 可以 到 别的 小区 去 参观 学习 一下 ？ 去 雪梨 看看 ， 去 领袖 硅谷 看看 吧 ！ 看看 那里 是不是 你们 这个 扫法 ， 看看 他们 是不是 能 到 今天 的 雪 下 完 了 再 一起 清理 ，'))


