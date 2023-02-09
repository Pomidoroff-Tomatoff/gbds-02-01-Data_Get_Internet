''' GB BigData / Олег Гладкий (https://gb.ru/users/3837199) // домашнее задание
    Исследования:
    -- технологии ItemLoader
'''

import scrapy
from scrapy.loader import ItemLoader
from parsel import Selector
from books_ItemLoader.items import BooksItemloaderItem  # Внимание: в названии папки исп. заглавные буквы!


class BooksSpider(scrapy.Spider):
    name = 'books'  # Это имя можно изменить из runner-а первым *args-параметром
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']
    icount: int = 0

    def parse(self, response):

        # 01/Новая технология: response

        iloader = ItemLoader(item=BooksItemloaderItem(), response=response)
        iloader.add_xpath('title', '//div[@class="col-sm-8 h1"]/a/text()')
        item = iloader.load_item()
        yield item

        # 02/Новая технология: selector
        # -- Используем цикл for
        #    для предварительно набранного списка селекторов

        books = response.css("article.product_pod")
        for book in books:
            self.icount += 1
            print(f"books.parse:{self.icount:05d}", end=" ")
            iloader = ItemLoader(item=BooksItemloaderItem(), selector=book)
            iloader.add_xpath('title', './/h3/a/@title')
            item = iloader.load_item()
            yield item

        # Следующая страница (краткого списка книг): здесь будет вызываться повторно код "01/response"

        return None  # end of parse()


