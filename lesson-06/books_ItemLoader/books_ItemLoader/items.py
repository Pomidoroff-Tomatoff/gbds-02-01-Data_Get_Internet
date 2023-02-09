# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join, Compose


def txtup(value: str = None):
    '''All key make upper case. If in value is string.'''
    return value.upper() if isinstance(value, (str,)) else value


def txtlower(value: str = None):
    '''All key make lower case. If in value is string.'''
    return value.lower() if isinstance(value, (str,)) else value


class BooksItemloaderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(
        input_processor=MapCompose(txtup, txtlower, ),
        output_processor=TakeFirst()
    )
    pass
