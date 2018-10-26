import time
import scrapy
import pymongo


class BiShiJie(scrapy.Spider):
    name = "bishijie"

    def __init__(self):
        client = pymongo.MongoClient('127.0.0.1', 27017)
        db = client['news']
        self.post = db['bishijie']
        self.post.create_index([("newsflash_id", pymongo.DESCENDING), ("issue_time", pymongo.DESCENDING)],
                               background=True)

    def start_requests(self):
        urls = [
            'http://www.bishijie.com/api/newsv17/index?size=50&client=pc'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        contents = str(response.body, encoding="utf-8")
        contents = eval(contents)["data"]
        if len(contents) == 0:
            return
        contents = contents[0]["buttom"]
        count = len(contents)
        print(count, 'items crawled ...')
        for item in contents:
            issue_time = item['issue_time']
            newsflash_id = item['newsflash_id']
            db_item = {'newsflash_id': newsflash_id,
                       'issue_time': issue_time,
                       'title': item['title'],
                       'content': item['content']}
            if self.post.find({'newsflash_id': newsflash_id}).count() != 0:
                print('newsflash_id %s has existed.' % newsflash_id)
                return
            self.post.insert(db_item)

        time.sleep(2)
        if count > 0:
            url = 'http://www.bishijie.com/api/newsv17/index?size=50&client=pc&timestamp=' + str(issue_time)
            yield scrapy.Request(url, callback=self.parse)


class SimpleUrl(scrapy.Spider):
    name = "simpleUrl"
    start_urls = [
        'http://www.bishijie.com/'
    ]

    def parse(self, response):
        filename = 'simple_url.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('save file: %s' % filename)
