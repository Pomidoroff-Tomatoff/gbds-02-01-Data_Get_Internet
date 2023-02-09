''' GB BigData / Олег Гладкий (https://gb.ru/users/3837199) // домашнее задание
    Исследования:
    -- аргументы командной строки:
       > передаваемые shell-командой
       > параметрами директивы скрипта (ранера)
'''


import scrapy


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    def __init__(self, *args, **kwargs):
        super(BooksSpider, self).__init__(*args, **kwargs)
        self.icount = 0
        if args:
            print(f"Внимание! Изменено имя паука, теперь: {self.name=} неключевым аргументом \"{args=}\"")
            # self.name = 'books'  # возврат имени паука, если оно было изменено в операторе с параметром *args
            # print(f"Возвращаем имя паука как в классе: {self.name=}")
            self.args = args

        if not kwargs:
            pass
            # raise "Нет аргументов"
        else:
            for key, value in kwargs.items():
                value_lst = list(value.split(','))
                if len(value_lst) > 1:
                    kwargs[key] = value_lst
            self.kwargs = kwargs
            pass

        print(f"Паук __init__:  {self.name=}: аргументы {args=}")
        print(f"Паук __init__:  {self.name=}: аргументы {kwargs=}")

    def parse(self, response):
        print(f"Парсер, получены аргументы:\n{self.args=}\n{self.kwargs=}")
        return None
