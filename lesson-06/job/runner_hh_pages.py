''' GB BigData / Олег Гладкий (https://gb.ru/users/3837199) // домашнее задание
    Запуск паука непосредственно из модуля Python-а (а не shell-командой "scrapy crawl...").
    Технология:
        CrawlerProcess
'''

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

# Паук:
from job.spiders.hh_pages import HhPagesSpider


if __name__ == '__main__':
    # Параметры проекта

    configure_logging()
    settings = get_project_settings()

    # CrawlerProcess

    process = CrawlerProcess(settings)

    # Параметры процесса

    process.crawl(HhPagesSpider)

    # Запускаем процесс
    # -- the script will block here until the crawling is finished

    process.start()

    print(f"---\nПаук завершил свою работу")
    print(f"Stop of CrawlerProcess")
