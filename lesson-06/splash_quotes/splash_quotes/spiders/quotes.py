import scrapy

from scrapy_splash import SplashRequest


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    # start_urls = ['http://quotes.toscrape.com/js']
    url = 'http://quotes.toscrape.com/js'

    custom_settings = {
        # LOG_LEVEL
        # https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-LOG_LEVEL
        # In list: CRITICAL, ERROR, WARNING, INFO, DEBUG
        'LOG_LEVEL': 'ERROR',

        # Configure item pipelines
        # See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
        'ITEM_PIPELINES': {
           'splash_quotes.pipelines.SplashQuotesPipeline': 300,
        },

        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },

        # Двойники:
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',

        # 'SPLASH_URL': 'http://localhost:8050',
        # 'SPLASH_URL': 'http://127.0.0.1:8050/run',
        # Если задан домен с сервером splash, то порт указывать не надо, так как он задан по умолчанию на данном сервере
        'SPLASH_URL': 'https://s1.onekkk.com/',

        # Описание других параметров:
        # https://pypi.python.org/pypi/scrapy-splash
    }

    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            splash.resource_timeout = 10.0
            splash: set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36")
            assert(splash:go(args.url))
            assert(splash:wait(1))
            return splash:html()
        end
    '''   # https://splash.readthedocs.io/en/stable/scripting-ref.html

    def start_requests(self):
        ''' Используется вместо переменной start_url
            для генерации или пред-обработки ссылок
        '''
        yield SplashRequest(
            url=self.url,                     # Сайт, который нужно рендерить
            endpoint='execute',               # Выполнить скрипт
            callback=self.parse,              # После выполнения скрипта ответ передать ф. self.parse
            args={'lua_source': self.script}  # Скрипт для выполнения
        )

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        print(f"PARS, QUOTES = {len(quotes)}, url = {response.url}")
        for quote in quotes:
            yield {
                'author': quote.xpath('.//small[@class="author"]/text()').get(),
                'quote':  quote.xpath('.//span[@class="text"]/text()').get(),
            }
