import scrapy


class QuotesJavascriptSpider(scrapy.Spider):
    name = 'quotes_javascript'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        pass
