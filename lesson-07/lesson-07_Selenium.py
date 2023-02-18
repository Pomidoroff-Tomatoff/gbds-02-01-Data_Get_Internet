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
from selenium.webdriver.support.ui import WebDriverWait  # для явного ожидания (Explisit)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # класс для ожидания
# Исключения
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException

# Firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions  # опции запуска
from webdriver_manager.firefox import GeckoDriverManager
# Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions  # опции запуска
from webdriver_manager.chrome import ChromeDriverManager
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

    # ВКУСНОЕ: использование ...DriverManager для автоматической загрузки и установки драйвера.
    #   https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
    #   https://github.com/SergeyPirogov/webdriver_manager#use-with-chrome
    #   webdriver-manager 3.8.5:
    #   https://pypi.org/project/webdriver-manager/
    #   Работает (пока) только для Хрома и ЛисаОгненного (именно эта версия, а не webdrivermanager 0.10.0)

    # FireFox, веб-драйвер для Огненного Лиса
    if browser.upper() == 'firefox'.upper():
        service = FirefoxService(GeckoDriverManager().install())
        # service = FirefoxService(webdriver_firefox_path)  # ручной режим
        options = FirefoxOptions()
        # Опции:
        options.page_load_strategy = 'eager'  # Стратегия загрузки ('normal', 'eager', 'none')
        # Опции, стандартные:
        options.set_preference('permissions.default.image', 1)         # вкл. картинок (1) / откл. (2)
        options.set_preference("javascript.enabled", True)             # отключение/вкл. JavaScript
        options.set_preference('permissions.default.stylesheet', 1)    # Disable (2) or Enable (1) CSS
        options.set_preference('dom.ipc.plugins.enabled.npswf32.dll', 'false') # отключение всплывающих окон для Windows ???
        options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false') # Disable Flash (всплывающие окна, Linux) ???
        # Опции НЕ стандартные:
        options.headless = False  # options.add_argument('--headless')  # откл. интерфейса
        # Драйвер
        driver = webdriver.Firefox(options=options, service=service)

    # Chrome, Web driver для Хром-а
    elif browser.upper() == 'chrome'.upper():
        service = ChromeService(ChromeDriverManager().install())
        # service = ChromeService(webdriver_chrome_path)  # Ручной режим
        options = ChromeOptions()
        # Опции:
        options.page_load_strategy = 'eager'  # Стратегия загрузки ('normal', 'eager', 'none')
        # Опции НЕ стандартные:
        options.headless = False  # options.add_argument('--headless')  # откл. интерфейса / Runs Chrome in headless mode.
        # options.add_argument('--no-sandbox')     # Bypass OS security model
        options.add_argument('--disable-gpu')    # applicable to windows os only
        options.add_argument('start-maximized')  # Окно на весь экран
        options.add_argument('disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        # Драйвер
        driver = webdriver.Chrome(options=options, service=service)

    # MS Edge, Web driver для Эдж-а (не работает пока)
    elif browser.upper() == 'edge'.upper():
        service = EdgeService(webdriver_edge_path)
        options = EdgeOptions()
        # Опции
        options.page_load_strategy = 'eager'  # Стратегия загрузки ('normal', 'eager', 'none')
        # Драйвер
        driver = webdriver.Edge(options=options, service=service)

    # MS Internet Explorer, Web driver для классики, MS IE (не работает пока)
    elif browser.upper() == 'ie'.upper():
        service = IeService(webdriver_ie_path)
        options = IeOptions()
        # Опции
        options.page_load_strategy = 'eager'  # Стратегия загрузки ('normal', 'eager', 'none')
        # Драйвер
        driver = webdriver.Ie(options=options, service=service)

    # Браузер определить не удалось!
    else:
        print(f"Ошибка: неизвестный браузер: {browser}.")
        return None

    # ОЖИДАНИЕ
    # Режим явного ожидания объектов Web-драйвера:
    # -- Будет работать, только если использовать вызов
    #      driver.wait.until([условия и объект поиска])
    # -- Зададим параметры явного ожидания как атрибут wait объекта driver
    driver.wait = WebDriverWait(
        driver,
        timeout=180,
        poll_frequency=1,
        ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]
    )
    # Режим НЕ-явного ожидания:
    # будет действовать на все вызовы driver.find_element(...) и подобное
    driver.implicitly_wait(60)

    driver.maximize_window()  # можно так распахнуть на весь экран именно здесь?
    return driver


# Поехали!
# Поддерживаемы браузеры: Firefox, Chrome
# не работающие в настоящий момент браузеры: Edge, IE...

with browser_connect(browser = (browser_name := 'Firefox')) as driver:
    driver.get(url_login)

    # Ждём загрузки страницы авторизации, но без загрузки необязательных объектов,
    # таких как изображения, css и так далее...
    driver.wait.until(EC.presence_of_element_located((By.XPATH, "//form[@class='form' and @method='post']")))

    # Авторизация
    id_user = driver.find_element(By.XPATH, "//form[@class='form' and @method='post']/input[@type='text' and @class='form-control' and @name='user']")
    id_user.send_keys('admin')

    time.sleep(1)

    id_pass = driver.find_element(By.XPATH, "//form[@class='form' and @method='post']/input[@type='text' and @class='form-control' and @name='pass']")
    id_pass.send_keys('admin')

    time.sleep(1)

    id_button = driver.find_element(By.XPATH, "//form[@class='form' and @method='post']/input[@type='submit' and contains(@name, 'Login')]")
    id_button.click()

    # Сайт переводит нас на страницу авторизованного пользователя
    # Ждём, когда появится объект с сообщением о результатах авторизации
    if True:  # неЯвное ожидание
        msg = driver.find_element(By.XPATH, '//div[@class="container"]/div[@class="row"]/div[contains(@class, "col-md-offset-4")]')
        msg_wait = 'Implicitly wait'
    else:    # Явное ожидание, параметры заданы ранее...
        msg = driver.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="container"]/div[@class="row"]/div[contains(@class, "col-md-offset-4")]')))
        msg_wait = 'Explicitly wait'

    # приехали!

    print(f"\nРезультат авторизации: \"{msg.text}\"\n\n"
          f"сайт: {url_login}\n"
          f"браузер: {browser_name}\n"
          f"ожидание: {msg_wait}\n")
    time.sleep(3)  # любуемся на страничку, а далее менеджер контекста with всё закрывает...


pass
print("End")
