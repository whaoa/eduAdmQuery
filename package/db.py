import pymongo

# 链接数据库
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.TYUT
print('mongodb数据库连接成功')