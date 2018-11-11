# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class NewsItem(Item):
    _id = Field()
    createTime = Field()
    publishTime = Field()
    source = Field()
    author = Field()
    title = Field()
    content = Field()
    upvotes = Field()
    shares = Field()
    comments = Field()
    top = Field()
    hot = Field()
    expire = Field()
    draft = Field()
