import pymongo

conn = pymongo.MongoClient('localhost', 27017)
db = conn['lib-detect']
packages = db['brief_packages']
c = open("wall.txt",'w')
for i in packages.find({"s_path": "com/mirage/livewallpaper"}):
    c.write(str(i))
c.close()