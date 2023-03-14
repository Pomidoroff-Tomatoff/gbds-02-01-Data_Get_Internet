''' GB BigData / Олег Гладкий (https://gb.ru/users/3837199) // Parsing/Lesson-08
    API: тестирование технологии на учебном сайте с цитатами (quotes.toscrape.com)
    Внимание, ошибка:
        -- метод start_request() используется здесь как именно генератор запросов,
           ведущий весь процесс этих запросов,
        -- при этом информацию о существовании текущей страниц, которую следует загрузить
           этот метод (start_request()) получает от отложенных сообщений непосредственного
           анализа обрабатываемых параллельно загруженных страниц.
        -- ошибка в том, что парсинг выполняется параллельно и с большой задержкой
           от непосредственной очереди загрузки страниц на столько,
           так что когда становиться ясно, что все возможные страницы уже загружены,
           загрузчик тем не менее пытается загружить множество следующих несуществующих страниц
        -- Спасением оказывается отрицательный ответ сервера на запрошенные несуществующие страницы.
'''
import scrapy
import json


class QuotesApiErrorSpider(scrapy.Spider):
    name = 'quotes_api_error'
    allowed_domains = ['quotes.toscrape.com']
    page_flag = True  # флаг о существовании страницы

    custom_settings = {
        'LOG_LEVEL': 'ERROR',    # LOG_LEVEL In list: CRITICAL, ERROR, WARNING, INFO, DEBUG (https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-LOG_LEVEL)
        'COOKIES_ENABLED': True,
        'ROBOTSTXT_OBEY': False,
        'TWISTED_REACTOR': 'twisted.internet.selectreactor.SelectReactor'  # Для запускали runner
    }

    def start_requests(self):
        url = 'https://quotes.toscrape.com/api/quotes'
        page = 0
        while self.page_flag and (page := page + 1) < 100:
            print(f"{page=}")
            request = scrapy.Request(
                url = url + f'?page={page}',
                callback = self.parse,
            )
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

        self.page_flag = json_response.get('has_next')  # ЗАПОЗДАЛО выставляем флаг о существовании следующей страницы
        print(f"Обработанная страница: {json_response.get('page')}, флаг продолжения: {self.page_flag}")
        return None
