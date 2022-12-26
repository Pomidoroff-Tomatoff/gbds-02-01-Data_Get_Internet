''' GB / Олег Гладкий / https://gb.ru/users/3837199
Курс:
    Методы сбора и обработки данных из сети Интернет,
    Урок 7. Парсинг данных. Selenium в Python
    https://gb.ru/lessons/262704/homework

Задание (домашнее), из методички:
1. Залогиниться на сайте 
2. Вывести сообщение, которое появляется после логина
   (связка логин/пароль может быть любой).

Внимание, ошибка на странице:
    Errors Detected in HTTP Request:

Решение:
    Эта страница с ошибкой загрузки неких изображений. Для выполнения задания необходимо:
    -- либо Отключить загрузку изображений (не желательно);
    -- либо переключить Стратегию загрузки:
        'normal' -- Ждём загрузки всех элементов.
        'eager'  -- Частично: DOM загружен полностью, но другие ресурсы, такие как Картинки, могут ещё подгружаться.
        'none'   -- Не блокирует WebDriver по всему возможному...
                    (в том числе изображений): режим "Стратегия загрузки" ('normal', 'eager', 'none')
'''

url_login = 'https://www.scrapethissite.com/pages/advanced/?gotcha=login'

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # класс для ожидания
# Исключения
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException

# FireFox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options  # опции запуска
# Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions  # опции запуска
# Edge
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions  # опции запуска
# IE
from selenium.webdriver.ie.service import Service as IeService
from selenium.webdriver.ie.options import Options as IeOptions  # опции запуска

import time


def browser_connect(browser: str = 'firefox'):
    ''' Открываем драйвер браузера, с помощью которого будем выполнять необходимые действия в браузере
    '''

    # Размещение веб-драйверов браузеров на локальной машине.
    webdriver_firefox_path = r"C:\Programs\Anaconda3\envs\scrapy\Scripts\geckodriver.exe"
    webdriver_chrome_path = r"C:\Programs\WebDriver\chromedriver.exe"
    webdriver_edge_path = r"C:\Programs\WebDriver\msedgedriver.exe"
    webdriver_ie_path = r"C:\Programs\WebDriver\IEDriverServer.exe"

    # FireFox, веб-драйвер для
    if browser.upper() == 'firefox'.upper():
        service = Service(webdriver_firefox_path)
        options = Options()

        # Опции драйвера
        options.page_load_strategy = 'eager'  # Стратегия загрузки ('normal', 'eager', 'none')
        # Стандрартные параметры:
        options.set_preference('permissions.default.image', 1)         # вкл. картинок (1) / откл. (2)
        options.set_preference("javascript.enabled", True)             # отключение/вкл. JavaScript
        options.set_preference('permissions.default.stylesheet', 1)    # Disable (2) or Enable (1) CSS
        options.set_preference('dom.ipc.plugins.enabled.npswf32.dll', 'false') # отключение всплывающих окон для Windows ???
        options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false') # Disable Flash (всплывающие окна, Linux) ???
        # Не стандартные: откл. интерфейса
        # options.add_argument('--headless')

        driver = webdriver.Firefox(options=options, service=service)

    # Chrome, Web driver для Хром-а
    elif browser.upper() == 'chrome'.upper():
        service = ChromeService(webdriver_chrome_path)
        options = ChromeOptions()

        # Опции
        options.page_load_strategy = 'eager'  # Стратегия загрузки ('normal', 'eager', 'none')

        driver = webdriver.Chrome(options=options, service=service)

    elif browser.upper() == 'edge'.upper():
        service = EdgeService(webdriver_edge_path)
        options = EdgeOptions()
        # Опции
        options.page_load_strategy = 'eager'  # Стратегия загрузки ('normal', 'eager', 'none')
        driver = webdriver.Edge(options=options, service=service)

    elif browser.upper() == 'ie'.upper():
        service = IeService(webdriver_ie_path)
        options = IeOptions()
        # Опции
        options.page_load_strategy = 'eager'  # Стратегия загрузки ('normal', 'eager', 'none')
        driver = webdriver.Ie(options=options, service=service)

    else:
        # Браузер определить не удалось!
        print(f"Ошибка: неизвестный браузер: {browser}.")
        return None

    # ОЖИДАНИЕ
    # Режим явного ожидания объектов Web-драйвера, будет работать,
    # только если использовать вызов driver.wait.until([условия и объект поиска])
    driver.wait = WebDriverWait(driver,
        timeout=60, poll_frequency=1,
        ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])

    # Режим НЕ-явного ожидания:
    # будет действовать на все вызовы driver.find_element(...) и подобное
    driver.implicitly_wait(60)

    return driver


# Поехали! Поддерживаемы браузеры: FireFox, Chrome, Edge, IE... Edge и IE не работают у меня (почему-то)
browser_name = 'FireFox'

with browser_connect(browser_name) as driver:
    driver.get(url_login)

    # Ждём загрузки страницы авторизации, но без загрузки необязательных объектов,
    # таких как изображения, css и так далее...
    driver.wait.until(EC.presence_of_element_located((By.XPATH, "//form[@class='form' and @method='post']")))

    # Авторизация
    id_user = driver.find_element(By.XPATH, "//form[@class='form' and @method='post']/input[@type='text' and @class='form-control' and @name='user']")
    id_user.send_keys('admin')

    id_pass = driver.find_element(By.XPATH, "//form[@class='form' and @method='post']/input[@type='text' and @class='form-control' and @name='pass']")
    id_pass.send_keys('admin')

    time.sleep(1)

    id_button = driver.find_element(By.XPATH, "//form[@class='form' and @method='post']/input[@type='submit' and contains(@name, 'Login')]")
    id_button.click()

    # Сайт переводит нас на страницу после ввода данных авторизации
    # Ждём, когда появится объект с сообщением о результатах авторизации
    msg = driver.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="container"]/div[@class="row"]/div[contains(@class, "col-md-offset-4")]')))

    print(f"\nРезультат авторизации: \"{msg.text}\"\n\n"
          f"сайт: {url_login}\n"
          f"браузер: {browser_name}")
    time.sleep(3)  # любуемся на страничку и закрываем её...

pass
print("End")
