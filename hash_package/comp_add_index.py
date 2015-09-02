import pymongo

conn = pymongo.MongoClient('localhost', 27017)
db = conn['test']
packages = db['bbb']
result = packages.create_index([('depth', pymongo.ASCENDING), ('b_total_call', pymongo.ASCENDING),
                                ('b_total_num', pymongo.ASCENDING), ('b_hash', pymongo.ASCENDING)])
print str(result)