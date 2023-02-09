''' БИБЛИОТЕКА для очистки данных сайта hh.ru '''

import datetime


import datetime


def date_convert(values: list = [], lang: str = 'RU'):
    '''Преобразование даты вида "24 января 2023" к типу date (2023-01-26)'''

    def current_date():
        return str(datetime.datetime.now().date())

    # Входящие данные:
    # ['Вакансия опубликована ', '24\xa0января\xa02023', ' в ', 'Москве']

    # Язык месяца:
    if lang.upper() == "RU":
        lang_index = 0
    elif lang.upper() == "EN":
        lang_index = 1
    else:
        print(f"Дата: ОШИБКА -- неверно выбран язык месяца \"{lang}\" {values}, аварийно используется RU.")
        lang_index = 0

    if len(values) <= 1:
        print(f"Дата: ОШИБКА -- неполные или пустые данные \"{values}\"")
        return current_date()

    value = values[1]
    date_elements = value.split()
    months_name = date_elements[1]

    months = {
        1:  ['январ',   'january'],
        2:  ['феврал',  'febrary'],
        3:  ['март',    'march'],
        4:  ['апрел',   'april'],
        5:  ['май',     'may'],
        6:  ['июн',     'june'],
        7:  ['июл',     'july'],
        8:  ['август',  'august'],
        9:  ['сентябр', 'september'],
        10: ['октябр',  'october'],
        11: ['ноябр',   'november'],
        12: ['декабр',  'december'],
    }

    months_number = 0
    for number, name in months.items():
        if name[lang_index] in months_name:
            months_number = number
            break

    date_elements[1] = months_number  # поменяли слово на числовое обозначение месяца
    date_string = "-".join(map(str, date_elements))

    try:
        date_converted = datetime.datetime.strptime(date_string, "%d-%m-%Y").date()
    except Exception as err_message:
        print(f"Ошибка с датой {value}: {err_message}")
        date_converted = current_date()
    finally:
        date_converted = str(date_converted)

    return date_converted
    # END date_convert()


def join_clear(words: list = []) -> str:
    ''' объединяем список слов в строку заменяя спец-пробелы так, чтобы цифры ост'''

    def join_digit_word(word: str = "") -> str:
        ''' Схлопнуть спец-пробел между цифрами,
            а между словами и цифрами -- поставить обычный пробел '''
        elements = word.split()
        for i in range(len(elements) - 1):
            if elements[i].isdigit():
                if elements[i + 1].isdigit():
                    elements[i + 1] = "".join([elements[i], elements[i + 1]])
                    elements[i] = ""
        else:
            word = " ".join(elements)
        return word

    if type(words) is list:
        for i in range(len(words)):
            words[i] = join_digit_word(words[i])
        string = " ".join(words)
        string = " ".join(string.split())
    elif type(words) is str:
        string = join_digit_word(words)
    else:
        string = words  # Ничего не делаем
    return string
    # END join_clear()


def duplicate_remover(values: list = None) -> list:
    ''' Удаляем дубликаты слов в оригинальном(!) списке,
        Адрес оригинального (полученного) списка возвращается.
        Порядок слов исходный (не меняется).
        ПРИМЕЧАНИЕ: Значение i+1 в срезе values[i + 1::] может выйти за границы,
        но это не приводит к ошибке!
    '''
    if type(values) is list:
        i = 0
        while i < len(values) - 1:
            while values[i] in values[i + 1::]:
                values.pop(values.index(values[i], i + 1, ))
            else:
                i += 1
    return values
    # END duplicates_remove()


def get_maney(money_range_str: str = "") -> dict:
    ''' Выделим цифровые значения зарплаты из строки '''

    pay = {'min': 0, 'max': 0, 'cur': ''}

    if not money_range_str:
        return pay

    if " ".join(money_range_str.split()) == r'з/п не указана':
        return pay

    # Специальные пробельные символы необходимо "схлопнуть"

    special_space_symbols = {
        "NARROW_NO_BREAK_SPACE": "\u202f",
        "NO_BREAK_SPACE": "\u00a0",
        "TAB": "\t",
    }

    for key, space_code in special_space_symbols.items():
        money_range_str = money_range_str.replace(space_code, "")

    # Анализируем:

    money_words = money_range_str.split(" ")  # Разделим строку на слова
    i = 0
    while money_words:
        i += 1
        if i > 10:
            print("Выход из бесконечного цикла")
            break

        if not money_words[-1].isdigit():
            pay['cur'] = money_words[-1].strip('.')
            money_words.pop(-1)
            continue

        if money_words[0].upper() in ["ОТ", "FROM"]:
            pay['min'] = int(money_words[1])
            money_words.pop(1)
            money_words.pop(0)
            continue

        if money_words[0].upper() in ["ДО", "-", "–", "—", "--"]:
            pay['max'] = int(money_words[1])
            money_words.pop(1)
            money_words.pop(0)
            continue

        if money_words[0].isdigit():
            pay['min'] = int(money_words[0])
            money_words.pop(0)
            continue
        else:
            money_words.pop(0)
            continue

    else:
        if not pay['min']:
            pay['min'] = pay['max']
        if not pay['max']:
            pass
            # pay['max'] = pay['min']
        pass

    return pay
    # END get_maney()


if __name__ == '__main__':
    print(f"Библиотека {__name__} запущена как самостоятельный модуль.")

    print(f"Тест join_clear")

    words = [
        'abc\u00a0123\u202f444',
        '333\u00a0000\tР',
        'от\u00a0123\u202f444\u202f444\u00a0руб до 333\u00a0000\tР.',
        '',
        '333\u00a0000\tР',
        '   a', ]

    for word in words:
        print(f"{word = }")
    else:
        print(f"\n")
    print(join_clear(words))

    pass
else:
    print(f"Библиотека {__name__} импортирована.")
