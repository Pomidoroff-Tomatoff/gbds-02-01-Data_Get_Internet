# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BooksItemloaderPipeline:
    def __init__(self):
        self.icount: int = 0

    def open_spider(self, spider):
        print(f"pipelines open: {spider.name=}")

    def process_item(self, item, spider):
        try:
            print(f"pipeline: {self.icount:05d} {item.get('title')[:60:]:60s}")
        except Exception as errmsg:
            print(f"pipelines: {self.icount:05d} {item=}")
        else:
            pass
        finally:
            pass

        # начальный item == 0, так как это общее название страницы, название книг далее...
        self.icount += 1
        return item
