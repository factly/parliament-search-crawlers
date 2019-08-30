import scrapy
import json
import logging
# logging.getLogger('scrapy').setLevel(logging.WARNING)


class QuotesSpider(scrapy.Spider):

    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, resp):
        self.log("I just visited " + resp.url)
        # with open("../files/data.json", 'w') as outfile:
        for quote in resp.css('div.quote'):
            item = {
                'authors': quote.css('small.author::text').extract(),
                'quotes': quote.css('span.text::text').extract(),
                'tags': quote.css('a.tag::text').extract()
            }
            yield item

        next_page_url = resp.css('li.next > a::attr(href)').extract_first()
        next_page_url = resp.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)
