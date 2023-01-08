# Запуск паука как файла (модуля) пайтона, а не shell-командой "scrapy crawl..."
# удобно для отладки кода

from twisted.internet import reactor  # сам реактор, который и будет запускать паука

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from books_scrapy.spiders.books import BooksSpider  # Наш паучёк b_tmp.py и его класс BTmpSpider


if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(BooksSpider)

    reactor.run()  # почему-то виснем здесь...
    reactor.run()  # почему-то виснем здесь...

    print("End-1")
    print("End-2")
