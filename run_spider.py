#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import scrapy.cmdline


def run_for_linux():
    while True:
        print('run spider at %s' % time.asctime(time.localtime(time.time())))
        os.system("scrapy crawl bishijie")
        os.system("scrapy crawl jinse")
        time.sleep(60)


def run_for_windows():
    # scrapy.cmdline.execute(['scrapy', 'crawl', 'bishijie'])
    scrapy.cmdline.execute(['scrapy', 'crawl', 'jinse'])


run_for_windows()
