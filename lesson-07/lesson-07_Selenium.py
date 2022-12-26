f''' GB / Олег Гладкий / https://gb.ru/users/3837199

Задание (домашнее):
1. Залогиниться на сайте 
2. Вывести сообщение, которое появляется после логина
   (связка логин/пароль может быть любой).
'''
url_login = 'https://www.scrapethissite.com/pages/advanced/?gotcha=login'

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# FireFox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options  # опции запуска
# Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions  # опции запуска

import time


def browser_connect(browser: str = 'firefox'):
    ''' Открываем драйвер браузера, с помощью которого будем выполнять необходимые действия в браузере
    '''

    # Размещение веб-драйверов браузеров на локальной машине.
    webdriver_firefox_path = r"C:\Programs\Anaconda3\envs\scrapy\Scripts\geckodriver.exe"
    webdriver_chrome_path  = r"C:\Programs\WebDriver\chromedriver.exe"

    # Веб-драйвер для FireFox
    if browser.upper() == 'firefox'.upper():
        service = Service(webdriver_firefox_path)
        options = Options()

        options.set_preference('permissions.default.image', 2)         # вкл. картинок (1) / откл. (2)
        options.set_preference("javascript.enabled", True)             # отключение/вкл. JavaScript
        options.set_preference('permissions.default.stylesheet', 1)    # Disable (2) or Enable (1) CSS
        options.set_preference('dom.ipc.plugins.enabled.npswf32.dll', 'false') # отключение всплывающих окон для Windows ???
        options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false') # Disable Flash (всплывающие окна, Linux) ???
        # options.add_argument('--headless')                           # откл. интерфейса

        driver = webdriver.Firefox(options=options, service=service)
        return driver

    # Web driver для Хром-а
    if browser.upper() == 'chrome'.upper():
        service = ChromeService(webdriver_chrome_path)
        options = ChromeOptions()

        driver = webdriver.Chrome(options=options, service=service)
        return driver

    # Браузер определить не удалось!
    print(f"Ошибка: неизвестный брауер: {browser}.")
    return None


with browser_connect('firefox') as driver:
    driver.get(url_login)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//form[@class='form' and @method='post']")))

    id_user = driver.find_element(By.XPATH, "//form[@class='form' and @method='post']/input[@type='text' and @class='form-control' and @name='user']")
    id_user.send_keys('admin')

    id_pass = driver.find_element(By.XPATH, "//form[@class='form' and @method='post']/input[@type='text' and @class='form-control' and @name='pass']")
    id_pass.send_keys('admin')

    id_button = driver.find_element(By.XPATH, "//form[@class='form' and @method='post']/input[@type='submit' and contains(@name, 'Login')]")
    id_button.click()

    # Переход на страницу после ввода данных авторизации
    # Ждём, когда появится объект с сообщением о результатах авторизации
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@class='container']")))
    # Получаем сообщение
    msg = driver.find_element(By.XPATH, '//div[@class="container"]/div[@class="row"]/div[contains(@class, "col-md-offset-4")]').text

    print(f"Авторизации на сайте: {url_login}\n"
          f"Прошла с результатом: \"{msg}\"")

pass
print("End")