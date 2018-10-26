import time
import scrapy
import pymongo


class BiShiJie(scrapy.Spider):
    name = "bishijie"

    def __init__(self):
        client = pymongo.MongoClient('127.0.0.1', 27017)
        db = client['news']
        self.post = db['bishijie']
        self.post.create_index([("issue_time", pymongo.DESCENDING)], background=True)

    def start_requests(self):
        urls = [
            'http://www.bishijie.com/kuaixun/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        contents = response.css('ul[data-id]')
        for item in contents:
            issue_time = int(item.css('ul::attr(id)').extract_first())
            title = item.css('a::attr(title)')[1].extract()
            body = item.css('a::text')[1].extract().strip()

            db_item = {'title': title, 'issue_time': issue_time, 'body': body}
            if self.post.find({'issue_time': issue_time}).count() != 0:
                return
            self.post.insert(db_item)

            """
            filename = 'bishijie.txt'
            with open(filename, 'a+') as f:
                f.write('时间: ' + issue_time)
                f.write('\n')
                f.write('标题: ' + title)
                f.write('\n')
                f.write('内容: ' + body)
                f.write('\n---------------\n')
            """

        time.sleep(2)
        url = 'http://www.bishijie.com/api/newsv17/index?size=50&client=pc&timestamp=' + str(issue_time - 1)
        yield scrapy.Request(url, callback=self.load_more)

    def load_more(self, response):
        contents = str(response.body, encoding="utf-8")
        contents = eval(contents)["data"]
        if len(contents) == 0:
            return
        contents = contents[0]["buttom"]
        count = len(contents)
        print(count, 'items crawled ...')
        for item in contents:
            issue_time = item['issue_time']
            db_item = {'title': item['title'], 'issue_time': issue_time, 'body': item['content']}
            if self.post.find({'issue_time': issue_time}).count() != 0:
                return
            self.post.insert(db_item)

            """
            filename = 'bishijie.txt'
            with open(filename, 'a+') as f:
                f.write('时间: ' + str(item['issue_time']))
                f.write('\n')
                f.write('标题: ' + item['title'])
                f.write('\n')
                f.write('内容: ' + item['content'])
                f.write('\n----------------\n')
            """

        time.sleep(2)
        if count > 0:
            url = 'http://www.bishijie.com/api/newsv17/index?size=50&client=pc&timestamp=' + str(issue_time - 1)
            yield scrapy.Request(url, callback=self.load_more)


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


class ItemSpider(scrapy.Spider):
    name = 'listSpider'
    start_urls = {
        'http://lab.scrapyd.cn/'
    }

    def parse(self, response):
        contents = response.css('div.quote')
        for item in contents:
            text = item.css('.text::text').extract_first()
            author = item.css('.author::text').extract_first()
            tags = item.css('.tags .tag::text').extract()
            tags = ','.join(tags)

            filename = '%s-语录.txt' % author
            with open(filename, 'a+') as f:
                f.write(text)
                f.write('\n')
                f.write('标签：' + tags)
                f.write('\n-----------\n')

        nextpage = response.css('li.next a::attr(href)').extract_first()
        if nextpage is not None:
            nextpage = response.urljoin(nextpage)
            yield scrapy.Request(nextpage, callback=self.parse)


class ArgSpider(scrapy.Spider):
    name = 'argSpider'

    def start_requests(self):
        url = 'http://lab.scrapyd.cn/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        contents = response.css('div.quote')
        for item in contents:
            print('item:', item)
            text = item.css('.text::text').extract_first()
            tags = item.css('.tags .tag::text').extract()
            tags = ','.join(tags)

            filename = '%s-语录.txt' % tags
            with open(filename, 'a+') as f:
                f.write(text)
                f.write('\n')
                f.write('标签：' + tags)
                f.write('\n-----------\n')

        nextpage = response.css('li.next a::attr(href)').extract_first()
        if nextpage is not None:
            nextpage = response.urljoin(nextpage)
            yield scrapy.Request(nextpage, callback=self.parse)
