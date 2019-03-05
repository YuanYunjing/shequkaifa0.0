# -*- coding:utf-8 -*-

"""
@author:Yuan
@file:read&write.py
@time:2018/1/27 16:17
"""
import pickle as p


def _readfile(path):
    with open(path, "rb") as fp:
        content = fp.read().decode("utf-8")  # 读取中文文本
    return content


# 保存至文件
def savefile(savepath, content):
    with open(savepath, "wb") as fp:
        fp.write(content)



# 读取bunch对象
def _readbunchobj(path):
    with open(path, "rb") as file_obj:
        bunch = p.load(file_obj)
    return bunch


# 写入bunch对象
def _writebunchobj(path, bunchobj):
    with open(path, "wb") as file_obj:
        p.dump(bunchobj, file_obj)

