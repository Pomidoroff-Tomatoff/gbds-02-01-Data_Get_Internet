''' GB BigData / Олег Гладкий (https://gb.ru/users/3837199) // Parsing/Lesson-08
    Работа с формой:
        > Логинимся на учебном сайте scrapethissite.com
        > находим и используем токен csrf_token
        > Стандартные средства Scrapy
'''

import scrapy
from scrapy import FormRequest


class SandboxCsrfSpider(scrapy.Spider):
    name = 'sandbox_csrf'
    allowed_domains = ['scrapethissite.com']
    start_urls = ['https://www.scrapethissite.com/pages/advanced/?gotcha=csrf']

    custom_settings = {
        # LOG_LEVEL In list: CRITICAL, ERROR, WARNING, INFO, DEBUG (https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-LOG_LEVEL)
        'LOG_LEVEL': 'ERROR',
        # Важно, для этого сайта (True)
        'COOKIES_ENABLED': True,
        # Set settings whose default value is deprecated to a future-proof value
        'TWISTED_REACTOR': 'twisted.internet.selectreactor.SelectReactor'
    }

    def parse(self, response):
        csrf_token = response.xpath('//form//input[@name="csrf"]/@value').get()
        username = 'admin'
        password = 'admin'
        print(f"Работа с формой, заполняем и отправляем:\n  {csrf_token=}\n  {username=}\n  {password=}\n  {response.url=}")

        form = FormRequest.from_response(
            response,                       # ссылка для отправки запроса
            formxpath='//form',             # адрес объекта-формы на странице по xpath
            formdata={
                'csrf': csrf_token,
                'user': username,       # адрес поля с именем и значение
                'pass': password,       # адрес поля с паролем и значение
            },
            callback=self.after_login
        )
        yield form
        return None

    def after_login(self, response):
        message = response.xpath('//div[@class="col-md-4 col-md-offset-4"]/text()').get().strip()
        print(f"Результат входа на сайт:\n  {response.url=} \n  {message=}")
        return None
