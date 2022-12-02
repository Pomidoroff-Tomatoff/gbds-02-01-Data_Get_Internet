# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import sys      # для записи лога в текстовый файл
import datetime


class BTmp_Pipeline:
    ''' Эксперимент на основе видео-лекции по открытию базы данных '''
    def __init__(self):
        ''' конструктор класса
        инициализация подлючения к БД МогдоДБ
        '''
        self.client_database_mongo = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        self.db_base = self.client_database_mongo["book_toscrape"]
        self.db_collection = self.db_base[spider.name]  # Имя коллекции задаём по имени паучка

    def __del__(self):
        ''' деструктор (финализатор) класса
            Ранее здесь размещалось закрытие подключения к базе данных MongoDB
            Внимание!
                Если выполняем закрытие клиентского канала к базе,
                то виснем...
                -- возможно, потому что закрытие базы данных может приводить к вызову этого метода (для закрытия БД)...
                Но это зависание началось не сразу...
        '''
        # self.client_database_mongo.close()

    def process_item(self, item, spider):
        return item


class TXT_LOG_BooksScrapyPipeline:
    # Файл (текстовый) лога
    file_log = None

    # Счётчик итераций или проходов
    count_page = 0

    def open_spider(self, spider):
        ''' Метод инициализации паука
        Открытие подключения к текстовому лог-файлу
        '''
        self.file_log = open((spider.name + "__log.txt"), "a", encoding="utf-8")
        print(f"Pipelines. CLASS TXT_LOG_BooksScrapyPipeline: ОТКРЫТ лог-файл \"{self.file_log.name}\"")

    def close_spider(self, spider):
        ''' Закрытие паучка '''
        self.file_log.close()
        print(f"Pipelines. CLASS TXT_LOG_BooksScrapyPipeline, ЗАКРЫТО: текстовый лог-файл")

    def log_item(self, item, spider):
        ''' log в текстовый файл для текущего item (кратко) '''
        self.count_page = self.count_page + 1
        for output_strim in [sys.stdout, self.file_log]:
            print(f"{datetime.datetime.now().strftime('%Y-%m-%d; %H.%M.%S')},  проход: {self.count_page:0>4}, title: {item['title']}", file=output_strim)

    def process_item(self, item, spider):
        self.log_item(item, spider)  # Заносим itme в лог файл, кратко.
        return item  # Да, здесь ретурн, а не йельд...


class MongoDB_BooksScrapyPipeline:

    # База данных MongoDB
    db_address = "mongodb://127.0.0.1:27017"
    db_name = "toscrape_book"
    db_base = None
    db_collection = None

    def open_spider(self, spider):
        ''' Метод инициализации паука
        Открытие подключения к базе данных MongoDB, текстовому лог-файлу
        '''
        self.client_database_mongo = pymongo.MongoClient(self.db_address)
        self.db_base = self.client_database_mongo[self.db_name]
        self.db_collection = self.db_base[spider.name]  # Имя коллекции задаём по имени паучка
        print(f"Pipelines: CLASS MongoDB_BooksScrapyPipeline, ОТКРЫТА БД MongoDB \"{self.db_base.name}\", коллекция \"{self.db_collection.name}\"")
        return

    def close_spider(self, spider):
        ''' Закрытие паучка '''
        self.client_database_mongo.close()
        print(f"Pipelines. CLASS MongoDB_BooksScrapyPipeline, ЗАКРЫТО: БД MongoDB.")
        return

    def process_item(self, item, spider):
        self.db_collection.insert_one(item)  # Заносим item в коллекцию базы. Имя коллекции по имени паучка.
        # print(f"Pipelines. CLASS MongoDB_BooksScrapyPipeline: документ занесён в БД.")
        return item


class BooksScrapyPipeline:
    ''' Класс, автоматически созданный при генерации проекта '''

    def process_item(self, item, spider):
        # print(f"Pipelines. CLASS BooksScrapyPipeline: стандартная обработка. {item}")
        return item
