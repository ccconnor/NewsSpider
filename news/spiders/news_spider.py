# -*- coding: utf-8 -*-

import json
import scrapy
from news.items import NewsItem


def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str.encode(encoding='utf-8'))
    return m.hexdigest()


class BiShiJie(scrapy.Spider):

    name = "bishijie"
    start_urls = [
        'http://www.bishijie.com/api/newsv17/index?size=50&client=pc'
    ]

    def parse(self, response):
        contents = json.loads(response.text)
        if len(contents['data']) == 0:
            return None
        contents = contents['data'][0]['buttom']
        self.logger.info('size of contents is %s' % len(contents))
        for news in contents:
            item = NewsItem()
            item['_id'] = md5('bishijie' + 'newsfalsh' + str(news.get('newsflash_id')))
            item['time'] = news.get('issue_time')
            item['source'] = '币世界'
            item['title'] = news.get('title')
            item['content'] = news.get('content')
            item['upvote'] = 0
            item['downvote'] = 0
            yield item


class JinSe(scrapy.Spider):
    name = 'jinse'
    start_urls = [
        'https://api.jinse.com/v4/live/list?limit=50&reading=false&source=web&flag=down'
    ]

    def parse(self, response):
        contents = json.loads(response.text)
        if contents['count'] == 0:
            return None
        contents = contents['list'][0]['lives']
        self.logger.info('size of contents is %s' % len(contents))
        for news in contents:
            item = NewsItem()
            content = news.get('content').replace('【','|').replace('】','|').split('|')
            item['_id'] = md5('jinsecaijing' + 'newsflash' + str(news.get('id')))
            item['time'] = news.get('created_at')
            item['source'] = '金色财经'
            item['title'] = content[2].strip()
            item['content'] = content[3]
            item['upvote'] = 0
            item['downvote'] = 0
            yield item