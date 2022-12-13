import scrapy
from w3lib.url import add_or_replace_parameters

from job.items import HhList_JobItem


class HhListSpider(scrapy.Spider):
    name = 'hh_list'
    allowed_domains = ['hh.ru']
    # start_urls = ['http://hh.ru/']
    # start_urls = ['https://nahabino.hh.ru/search/vacancy?area=1&clusters=true&enable_snippets=true&items_on_page=20&ored_clusters=true&search_field=description&text=python&order_by=publication_time&hhtmFrom=vacancy_search_list']
    start_url = 'https://hh.ru/search/vacancy/'

    count_pages = 0
    max_count_pages = 500000

    # Параметры поиска вакансий
    # -- примантировать параметры к начальной ссылке можно при помощи хорошей функции
    #      add_or_replace_parameters (w3lib.url)
    #    позволяющей не беспокоится о правилах стыковки частей запроса.
    item_on_page = 20
    params = {
        'area': 1,
        'clusters': 'true',
        'enable_snippets': 'true',
        'items_on_page': item_on_page,
        'ored_clusters': 'true',
        'search_field': 'description',
        'text': 'python',
        'order_by': 'publication_time',
        'hhtmFrom': 'vacancy_search_list',
        'customDomain': 1,
    }

    custom_settings = {
        # LOG_LEVEL
        # https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-LOG_LEVEL
        # In list: CRITICAL, ERROR, WARNING, INFO, DEBUG
        'LOG_LEVEL': 'ERROR',

        # Описание других параметров:
        # https://pypi.python.org/pypi/scrapy-splash
    }

    def start_requests(self):
        response = scrapy.Request(
            url=add_or_replace_parameters(self.start_url, self.params),
            callback=self.parse)
        yield response

    def parse(self, response):
        self.count_pages += 1
        vacancies = response.xpath('//div[@id="a11y-main-content"]/div[@class="serp-item"]')
        print(f"Processing page is: {self.count_pages:0>3}, {len(vacancies)=}")
        for vacancy in vacancies:
            yield self.parse_item(vacancy)

        next = response.xpath('//div[@data-qa="pager-block"]/a[@data-qa="pager-next"]/@href').get()
        if next:
            if self.count_pages < self.max_count_pages:
                yield response.follow(url=next, callback=self.parse)
        return 0

    def parse_item(self, vacancy):
        # поехали
        item = HhList_JobItem(
            title =
                vacancy.xpath('.//a[@class="serp-item__title"]/text()').get(),
            link =
                vacancy.xpath('.//a[@class="serp-item__title"]/@href').get().split('?')[0],
            employer = self.join_clear(
                vacancy.xpath('.//a[@data-qa="vacancy-serp__vacancy-employer"]/text()').getall()),
            salary = self.join_clear(
                vacancy.xpath('.//span[@data-qa="vacancy-serp__vacancy-compensation"]/text()').getall())
        )
        item['vacancy_id'] = item['link'].split('/vacancy/')[1]
        return item

    # БИБЛИОТЕКА
    def join_clear(self, words: list = []) -> str:
        ''' объединяем список слов в строку заменяя спец-пробелы '''
        def join_digit_word(word: str = "") -> str:
            ''' Схлопнуть спец-пробел между цифрами,
                а между словами и цифрами -- поставить обычный пробел '''
            elements = word.split()
            for i in range(len(elements) - 1):
                if elements[i].isdigit():
                    if elements[i + 1].isdigit():
                        elements[i + 1] = "".join([elements[i], elements[i + 1]])
                        elements[i] = ""
            else:
                word = " ".join(elements)
            return word

        if type(words) is list:
            for i in range(len(words)):
                words[i] = join_digit_word(words[i])
            string = " ".join(words)
            string = " ".join(string.split())
        elif type(words) is str:
            string = join_digit_word(words)
        else:
            string = words  # Ничего не делаем
        return string
        # END join_clear()

