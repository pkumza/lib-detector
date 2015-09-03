# -*- coding:utf-8 -*-
# Created at 2015/7/20

"""

figure 4:
    Just a Value
    Lib per App.

"""

__author__ = "Zachary Marv"


import json
import pymongo


def main_func():
    print 'Start'
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['test']
    d1 = db['d31']
    d2 = db['d32']

    num = 0

    for d in d1.find():
        if len(d['path'].split('/')) < 10:
            num += d['dep_num']
    for d in d2.find():
        if d['dep_num'] < 100:
            continue
        if len(d['path'].split('/')) < 10:
            num += d['dep_num']

    result = open('n.txt', 'w')
    result.write(str(num) + '\n')
    result.close()

if __name__ == '__main__':
    main_func()