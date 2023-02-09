# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst


def to_str(value):
    return str(value)


def key_vacancies(key_in: str = ""):
    if not key_in:
        return None  # проверка
    else:
        return int(key_in.split('/vacancy/')[1])


class JobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HhList_itemloader_JobItem(scrapy.Item):
    collection_name = 'vacancies_list_itemloader'  # имя таблицы, не является полем
    # key-поле для MongoDB, обязательное.
    _id = scrapy.Field(
        output_processor=TakeFirst()
    )
    title = scrapy.Field()
    employer = scrapy.Field(
        output_processor=TakeFirst()
    )
    # link = scrapy.Field()
    pass


class HhList_JobItem(scrapy.Item):
    collection_name = 'vacancies_list'  # имя таблицы, не является полем
    # key-поле для MongoDB, обязательное.
    _id = scrapy.Field()
    title = scrapy.Field()
    employer = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    salary_cur = scrapy.Field()
    # date_publication = scrapy.Field()  # отсутствует в кратком списке
    link = scrapy.Field()
    pass


class HhPages_JobItem(scrapy.Item):
    collection_name = 'vacancies'   # имя таблицы, не является полем
    _id = scrapy.Field()  # key-поле для MongoDB, обязательное.
    title = scrapy.Field()
    employer = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    salary_cur = scrapy.Field()
    # date_publication = scrapy.Field(serializer=str)  -- НЕ РАБОТАЕТ!!!
    # date_publication = scrapy.Field(input_processor=MapCompose(to_str)) -- НЕ РАБОТАЕТ!!!
    date_publication = scrapy.Field()
    link = scrapy.Field()
    pass
