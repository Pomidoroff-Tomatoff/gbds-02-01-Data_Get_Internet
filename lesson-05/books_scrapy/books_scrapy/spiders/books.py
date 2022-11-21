import scrapy
import sys  # для лога
import datetime

from books_scrapy.items import Books_BooksScrapyItem




class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    count_page = 0  # добавленная переменная для подсчёта количества обработанных страниц
    log_file_name = "books__log.txt"  # log-файл

    custom_settings = {
        # LOG_LEVEL
        # https: // docs.scrapy.org / en / latest / topics / settings.html  # std-setting-LOG_LEVEL
        # In list: CRITICAL, ERROR, WARNING, INFO, DEBUG (https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-LOG_LEVEL)
        'LOG_LEVEL': 'ERROR',

        # РАЗРЕШАЕМ ИСПОЛЬЗОВАНИЕ piplines.py для внесения полученных данных парсера в базу данных
        # Configure item pipelines
        # See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
        'ITEM_PIPELINES': {
            'books_scrapy.pipelines.BooksScrapyPipeline': 300, # это приоритет, чем больше цифра, тем он ниже...
        }
    }

    def parse(self, response, **kwargs):

        # 1. Парсим краткий список книг на текущей странице
        #    -. Сообщаем в лог-файл о странице, поступившей на обработку
        #    a. Получаем список всех объектов с описанием книг
        #    б. По этому списку объектов-книг проведём цикл с получением данных по каждой книге

        self.count_page = self.count_page + 1
        with open("books__log.txt", "a", encoding="utf-8") as file_log:
            for output_strim in [sys.stdout, file_log]:
                print(f"{datetime.datetime.now().strftime('%Y-%m-%d; %H.%M.%S')},  pass: {self.count_page:0>4},  url: {response.url}", file=output_strim)

        books = response.xpath('//ol[@class="row"]/li')
        for book in books:
            item = Books_BooksScrapyItem(
                title=
                    book.xpath('.//h3/a/@title').get(),
                image=response.urljoin(
                    book.xpath('.//div[@class="image_container"]/a/img/@src').get()),
                price=
                    book.xpath('.//p[@class="price_color"]/text()').get(),
                instock="".join(
                    book.xpath('.//p[contains(@class, "instock")]/text()').getall()).strip()
            )
            yield item

        # 2. Следующая страница (краткого списка книг):
        #    a. Ищем кнопку "Next" для перехода на следующую страницу и берём из неё локальную ссылку
        #       на следующую страницу
        #    б. Если следующая страница есть и локальную ссылку на неё не пустая
        #       объединяем корневую ссылку с только что полученной локальной ссылкой.
        #    в. Загружаем новую страницу (методом Request) и результат (response)
        #       отдаём себе же при помощи асинхронной технологии callback
        #       для выполнения пункта 1 -- парсинга списка книг.

        next_page = response.xpath('//li[@class="next"]/a[contains(text(), "next")]/@href').get()
        if next_page:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
