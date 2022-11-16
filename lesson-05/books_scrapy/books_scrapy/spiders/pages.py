import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import sys    # для записи лога


class PagesSpider(CrawlSpider):
    name = 'pages'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    custom_settings = {
        # LOG_LEVEL
        # https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-LOG_LEVEL
        # In list: CRITICAL, ERROR, WARNING, INFO, DEBUG (https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-LOG_LEVEL)
        # 'LOG_LEVEL': 'ERROR',
    }

    count_page = 0  # добавленная переменная для подсчёта количества обработанных страниц
    log_file_name = "pages__log.txt"

    # Правила, по которым мы будем действовать:
    #  1. вначале мы должны оказаться на первой странице
    #  2. получаем список ссылок на каждую книгу и по этому списку начинаем проваливаться в каждую книгу
    #  3. переходим на следующую страницу
    #     (находить ссылку по атрибуту href и использовать метод get() парсер будет самостоятельно
    #     и переходим к пункту 2.
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//article[@class='product_pod']/h3/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//li[@class="next"]/a')),
    )

    def parse_item(self, response):
        # лог самодельный...
        self.count_page = self.count_page + 1
        with open(self.log_file_name, "a", encoding="utf-8") as file_log:
            for output_strim in [sys.stdout, file_log]:
                print(f"Проход: {self.count_page:>2}, url: {response.url}", file=output_strim)

        article = response.xpath('//article[@class="product_page"]')
        table_data = article.xpath('./table[contains(@class, "table")]')
        yield {
            'title':
                article.xpath('.//div[contains(@class, "product_main")]/h1/text()').get(),
            'price':
                article.xpath('.//div[contains(@class, "product_main")]/p[@class="price_color"]/text()').get(),
            'in_stock': "".join(
                article.xpath('.//div[contains(@class, "product_main")]/p[@class="instock availability"]/text()').getall()
                ).strip(),
            'image': response.urljoin(
                article.xpath('.//div[@id="product_gallery"]//div[@class ="item active"]/img/@src').get()
                ),
            'product_description':
                article.xpath('./div[@id="product_description"]/following-sibling::p[1]/text()').get(),
                # article.xpath('./p/text()').get(),  # простой, но не привязанный к ID, вариант
            'upc':
                table_data.xpath('.//th[contains(text(), "UPC")]/following-sibling::td[1]/text()').get(),
            'product_type':
                table_data.xpath('.//th[contains(text(), "Product Type")]/following-sibling::td[1]/text()').get(),
            'price_exclude_tax':
                table_data.xpath('.//th[contains(text(), "Price (excl. tax)")]/following-sibling::td[1]/text()').get(),
            'price_include_tax':
                table_data.xpath('.//th[contains(text(), "Price (incl. tax)")]/following-sibling::td[1]/text()').get(),
            'tax':
                table_data.xpath('.//th[contains(text(), "Tax")]/following-sibling::td[1]/text()').get(),
            'availability':
                table_data.xpath('.//th[text()="Availability"]/following-sibling::td[1]/text()').get(),
            'number_of_reviews':
                table_data.xpath('.//th[text()="Number of reviews"]/following-sibling::td[1]/text()').get(),
        }
