# -*- coding:utf-8 -*-

"""
@author:Yuan
@file:Airblocker.py
@time:2018/1/21 10:09
"""

import time

import pandas as pd



# 搜索含广告用语的title
def adFind(titl, ad):
    rs = titl.find(ad)
    return rs

# 去广告（读入路径， 写入路径， 去广告列名）
def clearAd(rdPath, wtPath, colName):
    datas = pd.read_csv(rdPath)

    for index, row in datas.iterrows():
        title = str(row[colName])
        adList = ['招生', '培训', '求租', '转让', '出租', '红利', '优惠', '折扣', '出售', '急售', '已售', '急租', '求车位',
                  '招聘', '火热', '收支明细', '求购', '系统公告', '购狂欢盛宴', '换车位', '盛惠', '寻猫启示',
                  '寻人启示', '赢取',
                  '开业', '抽奖', '转租', '购房', '团购', '大奖', '红包', '求店员', '投票', '1元购', '促销',
                  '开班', '论坛升级公告']
        for ad in adList:
            result = adFind(title, ad)
            if result > -1:
                datas.drop([index], inplace=True)
                break

    datas.to_csv(wtPath, index=False)


if __name__ == '__main__':

    start = time.clock()

    clearAd("../data/content.csv", "../data/nad_content.csv", "title")

    elapsed = (time.clock() - start)
    print('-------------------------')
    print("Time used:", elapsed)