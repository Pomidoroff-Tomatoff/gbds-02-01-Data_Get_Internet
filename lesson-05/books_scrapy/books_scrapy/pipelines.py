# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import sys      # для записи лога в текстовый файл
import datetime


class BooksScrapyPipeline:

    # Счётчик итераций или проходов
    count_page = 0

    def __init__(self):
        ''' конструктор класса
            Открытие подключения к базе данных MongoDB
        '''
        db_address = "mongodb://127.0.0.1:27017"
        db_name = "book_toscrape"
        self.client_database_mongo = pymongo.MongoClient(db_address)
        self.base = self.client_database_mongo[db_name]
        print(f"Pipelines: База OPEN")


    def __del__(self):
        ''' деструктор (финализатор) класса
            Закрытие подключения к базе данных MongoDB
            Внимание!
                Если выполняем закрытие клиентского канала к базе,
                то виснем...
                Но это зависание началось не сразу...
        '''
        print(f"Pipelines: База закрывается {self.client_database_mongo=}")
        # self.client_database_mongo.close()
        # print(f"Pipelines: закр {self.client_database_mongo=}")


    def log_item(self, item, spider):
        ''' log для текущей item
        '''
        self.count_page = self.count_page + 1
        with open((spider.name + "__log.txt"), "a", encoding="utf-8") as file_log:
            for output_strim in [sys.stdout, file_log]:
                print(f"{datetime.datetime.now().strftime('%Y-%m-%d; %H.%M.%S')},  pass: {self.count_page:0>4}, title: {item['title']}", file=output_strim)


    def process_item(self, item, spider):
        collection = self.base[spider.name]  # Имя коллекции задаём по имени паучка
        collection.insert_one(item)
        self.log_item(item, spider)

        return item
