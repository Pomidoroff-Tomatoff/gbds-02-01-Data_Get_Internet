''' GB BigData / Олег Гладкий (https://gb.ru/users/3837199) // домашнее задание
    Запуск паука непосредственно из модуля Python-а, технология
        CrawlerRunner + reactor
    Внимание!
        settings.py, необходимо вкл. строку
            TWISTED_REACTOR = 'twisted.internet.selectreactor.SelectReactor'
'''

from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
# Паук:
from login.spiders.sandbox_csrf_javascript import SandboxCsrfJavascriptSpider


if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(SandboxCsrfJavascriptSpider).addBoth(lambda _: reactor.stop())

    reactor.run()
