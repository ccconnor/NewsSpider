# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import DropItem


class NewsPipeline(object):
    def __init__(self, mongo_host, mongo_port, mongo_db, mongo_auth_db, mongo_user, mongo_pass):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db
        self.mongo_auth_db = mongo_auth_db
        self.mongo_user = mongo_user
        self.mongo_pass = mongo_pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_auth_db=crawler.settings.get('MONGO_AUTH_DB'),
            mongo_user=crawler.settings.get('MONGO_USER'),
            mongo_pass=crawler.settings.get('MONGO_PASS')
        )

    def open_spider(self, spider):
        # self.client = pymongo.MongoClient("mongodb://{}:{}@{}:{}/?authSource={}"
        #                                   .format(self.mongo_user,
        #                                           self.mongo_pass,
        #                                           self.mongo_host,
        #                                           self.mongo_port,
        #                                           self.mongo_auth_db))
        self.client = pymongo.MongoClient()
        db = self.client[self.mongo_db]
        self.collection = db['newsflash']
        self.collection.create_index([("time", pymongo.DESCENDING)], background=True)

    def process_item(self, item, spider):
        if self.collection.find({'_id': item['_id']}).count() == 0:
            self.collection.insert_one(dict(item))
        else:
            # raise DropItem('news_id %s has existed' % item['_id'])
            pass
        return item

    def close_spider(self, spider):
        self.client.close()
