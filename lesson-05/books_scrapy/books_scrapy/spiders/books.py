import scrapy
import sys  # для лога


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    count_page = 0  # добавленная переменная для подсчёта количества обработанных страниц
    log_file_name = "books__log.txt"  # log-файл

    def parse(self, response, **kwargs):

        # 1. Парсим краткий список книг на текущей странице
        #    -. Сообщаем в лог-файл о странице, поступившей на обработку
        #    a. Получаем список всех объектов с описанием книг
        #    б. По этому списку объектов-книг проведём цикл с получением данных по каждой книге

        self.count_page = self.count_page + 1
        with open("books.log.txt", "a", encoding="utf-8") as file_log:
            for output_strim in [sys.stdout, file_log]:
                print(f"Парсим страницу списка книг {self.count_page:>2}, url: {response.url}", file=output_strim)

        books = response.xpath('//ol[@class="row"]/li')
        for book in books:
            yield {
                'title':
                    book.xpath('.//h3/a/@title').get(),
                'image': response.urljoin(
                    book.xpath('.//div[@class="image_container"]/a/img/@src').get()),
                'price':
                    book.xpath('.//p[@class="price_color"]/text()').get(),
                'instock': "".join(
                    book.xpath('.//p[contains(@class, "instock")]/text()').getall()).strip(),
            }

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
