# -*- coding:utf-8 -*-

"""
@author:Yuan
@file:getsqnamebyurl.py
@time:2018/4/6 22:12
"""

'''
通过url获得
社区名称

'''

import pymysql
import time

if __name__ == '__main__':
    start = time.clock()

    print('writing...')

    # 将a_url填到content_copy1_copy中
    ms = pymysql.connect(host='localhost', user='root', passwd='123456', database='shequkaifa', charset='utf8')
    cur = ms.cursor()
    count = cur.execute("""UPDATE content_copy1_copy INNER JOIN content
                            ON content.`cid` = content_copy1_copy.`cid`
                            SET content_copy1_copy.`a_url` = content.`a_url`""")
    ms.commit()
    print('填写完成！！')

    # 获得详情表中的社区名称与对应url的关系字典
    cur_xq = ms.cursor()
    count_xq = cur_xq.execute("select name, xq_url from xiangqing")
    result_xq = cur_xq.fetchall()
    result1dict = {}
    for result in result_xq:
        result1dict[result[0]] = result[1].split('/')[2].split('.')[0] # 获得url中的关键信息
    # print(result1dict)

    # 获得目标表的cid, 和a_url
    cur_ccc = ms.cursor()
    count_ccc = cur_ccc.execute("select cid, a_url from content_copy1_copy")
    result_ccc = cur_ccc.fetchall()
    result2dict = {}
    for result in result_ccc:
        result2dict[result[0]] = result[1].split('/')[2].split('.')[0]

    cur_ud_sqname = ms.cursor()

    flag = 0
    for k_ccc, v_ccc in result2dict.items():
        for k_xq, v_xq in result1dict.items():
            if v_ccc == v_xq:
                count_ud_sqname = cur_ud_sqname.execute("update content_copy1_copy set sq_name = %s where cid = %s",
                                                        (k_xq, k_ccc))
                ms.commit()
                flag += 1

    print(flag, 'items have been updated.')

    elapsed = time.clock() - start
    print('Time used:', elapsed)


