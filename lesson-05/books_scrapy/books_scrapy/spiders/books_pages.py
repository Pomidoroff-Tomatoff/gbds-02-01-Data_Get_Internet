import scrapy
import sys    # для записи лога


class BooksPagesSpider(scrapy.Spider):
    name = 'books_pages'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    count_page = 0  # добавленная переменная для подсчёта количества обработанных страниц
    log_file_name = "books_pages__log.txt"

    def parse(self, response, **kwargs):

        # 1. Парсим краткий список книг на текущей странице для получения
        #    ссылок на индивидуальную страницу каждой книги
        #    -. Сообщаем в лог-файл о странице, поступившей на обработку
        #    a. Получаем список всех объектов с описанием книг
        #    б. По этому списку объектов-книг проведём цикл с получением ссылки
        #       для каждой книги
        #    в. Для полученной ссылки выполняем запрос с получением индивидуальной страницы книги,
        #       возврат (callback) которого передаём в метод парсинга индивидуальной страницы.

        self.count_page = self.count_page + 1
        with open(self.log_file_name, "a", encoding="utf-8") as file_log:
            for output_strim in [sys.stdout, file_log]:
                print(f"Парсим страницу списка книг {self.count_page:>2}, url: {response.url}", file=output_strim)

        books = response.xpath('//ol[@class="row"]/li')
        for book in books:
            local_link = book.xpath('.//h3/a/@href').get()
            if local_link:
                link = response.urljoin(local_link)
                yield scrapy.Request(url=link, callback=self.parse_book)

        # 2. Следующая страница (краткого списка книг):
        #    a. Ищем кнопку "Next" для перехода на следующую страницу и берём из неё локальную ссылку
        #       на следующую страницу
        #    б. Если следующая страница есть и локальную ссылку на неё не пустая
        #       объединяем корневую ссылку с только что полученной локальной ссылкой.
        #    в. Загружаем новую страницу (методом Request) и результат (response)
        #       отдаём себе же при помощи асинхронной технологии callback
        #       для выполнения пункта 1 -- парсинга списка книг (ссылок на их индивидуальные страницы).

        next_page = response.xpath('//li[@class="next"]/a[contains(text(), "next")]/@href').get()
        if next_page:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)

    def parse_book(self, response):

        # Парсим данные о книге на её индивидуальной страницы

        article = response.xpath('//article[@class="product_page"]')
        yield {
            'title':
                article.xpath('.//div[contains(@class, "product_main")]/h1/text()').get(),
            'image': response.urljoin(
                article.xpath('.//div[@id="product_gallery"]//div[@class ="item active"]/img/@src').get()),
        }
