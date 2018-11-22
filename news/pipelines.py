# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import DropItem
import redis


class NewsPipeline(object):
    def __init__(self, mongo_host, mongo_port, mongo_db, mongo_auth_db, mongo_user, mongo_pass,
                 redis_host, redis_port, redis_pass, redis_db):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db
        self.mongo_auth_db = mongo_auth_db
        self.mongo_user = mongo_user
        self.mongo_pass = mongo_pass
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_pass = redis_pass
        self.redis_db = redis_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_auth_db=crawler.settings.get('MONGO_AUTH_DB'),
            mongo_user=crawler.settings.get('MONGO_USER'),
            mongo_pass=crawler.settings.get('MONGO_PASS'),
            redis_host=crawler.settings.get('REDIS_HOST'),
            redis_port=crawler.settings.get('REDIS_PORT'),
            redis_pass=crawler.settings.get('REDIS_PASS'),
            redis_db=crawler.settings.get('REDIS_DB'),
        )

    def open_spider(self, spider):
        self.mongoClient = pymongo.MongoClient("mongodb://{}:{}@{}:{}/?authSource={}"
                                          .format(self.mongo_user,
                                                  self.mongo_pass,
                                                  self.mongo_host,
                                                  self.mongo_port,
                                                  self.mongo_auth_db))
        # self.client = pymongo.MongoClient()
        db = self.mongoClient[self.mongo_db]
        self.collection = db['newsflash']
        self.collection.create_index([("time", pymongo.DESCENDING)], background=True)

        self.redis = redis.Redis(self.redis_host, self.redis_port, self.redis_db, self.redis_pass)

    def process_item(self, item, spider):
        if self.collection.find({'_id': item['_id']}).count() == 0:
            item['author'] = '网络抓取'
            # item['image'] = 'image--957970183-4761853cb2a04a7ab615098a0e99fbce.jpeg'
            item['upvotes'] = 0
            item['shares'] = 0
            item['comments'] = 0
            item['top'] = False
            item['hot'] = False
            item['expire'] = 0
            auto_release = self.redis.get('newsflash_auto_release')
            if auto_release is not None and auto_release.decode() == 'true':
                item['draft'] = False
                item['publishTime'] = item['createTime']
            else:
                item['draft'] = True
            self.collection.insert_one(dict(item))
        else:
            # raise DropItem('news_id %s has existed' % item['_id'])
            pass
        return item

    def close_spider(self, spider):
        self.mongoClient.close()
