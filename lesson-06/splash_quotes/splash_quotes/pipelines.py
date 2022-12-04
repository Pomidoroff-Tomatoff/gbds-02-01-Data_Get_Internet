# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo


class MongoDB_QuotesPipeline:

    # База данных MongoDB
    mongodb_address = "mongodb://127.0.0.1:27017"
    mongodb_client = None
    mongodb_base_name = "toscrape_quote"  # for both Quotes and Author collections
    mongodb_base = None
    mongodb_collection = None

    def open_spider(self, spider):
        self.mongodb_client = pymongo.MongoClient(self.mongodb_address)
        self.mongodb_base = self.mongodb_client[self.mongodb_base_name]
        # self.mongodb_collection = self.mongodb_base[spider.name]  # collection name == Spider Name
        return

    def close_spider(self, spider):
        self.mongodb_client.close()
        return

    def process_item(self, item, spider):
        self.mongodb_collection = self.mongodb_base[item.collection_name]  # collection name == class Item Name
        self.mongodb_collection.insert_one(item)
        return item


class SplashQuotesPipeline:

    def open_spider(self, spider):
        self.item_count = 0
        return

    def close_spider(self, spider):
        print(f"Total parsed items:  {self.item_count}.")
        return

    def process_item(self, item, spider):
        self.item_count += 1
        print(f"{self.item_count: >5}, collection \'{item.collection_name}\', {item['author']=}")
        return item
