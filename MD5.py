# -*- coding = utf-8 -*-
# @Author : Xinye Yang
# @File : MD5.py
# @Software : PyCharm
import hashlib
# md5 encryption method
def gen_md5(_str):
    hl = hashlib.md5()
    hl.update(_str.encode(encoding='utf-8'))
    return hl.hexdigest()
