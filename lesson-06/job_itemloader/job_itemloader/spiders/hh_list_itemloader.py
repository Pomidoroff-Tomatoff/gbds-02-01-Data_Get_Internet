import scrapy
from scrapy.loader import ItemLoader
from w3lib.url import add_or_replace_parameters

from job_itemloader.items import HhList_itemloader_JobItem


class HhListItemloaderSpider(scrapy.Spider):
    name = 'hh_list_itemloader'
    allowed_domains = ['hh.ru']
    start_url = 'https://hh.ru/search/vacancy/'
    # start_urls = ['http://hh.ru/']

    # Имя для MongoDB и MySQL для этого паучка
    collection_name = HhList_itemloader_JobItem.collection_name

    # счётчики-ограничители
    count_pages = 1
    max_count_pages = 2  # 500000  # макс. количество страниц со списком вакансий, для отладки


    custom_settings = {
        # LOG_LEVEL
        # https://docs.scrapy.org/en/latest/topics/settings.html#std-setting-LOG_LEVEL
        # In list: CRITICAL, ERROR, WARNING, INFO, DEBUG
        'LOG_LEVEL': 'ERROR',

        # Описание других параметров:
        # https://pypi.python.org/pypi/scrapy-splash
    }

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

    def start_requests(self):
        # Собрать параметры params с начальной ссылкой можно при помощи функции
        #      add_or_replace_parameters (w3lib.url)
        response = scrapy.Request(
            url=add_or_replace_parameters(self.start_url, self.params),
            callback=self.parse)
        yield response

    def parse(self, response):
        vacancies = response.xpath('//div[@id="a11y-main-content"]/div[contains(@class, "serp-item")]')
        if (page_processing := response.url.split("page=")[-1]).isdigit():
            page_processing = int(page_processing)
            page_processing += 1
        else:
            page_processing = 1
        print(f"PAGE PROCESSING: {page_processing:->5} ({self.count_pages:->5}), {len(vacancies)=}")
        for vacancy in vacancies:
            yield self.parse_item(vacancy)

        # Ограничение страниц: можно?
        if self.count_pages >= self.max_count_pages:   # ограничение
            return None  # хватит...
        else:
            self.count_pages += 1

        # переход
        next = response.xpath('//div[@data-qa="pager-block"]/a[@data-qa="pager-next"]/@href').get()
        if next:
            yield response.follow(url=next, callback=self.parse)
        return None

    def parse_item(self, selector):

        item = ItemLoader(item=HhList_itemloader_JobItem(), selector=selector)

        item.add_xpath('_id', './/a[@data-qa="vacancy-serp__vacancy_response"]/@href')
        item.add_xpath('title', './/a[@class="serp-item__title"]/text()')
        item.add_xpath('employer', './/a[@data-qa="vacancy-serp__vacancy-employer"]/text()')
        item.add_xpath('salary_min', './/span[@data-qa="vacancy-serp__vacancy-compensation"]/text()')
        item.add_value('salary_max', -1)
        item.add_value('salary_cur', -1)
        item.add_value('link', '')

        return item.load_item()
