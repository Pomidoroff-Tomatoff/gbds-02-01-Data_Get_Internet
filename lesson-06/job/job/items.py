# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    ''' Класс Item по умолчанию '''
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HhList_JobItem(scrapy.Item):
    collection_name = 'vacancies_list'   # имя таблицы, не является полем
    _id = scrapy.Field()                 # key-поле для MongoDB, обязательное.
    title = scrapy.Field()
    employer = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    salary_cur = scrapy.Field()
    # date_publication = scrapy.Field()  # отсутствует в кратком списке
    link = scrapy.Field()
    pass


class HhPages_JobItem(scrapy.Item):
    collection_name = 'vacancies'        # имя таблицы, не является полем
    _id = scrapy.Field()                 # key-поле для MongoDB, обязательное.
    title = scrapy.Field()
    employer = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    salary_cur = scrapy.Field()
    date_publication = scrapy.Field()    # date_publication = scrapy.Field(serializer=str)  -- НЕ РАБОТАЕТ!!!
    link = scrapy.Field()
    pass
