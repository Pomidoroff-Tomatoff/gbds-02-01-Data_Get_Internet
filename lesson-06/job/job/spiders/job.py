# БИБЛИОТЕКА

def join_clear(words: list = []) -> str:
    ''' объединяем список слов в строку заменяя спец-пробелы '''

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

    pay = {'min': 0, 'max': 0, 'cur': 'руб'}

    if not money_range_str:
        return pay

    if money_range_str.upper() == 'з/п не указана'.upper():
        pay['min'] = 0
        pay['max'] = 0
        pay['cur'] = ''
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

        if money_words[0].upper() == "от".upper() or \
                money_words[0].upper() == "from".upper():
            pay['min'] = int(money_words[1])
            money_words.pop(1)
            money_words.pop(0)
            continue

        if money_words[0].upper() == "до".upper() or money_words[0] == "-" or money_words[0] == "–" or money_words[
            0] == "—" or money_words[0] == "--":
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