# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
import sqlite3
import traceback


class SQLite_JobPipeline:

    connection = None
    cursor = None
    base_name_std = 'job_base'
    base_name_ext = '.db'
    table_name = 'vacancies'
    item_count = 0

    def get_query(self, name: str = table_name, query: str = 'insert'):
        ''' Подстановка в запрос: имя таблицы '''
        if query.upper() == 'insert'.upper():
            insert_query = f'''
                INSERT INTO {name}(
                    _id,
                    title,
                    employer,
                    salary_min,
                    salary_max,
                    salary_cur,
                    date_publication,
                    link
                    )
                VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                '''
            return insert_query

        if query.upper() == 'create'.upper():
            create_table_query = f'''
                CREATE TABLE {name}(
                    _id INTEGER PRIMARY KEY,
                    title TEXT,
                    employer TEXT,
                    salary_min INTEGER,
                    salary_max INTEGER,
                    salary_cur TEXT,
                    date_publication TEXT,
                    link TEXT
                )
                '''
                # vacancy_id INTEGER KEY,
            return create_table_query


    def open_spider(self, spider):
        ''' Иниализация класса при открытии паука '''
        if getattr(spider, 'collection_name'):
            # Задаём имя таблицы по имени атрибута коллекции в классе Item
            self.table_name = spider.collection_name

        # имя базы строим по имени паука -- стандартная часть + имя паучка
        base_name = self.base_name_std + '__' + spider.name + self.base_name_ext
        self.connection = sqlite3.connect(base_name)  # соединение (создание) с БД на диске
        self.cursor = self.connection.cursor()        # указатель на открытую БД

        # создаём таблицу
        try:
            self.cursor.execute(self.get_query(name=spider.collection_name, query='create'))
            # self.cursor.execute(self.create_table_query)
            self.connection.commit()
        except sqlite3.OperationalError:
            print(f"Таблица SQLite {spider.collection_name} уже существует...")
            pass
        else:
            pass

        print(f"База данных: {base_name}")
        print(f"Таблица в базе данных: {self.table_name}")

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(self.get_query(name=spider.collection_name, query='insert'), (
                item.get('_id'),
                item.get('title'),
                item.get('employer'),
                item.get('salary_min'),
                item.get('salary_max'),
                item.get('salary_cur'),
                item.get('date_publication'),
                item.get('link')
                )
            )
            self.connection.commit()
        except sqlite3.IntegrityError as error_msg:
            print(f". . . .SQLite,  {item['_id']=}, {error_msg}")
        except sqlite3.OperationalError as error_msg:
            print(f". . . .SQLite,  {item['_id']=}, {error_msg}")
        else:
            pass  # здесь всё хорошо!

        return item


class MongoDB_JobPipeline:
    ''' База данных MongoDB '''

    mongodb_address = "mongodb://127.0.0.1:27017"
    mongodb_client = None
    mongodb_base_name = "job"
    mongodb_base = None
    mongodb_collection = None

    def open_spider(self, spider):
        self.mongodb_client = pymongo.MongoClient(self.mongodb_address)
        self.mongodb_base = self.mongodb_client[self.mongodb_base_name]
        return

    def close_spider(self, spider):
        self.mongodb_client.close()
        return

    def process_item(self, item, spider):
        # Имя коллекции (таблица) определяется либо по атрибуту 'collection_name' класса "item",
        # а если он не определён, то по имени паука
        if getattr(item, 'collection_name'):
            self.mongodb_collection = self.mongodb_base[item.collection_name]
        else:
            self.mongodb_collection = self.mongodb_base[spider.name]

        # Заносим данные в базу!
        try:
            self.mongodb_collection.insert_one(item)
        except pymongo.errors.DuplicateKeyError as errmsg:
            print(f". . . .MongoDB, {item['_id']=}, DuplicateKeyError")
        else:
            pass  # здесь всё хорошо!

        return item


class JobPipeline:

    def open_spider(self, spider):
        self.item_count = 0

    def close_spider(self, spider):
        print(f"Processed items is: {self.item_count}")

    def process_item(self, item, spider):
        self.item_count += 1
        # print(f"{self.item_count:0>5}. employer={item.get('employer')=}")
        print(f"{self.item_count:0>5}. "
              f"{item.get('_id')}  "
              f"{(item.get('employer')[:20:] if item.get('employer') else ''):<20s}  "
              f"{item.get('title')}")
        return item
