import scrapy


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response, **kwargs):

        # 1. Парсим краткий список книг на текущей странице

        books = response.xpath('//ol[@class="row"]/li')
        for book in books:
            yield {
                'title': book.xpath('.//h3/a/@title').get(),
                'image':
                    response.urljoin(
                         book.xpath('.//div[@class="image_container"]/a/img/@src').get()
                    ),
                'price': book.xpath('.//p[@class="price_color"]/text()').get(),
                'instock':
                    "".join(
                         book.xpath('.//p[contains(@class, "instock")]/text()').getall()
                    ).strip(),
            }

        # 2. Следующая страница
        #    a. Ищем кнопку "Next" для перехода на следующую страницу и берём из неё локальную ссылку
        #       на следующую страницу
        #    б. Если следующая страница есть и локальную ссылку на неё не пустая
        #       объединяем корневую ссылку с только что полученной локальной ссылкой.
        #    в. Грузим новую страницу (методом Request) и результат (response)
        #       отдаём себе же при помощи асинхронной технологии callback.

        next_page = response.xpath('//li[@class="next"]/a[contains(text(), "next")]/@href').get()
        if next_page:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
