''' Новая технология в item.py, но по старинке в методе parse()
    Это приводит к ошибкам: разбираем их.
'''

import scrapy
from books_ItemLoader.items import BooksItemloaderItem


class BooksErrSpider(scrapy.Spider):
    name = 'books_err'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):

        #  00-1. Старая технология:
        # -- не работает с новым item.py
        # -- потому что ItemLoader в пауке не объявлен

        item = BooksItemloaderItem()
        item(title=response.xpath('//div[@class="col-sm-8 h1"]/a/text()'))
        yield item
        # #-> TypeError: 'BooksItemloaderItem' object is not callable

        # 00-2. Старая технология с объявлением класса (d : работает частично
        # -- объявляем класс с загрузчиком item.py
        # -- процессоры item.py не задействуются!

        item = {'title': response.xpath('//div[@class="col-sm-8 h1"]/a/text()')}
        yield item
        # #-> pipeline: 00000 item={'title': [<Selector xpath='//div[@class="col-sm-8 h1"]/a/text()' data='Books to Scrape'>]}