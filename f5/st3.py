# -*- coding:utf-8 -*-
# Created at 2015/8/28 晚上九点多一点点儿
# Modified at 2015/8/28

__author__ = 'Zachary Marv'

import pymongo

"""
Insert: D20 into D26

"""


def main_func():
    print 'Start'
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['lib-detect']
    d1 = db['d20']
    d0 = db['d26']
    cnt = 0

    for d in d1.find():
        if cnt % 100 == 0:
            print cnt
        cnt += 1
        # 都是因为手抖，代码让跑了但是没有正确地nohup，所以跑出去500个。哎呀。
        try:
            d0.insert(d)
        except:
            pass

if __name__ == '__main__':
    main_func()