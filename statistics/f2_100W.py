# -*- coding:utf-8 -*-
# Created at 2015/8/26

"""

figure 2: the distribution of cluster size

"""

__author__ = 'Zachary Marv'

import json
import pymongo


def main_func():
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['lib-detect']
    dep2 = db['brief_packages']
    res_call = {}
    res_num = {}
    cnt = 0
    cur_apk = ""
    per_num = 0
    per_call = 0
    for d in dep2.find().sort("apk", pymongo.ASCENDING):
        if cnt % 1000 == 0:
            print cnt
        cnt += 1
        if d['apk'] == cur_apk:
            #if d['direct_dir_num'] == 0:
            per_num += 1
            per_call += d['b_total_call']
        else:
            if per_num in res_num:
                res_num[per_num] += 1
            else:
                res_num[per_num] = 1
            per_num = 0
            per_call = 0
            cur_apk = d['apk']

    if per_num in res_num:
        res_num[per_num] += 1
    else:
        res_num[per_num] = 1

    result = open('res_num.txt', 'w')
    result.write(json.dumps(res_num))
    result.close()

if __name__ == '__main__':
    main_func()