# spider

### 爬虫文件
```
news/spiders/news_spider.py
```

### 数据处理文件
```
news/piplines.py
```

### 配置文件
```
news/settings.py
```

### 列出spider
```
scrapy list
```

### 抓取
```
scrapy crawl bishijie
```

### 定时运行
```
注意启动前修改redis配置
不加-u会出现有些打印不能实时看到，python会缓存
nohup python3 -u run_spider.py >run_spider.out 2>&1 &
```
