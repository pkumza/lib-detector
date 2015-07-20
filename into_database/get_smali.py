# -*- coding:utf-8 -*-
# Created at 2015/7/20

__author__ = 'Marchon'

"""
    Function:
        Convert APK into Smali file with Apktool(Version 2.0.1)
"""

import ConfigParser
import pymongo
import subprocess

def get_config(section, key):
    """
    Load the config File : into_database.conf
    载入设置文件 : into_database.conf
    """
    config = ConfigParser.ConfigParser()
    path = 'into_database.conf'
    config.read(path)
    return config.get(section, key)


def get_smali(path):
    """
    Convert APK into Smali file.
    :param path:
    :return:
    """
    cmd = "/home/ubuntu/lib-detector/tool/apktool decode " + path
    subprocess.call(cmd, shell=True)


def main_function_tmp():
    """
    MainFunction
    :return: 无
    """
    conn = pymongo.MongoClient(get_config('database', 'db_host'), int(get_config('database', 'db_port')))
    db = conn.get_database(get_config('database', 'db_name'))
    pacakges = db.get_collection(get_config('database', 'db_packages'))


