# -*- coding: utf-8 -*-

import json
import hashlib
import collections
import scrapy
from news.items import NewsItem


def md5(data):
    m = hashlib.md5()
    m.update(data.encode(encoding='utf-8'))
    return m.hexdigest()


class BiShiJie(scrapy.Spider):

    name = "bishijie"
    start_urls = [
        'http://www.bishijie.com/api/newsv17/index?size=20&client=pc'
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
            item['createTime'] = news.get('issue_time')
            item['title'] = news.get('title')
            item['content'] = news.get('content')
            item['source'] = '币世界'
            yield item


class JinSe(scrapy.Spider):
    name = 'jinse'
    start_urls = [
        'https://api.jinse.com/v4/live/list?limit=20&reading=false&source=web&flag=down'
    ]

    def parse(self, response):
        contents = json.loads(response.text)
        if contents['count'] == 0:
            return None
        contents = contents['list'][0]['lives']
        self.logger.info('size of contents is %s' % len(contents))
        for news in contents:
            item = NewsItem()
            pos = news.get('content').find('】')
            item['_id'] = md5('jinsecaijing' + 'newsflash' + str(news.get('id')))
            item['createTime'] = news.get('created_at')
            item['title'] = news.get('content')[1:pos]
            item['content'] = news.get('content')[pos+1:]
            item['source'] = '金色财经'
            yield item


class BiKuaiBao(scrapy.Spider):
    name = 'bikuaibao'

    def start_requests(self):
        url = 'http://api-qa.beekuaibao.com/thirdparty/getOpenData/V2'
        headers = {
            'Content-Type': 'application/json'
        }
        data = collections.OrderedDict()
        data['businessNo'] = 'B100000'
        data['tag'] = ''
        data['requestId'] = '12345678'
        data['id'] = ''
        json_data = json.dumps(data).replace(' ', '')
        key = 'bkb88888888'
        sha512 = hashlib.sha512()
        sha512.update(key.encode('utf-8'))
        sha512.update(json_data.encode('utf-8'))
        signature = sha512.hexdigest().upper()
        body = {
            'channel': 'imapp',
            'sign': signature,
            'data': data
        }
        yield scrapy.Request(url=url, callback=self.parse, method='POST', headers=headers, body=json.dumps(body))

    def parse(self, response):
        contents = json.loads(response.text)
        contents = contents['data']['body']['content']
        self.logger.info('size of contents is %s' % len(contents))
        for news in contents:
            item = NewsItem()
            item['_id'] = md5('bikuaibao' + 'newsfalsh' + str(news.get('id')))
            item['createTime'] = news.get('publishDate')//1000
            item['title'] = news.get('title')
            item['content'] = news.get('text')
            item['source'] = '币快报'
            yield item
