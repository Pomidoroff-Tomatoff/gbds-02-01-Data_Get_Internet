# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HhList_JobItem(scrapy.Item):
    collection_name = 'vacancies_list'  # имя таблицы, не является полем
    _id = scrapy.Field()  # key-поле для MongoDB, обязательное.
    title = scrapy.Field()
    link = scrapy.Field()
    vacancy_id = scrapy.Field()
    employer = scrapy.Field()
    salary = scrapy.Field()
    # date_publication = scrapy.Field()  # отсутствует в кратком списке
    pass


class HhPages_JobItem(scrapy.Item):
    collection_name = 'vacancies'  # имя таблицы, не является полем
    _id = scrapy.Field()  # key-поле для MongoDB, обязательное.
    title = scrapy.Field()
    link = scrapy.Field()
    vacancy_id = scrapy.Field()
    employer = scrapy.Field()
    salary = scrapy.Field()
    date_publication = scrapy.Field()
    pass
