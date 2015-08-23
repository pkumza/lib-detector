# -*- coding:utf-8 -*-
# Created at 2015/8/23

"""
    Function:
        get statistics for package number per Android app.
"""
__author__ = 'Zachary Marv - 马子昂'

import ConfigParser
import pymongo


def get_config(section, key):
    """
    Load the config File : into_database.conf
    载入设置文件 : into_database.conf
    """
    config = ConfigParser.ConfigParser()
    path = 'sta.conf'
    config.read(path)
    return config.get(section, key)


if __name__ == '__main__':

    num_dict = {}
    print("Main_Function Starts.")
    conn = pymongo.MongoClient(get_config('database', 'db_host'), int(get_config('database', 'db_port')))
    db = conn.get_database(get_config('database', 'db_name'))
    packages = db.get_collection(get_config('database', 'db_packages'))
    # print packages.create_index([('apk', pymongo.ASCENDING)])
    cnt = 0
    log = open('log.txt', 'w')
    apks = db.get_collection('apk_start').find()
    for app in apks:
        apk = app['apk_name']
        cnt += 1
        if cnt % 100 == 0:
            log.write(str(cnt)+'\n')
            if cnt % 1000 == 0:
                print cnt
        num = packages.find({"apk" : apk}).count()
        if num not in num_dict:
            num_dict[num] = 1
        else:
            num_dict[num] += 1
    res = open('../stat/pack_num_per_app.txt', 'w')
    for i in num_dict:
        res.write(str(i))
        res.write(',')
        res.write(str(num_dict[i]))
        res.write('\n')
    res.close()
    print("Main_Function Ends.")