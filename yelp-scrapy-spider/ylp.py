# -*- coding: utf-8 -*-

import scrapy
#from urllib.parse import urljoin

class ProductsSpider(scrapy.Spider):
    name = "ylp"
    start_urls = [
        'https://www.yelp.ca/search?find_desc=Hot+Tubs+and+Spas&find_loc=Calgary%2C+Alberta&ns=1',
    ]

    def parse(self, response):
        companies = response.css('li.regular-search-result')
        products = companies.css("a.biz-name.js-analytics-click::attr(href)").extract()
        for p in products:
            url = response.urljoin(p)
            yield scrapy.Request(url, callback=self.parse_product)

            NEXT_PAGE_SELECTOR = 'a.next ::attr(href)'
            next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
            if next_page:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse
                )

    def parse_product(self, response):
        for info in response.css('div.content-container.js-biz-details'):
            yield {
                'product_name': info.css('h1.biz-page-title::text').extract_first(),
                'url': info.css('span.biz-website.js-add-url-tagging a::text').extract(),
                'address': info.css('strong.street-address address::text').extract_first(),
                'phone': info.css('li span.biz-phone::text').extract_first(),
            }
