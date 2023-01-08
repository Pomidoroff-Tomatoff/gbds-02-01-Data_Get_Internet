# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksScrapyItem(scrapy.Item):
    ''' структура данных для паучка
        b_tmp.py
    '''
    # define the fields for your item here like:
    _id = scrapy.Field()  # key-поле для MongoDB, требуется его задать...
    title = scrapy.Field()


class Books_BooksScrapyItem(scrapy.Item):
    ''' структура данных для паучка
        books.py
        -- только пробежка по краткому списку книг, внутрь каждой книги не проваливаемся.
    '''
    _id = scrapy.Field()  # key-поле для MongoDB, требуется его задать...
    title = scrapy.Field()
    image = scrapy.Field()
    price = scrapy.Field()
    instock = scrapy.Field()


class Books_Pages_BooksScrapyItem(scrapy.Item):
    ''' Структура данных для паучков:
        -- books_pages.py
        -- pages.py
        Проваливаемся внутрь каждой книги!
    '''
    _id = scrapy.Field()  # key-поле для MongoDB, требуется его задать...
    title = scrapy.Field()
    image = scrapy.Field()
    price = scrapy.Field()
    in_stock = scrapy.Field()
    product_description  = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_exclude_tax = scrapy.Field()
    price_include_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    number_of_reviews = scrapy.Field()
