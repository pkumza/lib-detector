import pymongo

conn = pymongo.MongoClient('localhost', 27017)
db = conn['lib-detect']
packages = db['brief_packages']
result = packages.create_index([('apk', pymongo.ASCENDING)])
print str(result)