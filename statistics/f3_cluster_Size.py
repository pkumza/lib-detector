# -*- coding:utf-8 -*-
# Created at 2015/7/20
# Modified at 2015/8/28

__author__ = 'Marchon'

import json
import pymongo


def main_func(threshold):
    print 'Start'
    print threshold
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['test']
    dep1 = db['d1']
    # res_call = {}
    res_num = {}
    cnt = 0
    rss = open('top20_'+str(threshold)+'.txt', 'w')
    for d in dep1.find():
        if cnt % 100000 == 0:
            print cnt
        cnt += 1
        num = d['dep_num']
        if num in res_num:
            res_num[num] += 1
        else:
            res_num[num] = 1
        if num > threshold:
            rss.write(str(num))
            rss.write(',')
            rss.write(d['s_path'])
            rss.write('\n')
    result = open('res_num_'+str(threshold)+'.txt', 'w')
    result.write(json.dumps(res_num))
    result.close()
    rss.close()

if __name__ == '__main__':
    main_func(50)
    main_func(100)
    main_func(500)
    main_func(1000)