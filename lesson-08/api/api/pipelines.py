# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging  # журналирование
import pymongo
import sqlite3
import traceback
import time

logger = logging.getLogger(__name__)


class SQLite_ApiPipeline:

    def __init__(self, sqlite_base_name, sqlite_table_name):
        self.base_name_std = sqlite_base_name
        self.base_name_ext = '.db'
        self.table_name = sqlite_table_name
        self.connection = None
        self.cursor = None
        self.item_count_processed = 0      # счётчик всего
        self.item_count_inserted = 0       # счётчик успеха
        self.item_count_error_key = 0      # счётчик ошибок ключа
        self.item_count_error_io = 0       # счётчик ошибок записи
        self.item_count_error_other = 0    # счётчик остальных ошибок


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_base_name=crawler.settings.get('SQL_DATABASE'),
            sqlite_table_name=crawler.settings.get('SQL_TABLE')
        )

    def get_query(self, name: str = 'test_name', query: str = 'insert'):
        ''' Формальный запрос SQLite. Параметр: имя таблицы '''
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
            return create_table_query

    def open_spider(self, spider):
        logger.warning(f"SQLite, database: {self.base_name_std}{self.base_name_ext}")
        logger.warning(f"SQLite, db-table: {self.table_name}")

        self.connection = sqlite3.connect(self.base_name_std + self.base_name_ext)  # открываем соединение с БД (файл на диске)
        self.cursor = self.connection.cursor()        # указатель на открытую БД

        try:
            self.cursor.execute(self.get_query(name=self.table_name, query='create'))
            self.connection.commit()
        except sqlite3.OperationalError:
            print(f"SQLite: Таблица {self.table_name} уже существует...")
        except Exception as errmsg:
            print(f"SQLite, что-то с таблицей: {errmsg}.")
        else:  # успех, нет исключения
            pass

        print(f"SQLite: База данных: {self.base_name_std + self.base_name_ext}")
        print(f"SQLite: Таблица БД:  {self.table_name}")
        return None

    def close_spider(self, spider):
        self.connection.close()
        print(f"SQLite: items keyError: {self.item_count_error_key}")
        print(f"SQLite: items io-error: {self.item_count_error_io}")
        print(f"SQLite: items otherErr: {self.item_count_error_other}")
        print(f"SQLite: items inserted: {self.item_count_inserted}")
        return None

    def process_item(self, item, spider):
        def sql_record_insert():
            ''' SQL: запись на диск '''
            nonlocal item, item_count_error_io__retry
            try:
                self.cursor.execute(self.get_query(name=self.table_name, query='insert'), (
                    item.get('_id'),
                    item.get('name'),
                    item.get('employer_name'),
                    item.get('salary_min'),
                    item.get('salary_max'),
                    item.get('salary_cur'),
                    item.get('date_publication'),
                    item.get('url')
                    )
                )
                self.connection.commit()
            except sqlite3.IntegrityError as error_msg:
                self.item_count_error_key += 1    # счётчик ошибок ключа
                print(f". . . .SQLite,  {item['_id']=}, {error_msg}")
            except sqlite3.OperationalError as error_msg:
                item_count_error_io__retry += 1
                print(f". . . .SQLite,  {item['_id']=}, {error_msg}")
            except Exception as error_msg:
                self.item_count_error_other += 1  # счётчик остальных ошибок
                print(f". . . .SQLite,  {item['_id']=}, {error_msg}. Другое...")
            else:     # успех, исключения не было
                item_count_error_io__retry = 0    # сбрасываем счётчик повторов записи, так как у нас успех!
                self.item_count_inserted += 1     # счётчик успеха
            finally:  # всегда, выполняем в любом случае
                pass
            pass  # sql_write

        item_count_error_io__retry = 0   # Попытки записи
        while item_count_error_io__retry < 5:
            sql_record_insert()          # Запись
            if (item_count_error_io__retry > 0) and (item_count_error_io__retry < 5):
                time.sleep(1)            # Задержка перед следующей попыткой...
            else:
                break
        if item_count_error_io__retry > 0:
            self.item_count_error_io += 1  # счётчик ошибок записей, которые всё же внести не удалось...
        self.item_count_processed += 1     # счётчик всех операций

        return item
    pass  # SQLite_ApiPipeline -- class


class MongoDB_ApiPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongodb_address = mongo_uri
        self.mongodb_client = None
        self.mongodb_base_name = mongo_db
        self.mongodb_base = None
        self.mongodb_collection = None
        logger.warning(f"MongoDB: {mongo_uri=}, {mongo_db=}")

    @classmethod
    def from_crawler(cls, spider):
        ''' Получим параметры settings и передадим экз-ру '''
        return cls(
            mongo_uri=spider.settings.get('MONGO_URI'),
            mongo_db=spider.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.mongodb_client = pymongo.MongoClient(self.mongodb_address)
        self.mongodb_base = self.mongodb_client[self.mongodb_base_name]
        self.item_count_processed = 0  # счётчик всех операций
        self.item_count_inserted = 0   # счётчик успеха
        return

    def close_spider(self, spider):
        self.mongodb_client.close()
        print(f"MongoDB items inserted: {self.item_count_inserted}")
        return

    def process_item(self, item, spider):
        # Имя коллекции (таблица) определяется либо по атрибуту 'collection_name' класса "item",
        # а если он не определён, то по имени паука
        if getattr(item, 'collection_name'):
            self.mongodb_collection = self.mongodb_base[item.collection_name]
        else:
            self.mongodb_collection = self.mongodb_base[spider.name]

        # Преобразование времени в строку, так как МонгоДБ не поддерживает тип даты
        # item['date_publication'] = str(item.get('date_publication').date())

        try:  # Заносим в БД
            self.mongodb_collection.insert_one(ItemAdapter(item).asdict())
        except pymongo.errors.DuplicateKeyError as errmsg:
            print(f". . .  MongoDB, {item['_id']=}, DuplicateKeyError: дублирование ключа, строка не внесена.")
        except Exception as errmsg:
            print(f". . .  MongoDB, {item['_id']=}, {errmsg}.")
        else:     # успех, нет исключения
            self.item_count_inserted += 1   # счётчик успеха
        finally:  # всегда
            self.item_count_processed += 1  # счётчик всех операций

        return item  # end of process_item /method
    pass  # end of MongoDB... /class


class ApiPipeline:
    item_count = 0

    def close_spider(self, spider):
        print(f"Processed items all:    {self.item_count}")

    def process_item(self, item, spider):
        self.item_count += 1  # начинаем считать с 1-ы.

        print(f"{self.item_count:.>6d}", end=' ')
        if item.get('_id'):
            print(f"{item.get('_id'):0>7d}", end=' ')
        if item.get('name'):
            print(f"{item.get('name')[:60:]:<60s}", end='')
        print("")
        return item
