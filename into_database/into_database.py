# -*- coding:utf-8 -*-
# Created at 2015/7/20

"""
    Function:
        ***
"""
__author__ = 'Marchon'

import glob
import get_smali


def main_function():
    """
    Main Function
    :return:
    """
    apk_list = glob.glob("/home/ubuntu/apk0/androidApp/app_201311260117/*")
    for apk_path in apk_list:
        print apk_path
        get_smali.get_smali(apk_path)