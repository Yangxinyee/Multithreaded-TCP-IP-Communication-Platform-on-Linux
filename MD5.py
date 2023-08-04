# -*- coding = utf-8 -*-
# @Time : 2023/3/3 19:08
# @Author : XINXINXINYE
# @File : MD5.py
# @Software : PyCharm
import hashlib
# md5加密方法
def gen_md5(_str):
    hl = hashlib.md5()
    hl.update(_str.encode(encoding='utf-8'))
    return hl.hexdigest()