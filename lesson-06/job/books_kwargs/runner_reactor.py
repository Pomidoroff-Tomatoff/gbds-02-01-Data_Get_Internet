''' GB BigData / Олег Гладкий (https://gb.ru/users/3837199) // домашнее задание
    Запуск паука непосредственно из модуля Python-а (а не shell-командой "scrapy crawl...").
    Цели и задачи подхода:
        -- отладки кода
        -- передача аргументов
        -- может быть запуск нескольких пауков параллельно?...
    Технология:
        CrawlerRunner + reactor
    ВНИМАНИЕ:
        settings.py, необходимо отключить строку, вкл. по умолчанию (конец файла)
            # Set settings whose default value is deprecated to a future-proof value
        err:  TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
            # или заменить её на (из подсказки ошибки)
            TWISTED_REACTOR = 'twisted.internet.selectreactor.SelectReactor'
'''

from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from twisted.internet import task
from twisted.internet import reactor  # сам реактор, который и будет запускать паука
from threading import Thread
import time

# Паук:
from books_kwargs.spiders.books import BooksSpider


if __name__ == '__main__':
    # Параметры проекта

    configure_logging()
    settings = get_project_settings()

    # CrawlerRunner

    runner = CrawlerRunner(settings)

    # Параметры процесса в реакторе
    # -- Описание паука с указанием класса паука и его параметров
    # -- в рамках процесса может быть несколько пауков?
    # Внимание!
    #   Если указать обычный (неключевой) аргумент после класса паука,
    #   то этот неключевой аргумент переопределит имя паука, так как изменит атрибут name (паука) на это значение.
    #   То есть имя паука в атрибуте класса self.name изменится.

    deferred = runner.crawl(BooksSpider, "MyBooks_NewSpiderName", categories='Travel,Classics', key2='toscrape.com')
    # deferred = runner.join()
    deferred.addBoth(lambda _: reactor.stop())  # после завершения работы паука?

    # Запускаем реактор
    reactor.run()

    print(f"---\nПаук завершил свою работу\nРеактор остановлен")
