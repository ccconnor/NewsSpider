#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import scrapy.cmdline
from news.settings import *
import redis


def get_news_source():
    redis_client = redis.Redis(REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASS)
    if redis_client is None:
        return []
    sources = redis_client.get('news_source')
    if sources is None:
        return []
    source_list = sources.decode().split(';')
    if len(source_list) == 0:
        return []
    return source_list


def run_for_linux():
    while True:
        print('run spider at %s' % time.asctime(time.localtime(time.time())))
        source_list = get_news_source()
        if len(source_list) == 0:
            source_list.append('金色财经')
        for source in source_list:
            print('crawling', source)
            if source == '金色财经':
                os.system("scrapy crawl jinse")
            elif source == '币世界':
                os.system("scrapy crawl bishijie")
            elif source == '币快报':
                os.system("scrapy crawl bikuaibao")
            else:
                print(source, 'is not supported!')
                os.system("scrapy crawl bishijie")
        time.sleep(60)


def run_for_windows():
    scrapy.cmdline.execute(['scrapy', 'crawl', 'jinse'])
    scrapy.cmdline.execute(['scrapy', 'crawl', 'bishijie'])
    scrapy.cmdline.execute(['scrapy', 'crawl', 'bikuaibao'])


run_for_linux()
# run_for_windows()
