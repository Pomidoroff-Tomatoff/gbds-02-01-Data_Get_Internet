''' GB BigData / Олег Гладкий (https://gb.ru/users/3837199) // Parsing/Lesson-08
    Работа с формой:
        > Логинимся на учебном сайте scrapethissite.com
        > находим и используем токен csrf_token
        > Используем Scrapy Splash (для обычного сайта)
'''

import scrapy
from scrapy import FormRequest
from scrapy_splash import SplashFormRequest, SplashRequest


class SandboxCsrfJavascriptSpider(scrapy.Spider):
    name = 'sandbox_csrf_javascript'
    allowed_domains = ['scrapethissite.com']
    start_url = 'https://www.scrapethissite.com/pages/advanced/?gotcha=csrf'

    custom_settings = {
        # LOG_LEVEL In list: CRITICAL, ERROR, WARNING, INFO, DEBUG (https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-LOG_LEVEL)
        'LOG_LEVEL': 'ERROR',
        # Важно, для этого сайта (True)
        'COOKIES_ENABLED': True,
        # Set settings whose default value is deprecated to a future-proof value
        'TWISTED_REACTOR': 'twisted.internet.selectreactor.SelectReactor',
        # SPLASH
        # Описание параметров Splash:
        # https://pypi.python.org/pypi/scrapy-splash
        # 'SPLASH_URL': 'http://localhost:8050',
        # 'SPLASH_URL': 'http://127.0.0.1:8050/run',
        'SPLASH_URL': 'https://s1.onekkk.com/',
        # Двойники: (недаюсь, что понимаю)
        # Класс, используемый для обнаружения и фильтрации повторяющихся запросов.
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        # Класс, реализующий серверную часть хранилища кэша.
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
        'SPIDER_MIDDLEWARES': {
            # 'login.middlewares.LoginSpiderMiddleware': 543,
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,},
        'DOWNLOADER_MIDDLEWARES': {
            # 'login.middlewares.LoginDownloaderMiddleware': 543,
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,},
    }

    script = '''
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return {
                html = splash:html(),
            }
        end
    '''   # https://splash.readthedocs.io/en/stable/scripting-ref.html

    def start_requests(self):
        print(f"Scrapy + Splash-plugin: Login on {self.start_url}")
        request = SplashRequest(
            url=self.start_url,
            endpoint='execute',
            args={'lua_source': self.script},
            callback=self.parse)
        yield request
        return None

    def parse(self, response):
        csrf_token = response.xpath('//form//input[@name="csrf"]/@value').get()
        username = 'admin'
        password = 'admin'
        print(f"Работа с формой, заполняем и отправляем:\n  {csrf_token=}\n  {username=}\n  {password=}\n  {response.url=}")

        form = SplashFormRequest.from_response(
            response,                       # ссылка для отправки запроса
            formxpath='//form',             # адрес объекта-формы на странице по xpath
            formdata={
                'csrf': csrf_token,
                'user': username,       # адрес поля с именем и значение
                'pass': password,       # адрес поля с паролем и значение
            },
            args={
                'lua_source': self.script,
                'endpoint': 'execute',
                'wait': 1,
            },
            callback=self.after_login
        )
        yield form
        return None

    def after_login(self, response):
        message = response.xpath('//div[@class="col-md-4 col-md-offset-4"]/text()').get().strip()
        print(f"Результат входа на сайт:\n  {response.url=} \n  {message=}")
        return None
