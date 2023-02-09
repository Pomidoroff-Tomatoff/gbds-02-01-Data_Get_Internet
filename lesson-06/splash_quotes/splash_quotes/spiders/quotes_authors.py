import scrapy

from scrapy_splash import SplashRequest
from splash_quotes.items import Quote_SplashQuotesItem
from splash_quotes.items import Author_SplashQuotesItem


class QuotesAuthorsSpider(scrapy.Spider):
    name = 'quotes_authors'
    allowed_domains = ['quotes.toscrape.com']
    start_url = 'https://quotes.toscrape.com/'
    splash_mode = True

    custom_settings = {
        # LOG_LEVEL
        # https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-LOG_LEVEL
        # In list: CRITICAL, ERROR, WARNING, INFO, DEBUG
        'LOG_LEVEL': 'ERROR',

        # Configure item pipelines
        # See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
        # 'ITEM_PIPELINES': {
        #    'splash_quotes.pipelines.SplashQuotesPipeline': 300,
        #    'splash_quotes.pipelines.MongoDB_QuotesPipeline': 290,
        # },

        # 'SPLASH_URL': 'http://localhost:8050',
        # 'SPLASH_URL': 'http://127.0.0.1:8050/run',
        # Используем сервер в инете со Splash-ем, случайно найденный...
        # 'SPLASH_URL': 'https://s1.onekkk.com/',

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

    def get_rendering_request(self, url="", callback=None):
        if callback is not None:
            if self.splash_mode:
                return SplashRequest(
                    url=url,             # Сайт, который нужно рендерить
                    endpoint='execute',  # Выполнить скрипт
                    callback=callback,   # После выполнения скрипта ответ передать ф. self.parse()
                    args={'lua_source': self.script}  # Скрипт для выполнения
                )
            else:
                return scrapy.Request(url=url, callback=callback)
        else:
            logging.log(logging.CRITICAL, "*** ERROR callback=None")
            return None

    def start_requests(self):
        ''' 1-ый запрос request к начальному url '''
        yield self.get_rendering_request(url=self.start_url, callback=self.parse)

    def parse(self, response, **kwargs):
        quotes = response.xpath('//div[@class="quote"]')
        print(f"PARSE, QUOTES = {len(quotes)}, url = {response.url}")
        for quote in quotes:
            # цитата...
            yield self.parse_item(quote)
            # автор с его странички
            author_link_local = quote.xpath('.//small[@class="author"]/following-sibling::a[1]/@href').get()
            if author_link_local:
                link = response.urljoin(author_link_local)
                yield self.get_rendering_request(url=link, callback=self.parse_item_author)

        # следующая страница
        next_page_local = response.xpath('//nav/*/li[@class="next"]/a/@href').get()
        if next_page_local:
            next_page = response.urljoin(next_page_local)
            yield self.get_rendering_request(url=next_page, callback=self.parse)
        return

    def parse_item(self, quote):
        item = Quote_SplashQuotesItem(
            author=
                quote.xpath('.//small[@class="author"]/text()').get(),
            quote=
                quote.xpath('.//span[@class="text"]/text()').get(),
            tags=
                quote.xpath('.//a[@class="tag"]/text()').getall(),
        )
        return item  # это не генератор

    def parse_item_author(self, response):
        author_details = response.xpath('//div[@class="author-details"]')
        item = Author_SplashQuotesItem(
            author=
                author_details.xpath('.//*[@class="author-title"]/text()').get().strip(),
            born_date=
                author_details.xpath('.//*[@class="author-born-date"]/text()').get().strip(),
            born_location=
                author_details.xpath('.//*[@class="author-born-location"]/text()').get().lstrip('in').strip(),
            description=
                author_details.xpath('.//*[@class="author-description"]/text()').get().strip()
        )
        yield item
