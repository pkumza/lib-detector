# -*- coding:utf-8 -*-
# Created at 2015/4/27
# Modified at 2015/4/29
"""
Function:
Add Index for packages in database。
作用：
给数据库中的packages增加索引

Usage:
Modify intodb.conf, then just run this code or import intodb.py then call function 'main_func()'.
用法：
修改intodb.conf的设置，然后运行本代码，或者import intodb.py之后调用main_func()方法即可。

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
    path = 'into_database.conf'
    config.read(path)
    return config.get(section, key)


def add_depth_1_total_call_1():
    """
    建立索引
    depth .ASCENDING
    total_call .ASCENDING
    :return: result string
    """
    conn = pymongo.MongoClient(get_config('database', 'db_host'), int(get_config('database', 'db_port')))
    db = conn[get_config('database', 'db_name')]
    packages = db.packages
    result = packages.create_index([('depth', pymongo.ASCENDING), ('total_call', pymongo.ASCENDING)])
    print str(result)


def add_depth_1_total_call_1_total_num_1():
    """
    建立索引
    depth .ASCENDING
    total_call .ASCENDING
    total_num .ASCENDING
    :return: result string
    """
    conn = pymongo.MongoClient(get_config('database', 'db_host'), int(get_config('database', 'db_port')))
    db = conn[get_config('database', 'db_name')]
    packages = db.packages
    result = packages.create_index([('depth', pymongo.ASCENDING), ('total_call', pymongo.ASCENDING),
    ('total_num', pymongo.ASCENDING)])
    print str(result)


def add_depth_1_btc_1_btn_1_bha_1():
    """
    建立索引
    depth .ASCENDING
    b_total_call .ASCENDING
    b_total_num .ASCENDING
    b_hash .ASCENDING
    :return:
    """
    conn = pymongo.MongoClient(get_config('database', 'db_host'), int(get_config('database', 'db_port')))
    db = conn.get_database(get_config('database', 'db_name'))
    packages = db.get_collection(get_config('database', 'db_brief'))
    result = packages.create_index([('depth', pymongo.ASCENDING), ('b_total_call', pymongo.ASCENDING),
                                    ('b_total_num', pymongo.ASCENDING), ('b_hash', pymongo.ASCENDING)])
    print(str(result))
    return "Function Finished."


def add_status_1():
    """
    建立索引
    status .ASCENDING
    :return: result string
    """
    conn = pymongo.MongoClient(get_config('database', 'db_host'), int(get_config('database', 'db_port')))
    db = conn[get_config('database', 'db_name')]
    packages = db.packages
    result = packages.create_index([('status', pymongo.ASCENDING)])
    print str(result)


def add_path_1():
    """
    建立索引
    path .ASCENDING
    :return: result string
    """
    conn = pymongo.MongoClient(get_config('database', 'db_host'), int(get_config('database', 'db_port')))
    db = conn[get_config('database', 'db_name')]
    packages = db[get_config('database', 'db_dep_pack')]
    result = packages.create_index([('path', pymongo.ASCENDING)])
    print str(result)


if __name__ == '__main__':
    print add_depth_1_btc_1_btn_1_bha_1()
    pass