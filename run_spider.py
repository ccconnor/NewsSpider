#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os

while True:
    print('run spider at %s' % time.asctime(time.localtime(time.time())))
    os.system("scrapy crawl bishijie")
    time.sleep(60)
