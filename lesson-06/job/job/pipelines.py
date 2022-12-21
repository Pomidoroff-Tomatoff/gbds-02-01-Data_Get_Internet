# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
import sqlite3


class SQLite_JobPipeline:

    connection = None
    cursor = None
    base_name = 'job_base'
    base_name_ext = '.db'
    table_name = 'vacancies'
    item_count = 0

    create_table_query = f'''
        CREATE TABLE {table_name}(
            _id INTEGER PRIMARY KEY,
            title TEXT,
            vacancy_id TEXT,
            link TEXT,
            employer TEXT,
            salary TEXT,
            date_publication TEXT
        )
        '''
    insert_query = f'''
        INSERT INTO {table_name}(
            title,
            vacancy_id,
            link,
            employer,
            salary,
            date_publication
            )
        VALUES(?, ?, ?, ?, ?, ?)
        '''

    def open_spider(self, spider):
        # имя базы: добавляем имя паука
        base_name_and_spider = self.base_name + '__' + spider.name + self.base_name_ext
        self.connection = sqlite3.connect(base_name_and_spider)
        self.cursor = self.connection.cursor()

        try:
            self.cursor.execute(self.create_table_query)
            self.connection.commit()
        except sqlite3.OperationalError:
            print(f"Таблица SQLite {self.table_name} уже существует...")
            pass
        else:
            pass

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        if getattr(item, 'collection_name'):
            pass
        else:
            pass

        pass
        self.cursor.execute(self.insert_query, (
            item.get('title'),
            item.get('vacancy_id'),
            item.get('link'),
            item.get('employer'),
            item.get('salary'),
            item.get('date_publication')
            )
        )
        self.connection.commit()
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
        self.mongodb_collection.insert_one(item)
        return item


class JobPipeline:

    def open_spider(self, spider):
        self.item_count = 0

    def close_spider(self, spider):
        print(f"Processed items is: {self.item_count}")

    def process_item(self, item, spider):
        self.item_count += 1
        print(f"{self.item_count:0>5}. employer={item.get('employer'):<20s}, {item['title']= }")
        return item
