# -*- coding: utf-8 -*-

import scrapy
import json
from news.items import BishijieNewsItem


class BiShiJie(scrapy.Spider):
    name = "bishijie"
    start_urls = [
        'http://www.bishijie.com/api/newsv17/index?size=50&client=pc'
    ]

    def parse(self, response):
        contents = json.loads(response.text)
        self.logger.info('size of contents is %s' % len(contents['data']))
        if len(contents['data']) == 0:
            return None
        contents = contents['data'][0]['buttom']
        for news in contents:
            item = BishijieNewsItem()
            item['_id'] = news.get('newsflash_id')
            item['issue_time'] = news.get('issue_time')
            item['title'] = news.get('title')
            item['content'] = news.get('content')
            item['upvote'] = 0
            item['downvote'] = 0
            yield item
