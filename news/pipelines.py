# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import DropItem


class NewsPipeline(object):
    def __init__(self, mongo_uri, mongo_port, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_HOST'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db['bishijie'].create_index([("issue_time", pymongo.DESCENDING)], background=True)

    def process_item(self, item, spider):
        collection = item.collection
        if self.db[collection].find({'_id': item['_id']}).count() == 0:
            self.db[collection].insert_one(dict(item))
        else:
            raise DropItem('news_id %s has existed' % item['_id'])
        return item

    def close_spider(self, spider):
        self.client.close()
