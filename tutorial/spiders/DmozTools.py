# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TutorialItem


class DmoztoolsSpider(scrapy.Spider):
    name = 'DmoztoolsSpider'
    allowed_domains = ['http://dmoztools.net']
    start_urls = ['http://dmoztools.net/Computers/Programming/Languages/Python/Books',
                  'http://dmoztools.net/Computers/Programming/Languages/Python/Resources']

    def parse(self, response):
        # filename = response.url.split('/')[-2] + ".html"
        # with open(filename, 'wb') as fp:
        #     fp.write(response.body)
        div_site_item = response.xpath("//*[@id='site-list-content']/div/div[@class='title-and-desc']")
        for site_item in div_site_item:
            item = TutorialItem()
            item['title'] = site_item.css('div.site-title::text')
            # item['desc'] = site_item.css('div.site-descr::text')
            item['desc'] = site_item.xpath(".//div[@class ='site-descr']/text()").extract_first()
            item['link'] = site_item.css('a::attr(href)')
            yield item
