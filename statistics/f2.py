# -*- coding:utf-8 -*-
# Created at 2015/7/20

"""

figure 3: the distribution of cluster size


"""

'''
{
"_id" : ObjectId("55d534f8ea9448062d156f01"),
"status" : 4,
"direct_file_num" : 0,
"file_num" : 5726,
"path_parts" : [ "" ],
"total_num" : 4143,
"old_id" : ObjectId("55aee25aa0f89a77fe50766b"),
"b_total_call" : 33001,
"dir_num" : 121,
"apk" : "/home/ubuntu/lib-detector/decoded/com.workoutroutines.thedumbbellworkoutlite.apk",
"depth" : 0,
"b_total_num" : 4143,
"total_call" : 120065,
"b_hash" : 520442,
"direct_dir_num" : 2,
"path" : "/home/ubuntu/lib-detector/decoded/com.workoutroutines.thedumbbellworkoutlite.apk/smali" }




{ "_id" : ObjectId("55d537a1ea944807514616ae"),
 "status" : 1,
 "direct_file_num" : 3,
 "file_num" : 3,
 "path_parts" : [ "Values" ],
 "total_num" : 2,
 "old_id" : ObjectId("55af75e4a0f89a77fe57c02c"),
 "b_total_call" : 5,
 "dir_num" : 0,
 "apk" : "/home/ubuntu/lib-detector/decoded/com.appscapital.xabia.apk",
 "depth" : 1,
 "b_total_num" : 2,
 "total_call" : 5,
 "dep_num" : 218,
 "b_hash" : 1229,
 "direct_dir_num" : 0,
 "path" : "/home/ubuntu/lib-detector/decoded/com.appscapital.xabia.apk/smali/Values" }

'''
__author__ = 'Marchon'

import json
import pymongo


def main_func():
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn['lib-detect']
    dep2 = db['dep_packages2']
    # res_call = {}
    res_num = {}
    cnt = 0
    for d in dep2.find():
        if cnt % 1000 == 0:
            print cnt
        cnt += 1
        num = 1
        if d['status'] == 4:
            num = dep2.find({'apk': d['apk']}).count()
            if num in res_num:
                res_num[num] += 1
            else:
                res_num[num] = 1

    result = open('res_num.txt', 'w')
    result.write(json.dumps(res_num))
    result.close()

if __name__ == '__main__':
    main_func()