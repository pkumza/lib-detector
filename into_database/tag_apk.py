# -*- coding:utf-8 -*-
__author__ = 'Marchon'
# Target : add  - apk_start = db.get_collection(get_config('database', 'db_apk_start'))

# This File has lost its use.
# 这个脚本是用来临时patch的
# 因为之前没有db.apk_start这一个项目，然后又已经运行了不少内容，这个就是用来做这个作用的。


import ConfigParser
import pymongo


def get_config(section, key):
    """
    Load the config File : into_database.conf
    载入设置文件 : into_database.conf
    """
    config = ConfigParser.ConfigParser()
    path = 'into_database.conf'
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
    apk_start = db.get_collection(get_config('database', 'db_apk_start'))
    packages = db.get_collection(get_config('database', 'db_packages'))
    db_api_dict = db.get_collection(get_config('database', 'db_dict'))
    api_dict = {}

    cnt = 0
    for package in packages.find():
        cnt += 1
        if cnt < 335800:
            continue
        if apk_start.find({"apk_name": package["apk"]}).count() == 0:
            if cnt % 100 == 0:
                print "Tag %d %s" % (cnt, package["apk"])
            apk_start.insert({"apk_name": package["apk"]})


if __name__ == '__main__':
    main_func()
