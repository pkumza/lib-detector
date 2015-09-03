# -*- coding:utf-8 -*-
# Created at 2015/8/28 晚上十点多一点点儿
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
    d6 = db['d26']
    d0 = db['d20']

    res_num = open('st5_res_num.txt', 'w')

    cur_apk_num = 0
    cur_apk = ""
    cur_apk_list = []
    cur_list = []

    cnt = 0
    for d in d6.find().sort([("apk", pymongo.ASCENDING),("depth", pymongo.ASCENDING)]):
        if cnt % 10000 == 0:
            print cnt
        cnt += 1

        if d['path'] in cur_apk_list:
            continue
        if d['apk'] != cur_apk:
            res_num.write(str(cur_apk_num))
            res_num.write('\n')
            if cur_apk_num > 50 :
                print "HAHA"
                print cur_list
                print "HEHE"
                print cur_apk_list
            cur_apk = d['apk']
            cur_apk_num = 0
            cur_apk_list = []
            cur_list = []
        if 'parent' in d:
            if d0.find({"path" : d['parent']}).count() == 0:
                continue
        cur_apk_list.append(d['path'])
        if '/'.join(d['path'].split('/')[:-1]) not in cur_apk_list:
            cur_apk_num += 1
            cur_list.append(d['path'])

    res_num.write(str(cur_apk_num))
    res_num.write('\n')
    res_num.close()

if __name__ == '__main__':
    main_func()