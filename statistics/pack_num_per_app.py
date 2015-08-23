# -*- coding:utf-8 -*-
# Created at 2015/8/23

"""
    Function:
        get statistics for package number per Android app.
"""
__author__ = 'Zachary Marv - 马子昂'

import ConfigParser
import pymongo
import sys


def get_config(section, key):
    """
    Load the config File : into_database.conf
    载入设置文件 : into_database.conf
    """
    config = ConfigParser.ConfigParser()
    path = 'sta.conf'
    config.read(path)
    return config.get(section, key)


def main_func():
    """
    Main Function
    主方法
    """
    num_dict = {}
    print("Main_Function Starts.")
    conn = pymongo.MongoClient(get_config('database', 'db_host'), int(get_config('database', 'db_port')))
    db = conn.get_database(get_config('database', 'db_name'))
    packages = db.get_collection(get_config('database', 'db_packages'))
    if len[sys.argv] > 1 and sys.argv[1] == 'a':
        result = packages.create_index([('apk', pymongo.ASCENDING)])
    apks = db.get_collection('apk_start')
    for apk in apks:
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


if __name__ == '__main__':

    main_func()