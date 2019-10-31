# -*- coding: utf-8 -*-
import scrapy


class YlpSpider(scrapy.Spider):
    name = 'ylp'
    allowed_domains = ['yellowpages.com']
    start_urls = ['https://www.yellowpages.com/search?search_terms=hot+tubs+and+spas&geo_location_terms=ID/']


    def parse(self, response):
        companies = response.xpath('//*[@class="info"]')

        for company in companies:
            name = company.xpath('h2/a[@class="business-name"]/span/text()').extract_first()
            streetaddress = company.xpath('div/p[@class="adr"]/span[@class="street-address"]/text()').extract()
            city = company.xpath('div/p[@class="adr"]/span[@class="locality"]/text()').extract()
            state = company.xpath('div/p[@class="adr"]/span[3]/text()').extract()
            zipcode = company.xpath('div/p[@class="adr"]/span[4]/text()').extract()
            phone = company.xpath('div/div[@class="phones phone primary"]/text()').extract_first()
            
            website = company.xpath('div/div[@class ="links"]/a/@href').extract_first()

            yield {'City': city, 'Name': name, 'address': streetaddress, 'City': city, 'State': state, 'Zipcode': zipcode, 'Phone': phone, 'Website': website}

            NEXT_PAGE_SELECTOR = 'a.next ::attr(href)'
            next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
            if next_page:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse
                )
