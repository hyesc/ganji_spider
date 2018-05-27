# 将mongo数据读取出来保存到mysql中
from pymongo import MongoClient
import pymysql


def mongp2sql():
    client = MongoClient(host='localhost', port=27017)
    # ganji_phone = client.ganji.ganji_phone
    ganji_phone = client.ganji.test

    # db.stu.find().skip(5).limit(4)
    count = ganji_phone.count()  # 总条目数
    limit = 50  # 一次读取500条
    times = count // limit
    skip = 0  # 起始跳过0

    for i in range(times + 1):
        cursor = ganji_phone.find({}).skip(skip).limit(limit)
        for item in cursor:
            print(item)
            # 从item中取出数据,保存到mysql中

        skip += limit


if __name__ == '__main__':
    mongp2sql()
