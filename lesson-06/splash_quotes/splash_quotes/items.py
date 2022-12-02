# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SplashQuotesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # _id = scrapy.Field()  # key-поле для MongoDB, требуется его иметь, значение задаётся самой монгой.
    pass


class Author_SplashQuotesItem(scrapy.Item):
    _id = scrapy.Field()  # key-поле для MongoDB, требуется его иметь, значение задаётся самой монгой.
    author = scrapy.Field()
    born_date = scrapy.Field()
    born_location = scrapy.Field()
    description = scrapy.Field()
    pass


class Quote_SplashQuotesItem(scrapy.Item):
    _id = scrapy.Field()  # key-поле для MongoDB, требуется его иметь, значение задаётся самой монгой.
    author = scrapy.Field()
    quote = scrapy.Field()
    tags = scrapy.Field()
    pass
