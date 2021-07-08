import pymongo

# 连接数据库
def connect_mongodb(host, port, username, password, use_db):
    client = pymongo.MongoClient('mongodb://{}:{}@{}:{}'.format(username, password, host, port))
    return client[use_db]


if __name__ == '__main__':
    mongodb_host = '192.168.0.107'
    mongodb_port = 27017
    mongodb_username = 'gsh'
    mongodb_password = 'gsh'
    mongodb_use_db = 'gsh-test'
    db = connect_mongodb(mongodb_host, mongodb_port, mongodb_username, mongodb_password, mongodb_use_db)

    # 用户信息
    user_info = {
        'nickname': 'gsh',
        'atc': 5,
        'def': 99,
        'hp': 500,
        'skill': [
            {
                'name': '铁头功',
                'def': 50
            },
            {
                'name': '吃包子',
                'hp': 100
            }
        ]
    }
    # 插入
    # db.user代表操作user表
    res = db.user.insert_one(user_info)
    # 返回当前新增数据的Object_id是bson类型 不能被json序列化，可以转换为字符串
    print(res.inserted_id)
    res = db.user.find({})
    for i in res:
        # 返回字典
        print(i)
