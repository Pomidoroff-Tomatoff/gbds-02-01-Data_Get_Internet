''' GB BigData / Олег Гладкий (https://gb.ru/users/3837199) // домашнее задание
    Запуск паука непосредственно из модуля Python-а (а не shell-командой "scrapy crawl...").
    Цели и задачи подхода:
        -- отладки кода
        -- передача аргументов
        -- может быть запуск нескольких пауков параллельно?...
    Технология:
        CrawlerRunner + reactor + defer

    https://docs.huihoo.com/scrapy/1.0/topics/practices.html#run-from-script
'''

from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from twisted.internet import task
from twisted.internet import reactor, defer
from threading import Thread
import time

# Паук:
from books_kwargs.spiders.books import BooksSpider


if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(BooksSpider, "MyBooks_NewSpiderName", categories='Travel,Classics', key2='toscrape.com')
        # yield runner.crawl(MySpider2)
        reactor.stop()

    crawl()
    reactor.run()

    print(f"---\nПаук завершил свою работу")
    print(f"Stop of reactor")
