# -*- coding:utf-8 -*-
# Created at 2015/8/28 晚上九点多两点点儿
# Step 2
# Modified at 2015/8/28

__author__ = 'Zachary Marv'

import pymongo

"""
Add index
"""


conn = pymongo.MongoClient('localhost', 27017)
db = conn['lib-detect']
packages = db['d20']
result = packages.create_index([('path', pymongo.ASCENDING)])
print str(result)