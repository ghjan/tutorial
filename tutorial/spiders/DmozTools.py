# -*- coding: utf-8 -*-
import scrapy


class DmoztoolsSpider(scrapy.Spider):
    name = 'DmoztoolsSpider'
    allowed_domains = ['http://dmoztools.net']
    start_urls = ['http://dmoztools.net/Computers/Programming/Languages/Python/Books',
                  'http://dmoztools.net/Computers/Programming/Languages/Python/Resources']

    def parse(self, response):
        filename = response.url.split('/')[-2] + ".html"
        with open(filename, 'wb') as fp:
            fp.write(response.body)
