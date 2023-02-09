''' GB BigData / Олег Гладкий (https://gb.ru/users/3837199) // домашнее задание
    Запуск паука непосредственно из модуля Python-а (а не shell-командой "scrapy crawl...").
    Цели и задачи подхода:
        -- отладки кода
        -- передача аргументов
        -- запуск нескольких пауков параллельно в рамках одного процесса
    Технология:
        CrawlerProcess
'''

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

# Паук:
from books_kwargs.spiders.books import BooksSpider


if __name__ == '__main__':
    # Параметры проекта

    configure_logging()
    settings = get_project_settings()

    # CrawlerProcess

    # process = CrawlerProcess(settings, {'LOG_LEVEL': 'ERROR'})
    process = CrawlerProcess(settings, {'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})

    # Параметры процесса
    # -- Описание процесса с указанием класса паука и его параметров
    # -- в рамках процесса может быть несколько пауков
    # Внимание!
    #   Если указать обычный (неключевой) аргумент после класса паука,
    #   то этот неключевой аргумент переопределит имя паука, так как изменит атрибут name (паука) на это значение.
    #   То есть имя паука в атрибуте класса self.name изменится.

    process.crawl(BooksSpider, "MyBook_NewSpiderName", categories='Travel,Classics', key2='toscrape.com')

    # Запускаем процесс
    # -- the script will block here until the crawling is finished
    process.start()

    print(f"---\nПаук завершил свою работу")
    print(f"Stop of CrawlerProcess")
