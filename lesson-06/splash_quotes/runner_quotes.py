# Запуск паука как файла (модуля) пайтона, а не shell-командой "scrapy crawl..."
# удобно для отладки кода

from twisted.internet import reactor  # сам реактор, который и будет запускать паука

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from splash_quotes.spiders.quotes import QuotesSpider  # Наш паучёк


if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(QuotesSpider)

    reactor.run()  # почему-то виснем здесь...

    print("End-1")
    print("End-2")
