import scrapy
import os
from scrapy import Request

class WalmartSpider(scrapy.Spider):
    name = 'walmart'
    allowed_domains = ['www.walmart.com']
    start_urls = ['https://www.walmart.com/search/?query=Food&cat_id=976759&grid=true&redirect=false']
    custom_settings = {
            'FEED_URI': 'walmart.csv',
            }    

    if os.path.isfile('walmart.csv'): 
        os.remove('walmart.csv')

    def parse(self, response):
        self.page_number = 1
        print("======================================================================================================================================================")
        print(f"Getting response from {response.url}")
        print("======================================================================================================================================================")
        titles = response.css('a.truncate-title > span ::text').extract()
        ratings = response.css('span.stars-reviews-count > span:nth-of-type(1) ::text').extract()
        ratings = [rating.strip() for rating in ratings]
        prices = response.css('span.price > span.visuallyhidden ::text').extract()
        prices = [price.replace("$","") for price in prices]
        urls = response.css('a.product-title-link ::attr(href)').extract()

        for item in zip(titles,ratings,prices,urls):
            scraped_data = {
                    'title': item[0],
                    'number of ratings': item[1],
                    'price': item[2],
                    'url': item[3]
                    }
            yield scraped_data 
        
        if self.page_number < 10:
           self.page_number += 1
           pagination_url = f"http://search//?query=Food&amp;page={self.page_number}&amp;cat_id=976759&amp;grid=true&amp;redirect=false&amp;ps=40"
           yield Request(url=pagination_url, callback=self.parse)

        side_urls = response.css('div.sidebar-container a::attr(href)').extract() 
        for url in side_urls:
            abs_url = f"https://www.walmart.com/search/{url}" 
            yield Request(url=abs_url, callback=self.parse)


