# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst, Compose, Identity
import datetime


class ApiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HhApiItem(scrapy.Item):
    collection_name = 'vacancies_api'

    _id = scrapy.Field(
        input_processor=MapCompose(lambda v: int(v)),
        output_processor=TakeFirst()
    )
    name = scrapy.Field(
        input_processor=MapCompose(str),
        output_processor=Join(' ')
    )
    employer_id = scrapy.Field(
        input_processor=Compose(),
        output_processor=TakeFirst()
    )
    employer_name = scrapy.Field(
        input_processor=Compose(),
        output_processor=TakeFirst()
    )
    employer_url = scrapy.Field(
        input_processor=Compose(),
        output_processor=TakeFirst()
    )
    salary_min = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    salary_max = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    salary_cur = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
    date_publication = scrapy.Field(
        input_processor=MapCompose(),  # lambda t: datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%S%z")),
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        input_processor=MapCompose(),
        output_processor=TakeFirst()
    )
