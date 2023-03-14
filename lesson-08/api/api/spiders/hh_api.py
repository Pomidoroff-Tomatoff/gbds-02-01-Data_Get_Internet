''' GB BigData / Олег Гладкий (https://gb.ru/users/3837199) // Parsing, https://gb.ru/lessons/262705/
    ДЗ-8: Scrapy API & Login

    API, быстрый старт:
        https://habr.com/ru/company/hh/blog/303168/
    hh API:
        https://github.com/hhru/api/blob/master/README.md#Ресурсы
    Дополнительно:
        https://temofeev.ru/info/articles/rabota-s-api-headhunter-pri-pomoshchi-python/

    Нехватает работы с параметрами API:
        -- их очень много
        -- можно-ли добавлять вложенными словарями?
'''

import scrapy
from scrapy.http import HtmlResponse
from scrapy import Request
import json
import math                                       # округление в большую сторону
from w3lib.url import add_or_replace_parameters
from scrapy.loader import ItemLoader
from itemloaders.processors import SelectJmes
import logging  # журналирование
from api.items import HhApiItem  # пользовательский класс с полями item...


class HhApiSpider(scrapy.Spider):
    name = 'hh_api'
    allowed_domains = ['api.hh.ru']
    start_url = 'https://api.hh.ru/vacancies'
    # jornal = logging.getLogger(__name__)  # журнал

    custom_settings = {
        'USER_AGENT': 'api-test-agent',     # Объязательно для тестового доступа на hh или ничего не вернётся!
        'LOG_LEVEL': 'WARNING',             # LOG_LEVEL In list: CRITICAL, ERROR, WARNING, INFO, DEBUG (https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-LOG_LEVEL)
        'FEED_EXPORT_ENCODING': 'UTF-8',    # Unicode
        'COOKIES_ENABLED': True,
        'ROBOTSTXT_OBEY': False,
        'TWISTED_REACTOR': 'twisted.internet.selectreactor.SelectReactor',  # Для запуска паука приложением Питона runner_hh_api.py
    }

    def __init__(self, *args, **kwargs):
        super(HhApiSpider, self).__init__(*args, **kwargs)

        self.keyword = "JavaScript"  # Ключевое слово поиска по умолчанию

        if args:
            self.args = args
        if kwargs:
            self.kwargs = kwargs
            for key, value in kwargs.items():
                if key.upper() == "keyword".upper():
                    self.keyword = value
                    break

        # Параметры запроса паука
        self.logger.warning(f"Ключевое слово поиска: {self.keyword=}")
        self.params = {
            'area': 1,
            'clusters': 'true',
            'enable_snippets': 'true',
            'per_page': 20,
            'page': 0,
            'ored_clusters': 'true',
            'search_field': 'description',
            'text': self.keyword,
            'order_by': 'publication_time',
            'hhtmFrom': 'vacancy_search_list',
            'customDomain': 1,
        }  # хорошо бы с этим разобраться...

    def start_requests(self):
        request = Request(
            url=add_or_replace_parameters(self.start_url, self.params),
            callback=self.parse)
        yield request

    def parse(self, response: HtmlResponse, **kwargs):
        json_response = json.loads(response.body)

        # Отправляем в очередь следующий запрос асинхронному загрузчику...
        pages = json_response.get('pages')     # всего страниц
        page = json_response.get('page')       # текущая страница полученного ответа
        next_page = page + 1                   # следующая (+1) страница
        if next_page < pages:
            self.params['page'] = next_page
            request = Request(
                url=add_or_replace_parameters(self.start_url, self.params),
                callback=self.parse)
            yield request

        # Анализ ответа
        self.logger.warning(f"СТРАНИЦА {page=}, {pages=}")
        items = json_response.get('items')    # список позиций
        for item in items:
            yield self.parse_item(item)       # отправляем по конвейеру в pipeline.py
        return None

    def parse_item(self, json_selector):
        ''' Непосредственный захват данных
            и передача их для очистки в items.py и далее по конвейеру... '''
        il = ItemLoader(item=HhApiItem(), selector=json_selector)
        il.add_value('_id', SelectJmes('id')(json_selector))
        il.add_value('name', SelectJmes('name')(json_selector))
        il.add_value('employer_id', SelectJmes('employer.["id"]')(json_selector))
        il.add_value('employer_name', SelectJmes('employer.["name"]')(json_selector))
        il.add_value('salary_min', SelectJmes('salary.["from"]')(json_selector))
        il.add_value('salary_max', SelectJmes('salary.["to"]')(json_selector))
        il.add_value('salary_cur', SelectJmes('salary.["currency"]')(json_selector))
        il.add_value('date_publication', SelectJmes('published_at')(json_selector))
        il.add_value('employer_id', SelectJmes('employer.["id"]')(json_selector))
        il.add_value('employer_name', SelectJmes('employer.["name"]')(json_selector))
        il.add_value('employer_url', SelectJmes('employer.["alternate_url"]')(json_selector))
        il.add_value('url', SelectJmes('alternate_url')(json_selector))

        return il.load_item()

    pass  # (end) HhApiSpider -- class
