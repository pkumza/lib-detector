# -*- coding:utf-8 -*-
# Created at 2015/7/20

"""
    Function:
        ***
"""
__author__ = 'Marchon'

import ConfigParser
import pymongo
'''
Before:
{
"_id" : ObjectId("55ae0deea0f89a745ee0e88d"),
"status" : 0,
"api_dict" : { "2859" : 1, "2860" : 1, "2861" : 1, "2728" : 1, "0" : 1, "2672" : 1 },
"dir_num" : 0,
"apk" : "/home/ubuntu/lib-detector/decoded/com.momgame.friuts.apk",
"direct_dir_num" : 0,
"path" : "/home/ubuntu/lib-detector/decoded/com.momgame.friuts.apk/smali/com/mopub/nativeads/factories",
"direct_file_num" : 1,
"path_parts" : [ "com", "mopub", "nativeads", "factories" ],
"total_num" : 6,
"total_call" : 6,
"depth" : 4,
"file_num" : 1 }
'''

'''
After:
{ "_id" : ObjectId("55c1dcbfea9448082b3c6003"),
 "status" : 0,
 "direct_file_num" : 1,
 "file_num" : 1,
 "path_parts" : [ "com",
 "google",
 "android",
 "gms",
 "actions" ],
 "total_num" : 1,
 "old_id" : ObjectId("55ae11a8a0f89a77fe4588c2"),
 "b_total_call" : 1,
 "dir_num" : 0,
 "apk" : "/home/ubuntu/lib-detector/decoded/com.ska.apk",
 "depth" : 5,
 "b_total_num" : 1,
 "b_hash" : 1,
 "direct_dir_num" : 0,
 "path" : "/home/ubuntu/lib-detector/decoded/com.ska.apk/smali/com/google/android/gms/actions",
 "total_call" : 1 }
'''


def get_config(section, key):
    """
    Load the config File : into_database.conf
    载入设置文件 : into_database.conf
    """
    config = ConfigParser.ConfigParser()
    path = 'hash.conf'
    config.read(path)
    return config.get(section, key)


def main_func():
    """
    Main Function
    主方法
    """
    print("Main_Function Start.")
    conn = pymongo.MongoClient(get_config('database', 'db_host'), int(get_config('database', 'db_port')))
    db = conn.get_database(get_config('database', 'db_name'))
    packages = db.get_collection(get_config('database', 'db_packages'))
    db_api_dict = db.get_collection(get_config('database', 'db_dict'))
    brief = db.get_collection(get_config('database', 'db_brief'))
    cnt = 0
    for package in packages.find():
        cnt += 1
        if cnt % 100 == 0:
            print cnt
        cnt_file = open('cnt.txt', 'w')
        cnt_file.write(str(cnt))
        cnt_file.close()
        # brief_package
        br = {}
        pass
        br["old_id"] = package["_id"]
        br["status"] = package["status"]
        br["dir_num"] = package["dir_num"]
        br["apk"] = package["apk"]
        br["direct_dir_num"] = package["direct_dir_num"]
        br["path"] = package["path"]
        br["direct_file_num"] = package["direct_file_num"]
        br["path_parts"] = package["path_parts"]
        br["total_num"] = package["total_num"]
        br["total_call"] = package["total_call"]
        br["depth"] = package["depth"]
        br["file_num"] = package["file_num"]
        b_total_num = 0
        b_total_call = 0
        b_hash = 0
        for a in package["api_dict"]:
            if int(a) < 100000:
                b_total_num += 1
                b_total_call += package["api_dict"][a]
                b_hash = (b_hash + int(a) * package["api_dict"][a]) % 999983
        br["b_total_num"] = b_total_num
        br["b_total_call"] = b_total_call
        br["b_hash"] = b_hash
        brief.insert(br)


if __name__ == '__main__':
    main_func()
