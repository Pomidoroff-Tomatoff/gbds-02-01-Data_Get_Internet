import scrapy
import logging

from scrapy_splash import SplashRequest
from splash_quotes.items import Author_SplashQuotesItem


class AuthorSpider(scrapy.Spider):
    name = 'author'
    allowed_domains = ['quotes.toscrape.com']
    start_url = 'https://quotes.toscrape.com/'
    splash_mode = True

    script = '''
            function main(splash, args)
                splash.private_mode_enabled = false
                splash.resource_timeout = 10.0
                splash: set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36")
                assert(splash:go(args.url))
                assert(splash:wait(1))
                return splash:html()
            end
        '''  # https://splash.readthedocs.io/en/stable/scripting-ref.html

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
        yield self.get_rendering_request(url=self.start_url, callback=self.parse)

    def parse(self, response, **kwargs):
        quotes = response.xpath('//div[@class="quote"]')
        print(f"PARSE, QUOTES = {len(quotes)}, url = {response.url}")
        for quote in quotes:
            # нырок на страничку автора
            link_local = quote.xpath('.//small[@class="author"]/following-sibling::a[1]/@href').get()
            if link_local:
                link = response.urljoin(link_local)
                yield self.get_rendering_request(url=link, callback=self.parse_item)

        next_page_local = response.xpath('//nav/*/li[@class="next"]/a/@href').get()
        if next_page_local:
            next_page = response.urljoin(next_page_local)
            yield self.get_rendering_request(url=next_page, callback=self.parse) 

    def parse_item(self, response):
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
