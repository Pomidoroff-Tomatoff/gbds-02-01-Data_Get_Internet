import scrapy

from books_scrapy.items import Books_Pages_BooksScrapyItem


class BooksPagesSpider(scrapy.Spider):
    name = 'books_pages'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    custom_settings = {
        # LOG_LEVEL
        # https: // docs.scrapy.org / en / latest / topics / settings.html  # std-setting-LOG_LEVEL
        # In list: CRITICAL, ERROR, WARNING, INFO, DEBUG (https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-LOG_LEVEL)
        'LOG_LEVEL': 'ERROR',
    }

    ''' После включения piplines.py функциональность с базой данных MongoDB 
        и текстовым логом переехала в файл piplines.py и классы 
        MongoDB_BooksScrapyPipeline и
        XT_LOG_BooksScrapyPipeline соответственно
    '''

    def parse(self, response, **kwargs):
        # 1. Парсим краткий список книг на текущей странице для получения
        #    ссылок на индивидуальную страницу каждой книги
        #    -. Сообщаем в лог-файл о странице, поступившей на обработку
        #    a. Получаем список всех объектов с описанием книг
        #    б. По этому списку объектов-книг проведём цикл с получением ссылки
        #       для каждой книги
        #    в. Для полученной ссылки выполняем запрос с получением индивидуальной страницы книги,
        #       возврат (callback) которого передаём в метод парсинга индивидуальной страницы.

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

        ''' Парсим данные о книге с её индивидуальной страницы '''

        article = response.xpath('//article[@class="product_page"]')
        table_data = article.xpath('./table[contains(@class, "table")]')

        item = Books_Pages_BooksScrapyItem(
            title =
                article.xpath('.//div[contains(@class, "product_main")]/h1/text()').get(),
            price =
                article.xpath('.//div[contains(@class, "product_main")]/p[@class="price_color"]/text()').get(),
            in_stock ="".join(
                article.xpath('.//div[contains(@class, "product_main")]/p[@class="instock availability"]/text()').getall()
                ).strip(),
            image = response.urljoin(
                article.xpath('.//div[@id="product_gallery"]//div[@class ="item active"]/img/@src').get()
                ),
            product_description =
                article.xpath('./div[@id="product_description"]/following-sibling::p[1]/text()').get(),
            upc =
                table_data.xpath('.//th[contains(text(), "UPC")]/following-sibling::td[1]/text()').get(),
            product_type =
                table_data.xpath('.//th[contains(text(), "Product Type")]/following-sibling::td[1]/text()').get(),
            price_exclude_tax =
                table_data.xpath('.//th[contains(text(), "Price (excl. tax)")]/following-sibling::td[1]/text()').get(),
            price_include_tax =
                table_data.xpath('.//th[contains(text(), "Price (incl. tax)")]/following-sibling::td[1]/text()').get(),
            tax =
                table_data.xpath('.//th[contains(text(), "Tax")]/following-sibling::td[1]/text()').get(),
            availability =
                table_data.xpath('.//th[text()="Availability"]/following-sibling::td[1]/text()').get(),
            number_of_reviews =
                table_data.xpath('.//th[text()="Number of reviews"]/following-sibling::td[1]/text()').get()
        )

        yield item
