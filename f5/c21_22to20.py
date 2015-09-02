# -*- coding:utf-8 -*-
# Created at 2015/8/28 晚上九点多一点点儿
# Modified at 2015/8/28

__author__ = 'Zachary Marv'

import pymongo

"""
Input: D21 D22
Output: D20
"""


def main_func():
    print 'Start'
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['lib-detect']
    d1 = db['d21']
    d2 = db['d22']
    d0 = db['d20']
    cnt = 0

    for d in d1.find():
        if cnt % 100 == 0:
            print cnt
        cnt += 1
        d0.insert(d)
    for d in d2.find():
        if cnt % 1000 == 0:
            print cnt
        cnt += 1
        if d['dep_num'] >= 100:
            d0.insert(d)

if __name__ == '__main__':
    main_func()