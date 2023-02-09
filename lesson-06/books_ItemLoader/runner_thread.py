''' GB BigData / Олег Гладкий (https://gb.ru/users/3837199) // домашнее задание
    Запуск паука непосредственно из модуля Python-а (а не shell-командой "scrapy crawl...").
    Цели и задачи подхода:
        -- отладки кода
        -- передача аргументов
        -- запуск нескольких пауков параллельно в рамках одного процесса
    Технология:
        CrawlerRunner + Thread (поток)
    Недочёты:
        не знаем, как послать сигнал для Thread, когда работа паука уже завершена...
'''


from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from twisted.internet import task
from twisted.internet import reactor  # сам реактор, который и будет запускать паука
from threading import Thread
import time

# Паук:
from books_ItemLoader.spiders.books import BooksSpider


if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()

    # CrawlerRunner

    runner = CrawlerRunner(settings)

    # Параметры процесса
    # -- Описание процесса с указанием класса паука и его параметров
    # -- в рамках процесса может быть несколько пауков
    # Внимание!
    #   Если указать обычный (неключевой) аргумент после класса паука,
    #   то этот неключевой аргумент переопределит имя паука, так как изменит атрибут name (паука) на это значение.
    #   То есть имя паука в атрибуте класса self.name изменится.

    runner.crawl(BooksSpider, "MyBooks", categories='Travel,Classics', key2='toscrape.com')

    # Thread
    # -- ??? технология не разобрана... ???
    # Внимание!
    #   ??? ручной режим для завершения... по времени ???

    Thread(target=reactor.run, args=(False,)).start()
    time.sleep(5)
    Thread(target=reactor.stop).start()

    print(f"---\nПаук завершил свою работу")
    print(f"End")
