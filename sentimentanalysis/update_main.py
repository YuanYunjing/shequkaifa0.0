# -*- coding:utf-8 -*-

"""
@author:Yuan
@file:update_main.py
@time:2018/3/29 18:45
"""

'''
主函数
整理社区分值结果

'''


import pymysql
import time

if __name__ == '__main__':
    start = time.clock()

    print('writing...')
    ms = pymysql.connect(host='localhost', user='root', passwd='123456', database='shequkaifa', charset='utf8')
    cur = ms.cursor()
    '''
    # cid不冲突时
    
    count = cur.execute("""SELECT content_test.cid, nad_content.sq_name, content_test.finalscore ,
                                    content_test.precag, content_test.content
                        FROM content_test, nad_content 
                        WHERE content_test.`cid`=nad_content.`cid` AND nad_content.sq_name!=''""")
    flag = 0
    for i in range(count):
        fc = cur.fetchone()
        cur_cid = ms.cursor()
        count_cid = cur_cid.execute("select cid from shequscore where cid = %s", (fc[0]))
        if count_cid == 0:
            cur_inser = ms.cursor()
            cur_inser.execute("insert into shequscore values(%s, %s, %s, %s, %s)", (fc[0], fc[1], fc[2], fc[3], fc[4]))
            flag += 1
            ms.commit()
            
    print(flag, 'rows have been writed.')
    
    '''
    count = cur.execute("""SELECT cid, sq_name, content, labels, score
                            from content_copy1_copy
                            where labels != ''""")
    flag = 0
    for i in range(count):
        fc = cur.fetchone()
        cur_cid = ms.cursor()
        count_cid = cur_cid.execute("select cid from shequscore_copy1_copy where cid = %s", (fc[0]))
        if count_cid == 0:
            cur_inser = ms.cursor()
            cur_inser.execute("insert into shequscore_copy1_copy values(%s, %s, %s, %s, %s)", (fc[0], fc[1], fc[2], fc[3], fc[4]))
            flag += 1
            ms.commit()

    print(flag, 'rows have been writed.')

    elapsed = time.clock() - start
    print('Time used:', elapsed)
