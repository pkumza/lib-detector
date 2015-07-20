# -*- coding:utf-8 -*-
# Created at 2015/5/14
"""
    Function:
        找到重复次数超过50的package。只找代表元素。
"""
__author__ = 'Marchon'

import ConfigParser


def get_config(conf, section, key):
    """
    Load the config File : into_database.conf
    载入设置文件 : into_database.conf
    """
    config = ConfigParser.ConfigParser()
    config.read(conf)
    return config.get(section, key)