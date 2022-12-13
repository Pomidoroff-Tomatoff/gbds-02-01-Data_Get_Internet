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


words = [
    'abc\u00a0123\u202f444',
    '333\u00a0000\tР',
    'от\u00a0123\u202f444\u202f444\u00a0руб до 333\u00a0000\tР.',
    '',
    '333\u00a0000\tР',
    '   a',
]

for word in words:
    print(f"{word = }")
else:
    print(f"\n")
    print(join_clear(words))

    words.applay

pass
