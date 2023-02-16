''' GB BigData / Олег Гладкий (https://gb.ru/users/3837199) // Parsing/Lesson-08
    API: тестирование технологии на учебном сайте с цитатами (quotes.toscrape.com)
'''
import scrapy
import json


class QuotesApiSpider(scrapy.Spider):
    name = 'quotes_api'
    allowed_domains = ['quotes.toscrape.com']
    page_flag = True

    custom_settings = {
        # LOG_LEVEL In list: CRITICAL, ERROR, WARNING, INFO, DEBUG (https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-LOG_LEVEL)
        'LOG_LEVEL': 'ERROR',
        'COOKIES_ENABLED': True,
        'ROBOTSTXT_OBEY': False,
        # Set settings whose default value is deprecated to a future-proof value
        'TWISTED_REACTOR': 'twisted.internet.selectreactor.SelectReactor'
    }

    def start_requests(self):
        url = 'https://quotes.toscrape.com/api/quotes'
        page = 0
        while self.page_flag and (page := page + 1) < 100:
            request = scrapy.Request(
                url = url + f'?page={page}',
                callback = self.parse,
            )
            yield request

        return None

    def parse(self, response):
        resp_json = json.loads(response.body)       # Получаем JSON из ответа
        quotes = resp_json.get('quotes')
        for quote in quotes:
            item = {
                'author': quote.get('author').get('name'),
                'tag': quote.get('tags'),
                'quotes_text': quote.get('text'),
            }
            yield item

        self.page_flag = resp_json.get('has_next')  # Следующая страница существует?
        return None
