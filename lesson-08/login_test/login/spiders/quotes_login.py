''' Формы со скрытыми данным
    -- обычная форма,
    -- но имеющая где-то на странице скрытый тэг с уникальным значением текущего сеанса,
       значение которого необходимо так же передать вместе с заполненной формой
    https://docs.scrapy.org/en/latest/topics/request-response.html#request-usage-examples
'''

import scrapy


class QuotesLoginSpider(scrapy.Spider):
    name = 'quotes_login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/login']

    custom_settings = {
        # LOG_LEVEL In list: CRITICAL, ERROR, WARNING, INFO, DEBUG (https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-LOG_LEVEL)
        'LOG_LEVEL': 'ERROR',

        # Обязательно включить для этого сайта (True)
        'COOKIES_ENABLED': True,
        }

    def parse(self, response):
        csrf_token = response.xpath('//input[@name="csrf_token"]/@value').get()
        username = 'admin'
        password = 'admin'
        print(f"Работа с формой, заполняем и отправляем:\n  {csrf_token=}\n  {username=}\n  {password=}\n  {response.url=}")

        form = scrapy.FormRequest.from_response(
            response,                       # ссылка для отправки запроса
            formxpath='//form',             # адрес объекта-формы на странице по xpath
            formdata={
                'csrf_token': csrf_token,
                'username': username,       # адрес поля с именем и его значение
                'password': password,       # адрес поля с паролем и его значение
            },
            # clickdata={'type': 'submit'},
            callback=self.after_login
        )
        yield form
        return None

    def after_login(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        print(f"Результат входа на сайт:\n  {response.url=} \n  найдено цитат {len(quotes)=}")
        return None
