# Selenium для Python

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
t_start = time.time()

# Для клавиши Пробел.
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

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


''' ПОЕХАЛИ! '''
# firefox chrome
with browser_connect('firefox') as driver:
    url = 'http://quotes.toscrape.com/js-delayed/'
    driver.get(url)  # Запускаем браузер с нашей страничкой

    # Явное ожидание
    quotes = driver.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'quote')))

    # Неявное ожидание
    # quotes = driver.find_elements(By.CLASS_NAME, 'quote')

    print(f"Всего цитат найдено: {len(quotes)=}")
    time.sleep(5)

pass
print(f"End, run time {(time.time() - t_start):.0f} sec.")
