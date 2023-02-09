''' GB BigData / Олег Гладкий (https://gb.ru/users/3837199) // домашнее задание
    Запуск паука непосредственно из модуля Python-а (а не shell-командой "scrapy crawl...").
    Цели и задачи подхода:
        -- shell-команда из модуля Питона ("scrapy crawl...")
        -- передача аргументов
        -- запуск только одного паука
    Технология:
        scrapy.cmdline.execute
'''


import sys
from scrapy.cmdline import execute


if __name__ == '__main__':
    sys.argv = f"scrapy crawl books -a categories=Travel,Classics".split()
    execute()

    # Внимание!
    # команды далее не выполняется... почему-то...
    print(f"---\nПаук books завершил свою работу")
