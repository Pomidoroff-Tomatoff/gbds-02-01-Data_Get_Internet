# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst, Compose, Identity
import datetime  # для того, чтобы иметь возможность преобразовать тип date к строке???

# import lib.job as job  # Библиотека для парсера
# from job.lib.job_lib import join_clear, get_maney
# , get_maney   # Библиотека для парсера
# Библиотека для парсера

from job.lib.join_clear import join_clear as join_clear
from job.lib.get_money import get_money as get_money
from job.lib.duplicate_remover import duplicate_remover as duplicate_remover


# Глобальные переменные модуля
KEY_VACANCIES_ID = 0
MONEY_ID = 0
MONEY_MIN = 0
MONEY_MAX = 0
MONEY_CUR = '0'


def key_vacancies(key_in: str = ""):
    ''' ID вакансии из url на hh.ru'''
    global KEY_VACANCIES_ID

    if not key_in: return None  # проверка

    if 'applicant' in key_in:
        _id = key_in.split('vacancyId=')[1].split('&')[0]
    else:
        _id = key_in.split('?')[0].split('/vacancy/')[1]

    if _id.isdigit():
        _id = int(_id)
    else:
        print(f"ОШИБКА: {_id=} не является числом, перевести в целые не получиться.")

    KEY_VACANCIES_ID = _id
    return _id

def link_vacancies(value):
    ''' Формируем ссылку по _id вакансии, сохранённой в глобальной переменной
        Так как _id вакансии объязательно присутствует для каждой итерации (иначе данные не занесуться),
        то можно не волноваться, что по ошибке мы получим значение _id из какой-либо предыдущей итерации...
    '''
    global KEY_VACANCIES_ID
    return 'https://hh.ru/vacancy/' + str(KEY_VACANCIES_ID)


def get_money_min(value):
    ''' Разбор данных и получение всех значений зарплаты.
        Запоминаем _ID, для которых эти значения имеют смысл. '''
    global KEY_VACANCIES_ID, MONEY_ID, MONEY_MIN, MONEY_MAX, MONEY_CUR
    salary = get_money(join_clear(value))
    MONEY_ID = KEY_VACANCIES_ID
    MONEY_MIN = salary['min']
    MONEY_MAX = salary['max']
    MONEY_CUR = salary['cur']
    return MONEY_MIN


def get_money_max(value):
    ''' Возврат ранее сохранённой МАКС зарплаты в глобальных переменных.
        Учитываем _ID, для которого значение макс-зарплаты актуально. '''
    global KEY_VACANCIES_ID, MONEY_ID, MONEY_MIN, MONEY_MAX, MONEY_CUR
    if MONEY_ID != KEY_VACANCIES_ID:
        return 0
    return MONEY_MAX


def get_money_cur(value):
    ''' Возврат ранее сохранённой ВАЛЮТЫ зарплаты в глобальных переменных.
        Учитываем _ID, для которого значение валюты зарплаты актуально. '''
    global KEY_VACANCIES_ID, MONEY_ID, MONEY_MIN, MONEY_MAX, MONEY_CUR
    if MONEY_ID != KEY_VACANCIES_ID:
        return ""
    return MONEY_CUR


class JobItem(scrapy.Item):
    ''' Класс Item по умолчанию '''
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HhList_itemloader_JobItem(scrapy.Item):
    collection_name = 'vacancies_list_itemloader'  # имя таблицы, не является полем
    # Внимание! Порядок обработки полей важен: _id должно быть первым и так далее...
    # key-поле _id для MongoDB, обязательное.
    _id = scrapy.Field(
        input_processor=MapCompose(key_vacancies),
        output_processor=TakeFirst()
    )
    title = scrapy.Field(
        input_processor=MapCompose(join_clear),
        output_processor=TakeFirst()
    )
    employer = scrapy.Field(
        input_processor=Compose(join_clear),  # Join(),
        output_processor=TakeFirst()
    )
    salary_min = scrapy.Field(
        input_processor=Compose(get_money_min),
        output_processor=TakeFirst()
    )
    salary_max = scrapy.Field(
        input_processor=Compose(get_money_max),
        output_processor=TakeFirst()
    )
    salary_cur = scrapy.Field(
        input_processor=Compose(get_money_cur),
        output_processor=TakeFirst()
    )
    link = scrapy.Field(
        input_processor=Compose(link_vacancies),
        output_processor=TakeFirst()
    )
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
