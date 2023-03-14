''' GB BigData / Олег Гладкий (https://gb.ru/users/3837199) // Parsing/Lesson-08
    API: тестирование технологии на учебном сайте с цитатами (quotes.toscrape.com)
'''
import scrapy
import json


class QuotesApiSpider(scrapy.Spider):
    name = 'quotes_api'
    allowed_domains = ['quotes.toscrape.com']
    start_url = 'https://quotes.toscrape.com/api/quotes'

    custom_settings = {
        'LOG_LEVEL': 'ERROR',    # LOG_LEVEL In list: CRITICAL, ERROR, WARNING, INFO, DEBUG (https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-LOG_LEVEL)
        'COOKIES_ENABLED': True,
        'ROBOTSTXT_OBEY': False,
        'TWISTED_REACTOR': 'twisted.internet.selectreactor.SelectReactor'  # Для запускали runner
    }

    def start_requests(self):
        ''' Не обязательный метод, можно обойтись стартовой ссылкой.
            Но всё же отработаем здесь этот подход
        '''
        page = 1  # Внимание, считать начинаем с 1-цы, а не нуля!
        request = scrapy.Request(
            url = self.start_url + f'?page={page}',
            callback = self.parse, )
        yield request
        return None

    def parse(self, response, **kwargs):
        json_response = json.loads(response.body)       # Получаем JSON из ответа
        quotes = json_response.get('quotes')
        for quote in quotes:
            item = {
                'author': quote.get('author').get('name'),
                'tag': quote.get('tags'),
                'quotes_text': quote.get('text'),
            }
            yield item

        print(f"Загружена страница: {json_response.get('page')}, флаг продолжения: {json_response.get('has_next')}")
        # Следующая страница
        if json_response.get('has_next'):
            page = json_response.get('page') + 1
            request = scrapy.Request(
                url = self.start_url + f'?page={page}',
                callback = self.parse,)
            yield request

        return None
