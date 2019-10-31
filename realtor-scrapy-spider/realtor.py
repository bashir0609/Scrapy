# -*- coding: utf-8 -*-
import scrapy


class RealSpider(scrapy.Spider):
    name = 'real'
    allowed_domains = ['realtor.com']
    start_urls = ['https://www.realtor.com/realestateagents/orlando_fl']

    def parse(self, response):
        companies = response.css('div.agent-list-card-title-text')
        products = companies.xpath('//div[@itemprop="name"]/a/@href').extract()
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
        for info in response.css('div.modal-body'):
            yield {
                'name': info.xpath('//p[@itemprop="name"]/text()').extract_first(),
                'url': info.xpath('//a[@itemprop="url"]/@href').extract_first(),
                'address': info.xpath('//span[@itemprop="streetAddress"]/text()').extract(),
                'phone': info.xpath('//span[@itemprop="telephone"]/text()').extract_first().strip(),
            }
