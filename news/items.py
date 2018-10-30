# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class NewsItem(Item):
    _id = Field()
    issue_time = Field()
    title = Field()
    content = Field()
    upvote = Field()
    downvote = Field()


class BishijieNewsItem(NewsItem):
    collection = 'bishijie'


class JinsecaijingNewsItem(NewsItem):
    collection = 'jinsecaijing'
