# -*- coding: utf-8 -*-

# Scrapy settings for tutorial project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import random

BOT_NAME = 'tutorial'

SPIDER_MODULES = ['tutorial.spiders']
NEWSPIDER_MODULE = 'tutorial.spiders'

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"


class USER_AGENT_ENUM(object):
    CHROME = 0
    FIREFOX = 1
    IE = 2
    ANDROID = 3
    IPHONE = 4


USER_AGENT_MAPPING = {
    USER_AGENT_ENUM.CHROME:
        'Mozilla/%s.0 (Windows NT %s.0; WOW%s) AppleWebKit/%s.36 (KHTML, like Gecko) Chrome/%s.0.2357.65 Safari/%s.36' \
        % (random.randint(4, 5), random.randint(8, 10), random.choice([32, 64]),
           random.randint(521, 537), random.randint(31, 43), random.randint(521, 537)),
    USER_AGENT_ENUM.FIREFOX:
        'Mozilla/%s.0 (Windows NT %s.0; WOW%s; rv:%s.0) Gecko/20100101 Firefox/%s.0' \
        % (random.randint(4, 5), random.randint(8, 10), random.choice([32, 64]), random.randint(29, 36),
           random.randint(29, 36)),
    USER_AGENT_ENUM.IE:
        'Mozilla/%s.0 (compatible; MSIE %s.0; Windows NT %s.1; WOW%s; Trident/%s.0)' \
        % (random.randint(4, 5), random.randint(8, 10), random.randint(8, 10), random.choice([32, 64]),
           random.randint(4, 5)),
    USER_AGENT_ENUM.ANDROID:
        'Mozilla/%s.0(Linux;U;Android4.%s.%s;zh-cn;%s)AppleWebKit/534.30(KHTML, likeGecko)Version/%s.0MobileSafari/534.30' \
        % (random.randint(4, 5), random.randint(0, 3), random.randint(0, 3), \
           random.choice(["nokia", "sony", "ericsson", "mot", "samsung", "sgh", "lg", "sie", "philips", "panasonic",
                          "alcatel", "lenovo", "cldc", "midp", "wap", "mobile"]), \
           random.randint(3, 5)),
    USER_AGENT_ENUM.IPHONE:
        'Mozilla/%s.0(iPhone;CPUiPhoneOS%s_%s_%slikeMacOSX)AppleWebKit/%s00.1.%s(KHTML, likeGecko)Mobile/12H321' \
        % (random.randint(4, 5), random.randint(6, 8), random.randint(0, 1), random.randint(0, 4),
           random.randint(4, 6), random.randint(1, 4))
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS_PER_IP = 4

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'tutorial.middlewares.ProxyMiddleware': 90,
    'tutorial.middlewares.RandomUserAgent': 490,
}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'tutorial.pipelines.WebcrawlerScrapyPipeline': 300,  # 保存到mysql数据库
    'tutorial.pipelines.JsonWithEncodingPipeline': 300,  # 保存到文件中
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 3
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

COOKIES_ENABLED = False

# Mysql数据库的配置信息
MYSQL_HOST = '139.224.219.76'
MYSQL_DBNAME = 'testdb'  # 数据库名字，请修改
MYSQL_USER = 'root'  # 数据库账号，请修改
MYSQL_PASSWD = 'DavidZhang=123456'  # 数据库密码，请修改

MYSQL_PORT = 3306  # 数据库端口，在dbhelper中使用

IPPOOL_HTTP = None
IPPOOL_HTTPS = None
