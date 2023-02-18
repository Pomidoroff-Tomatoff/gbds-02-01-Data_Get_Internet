# Selenium для Python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Современный способ подключения драйвера с использованием службы (Service)
# FireFox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options  # опции запуска
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile  # устарело, не рекомендуется...

# Crome
from selenium.webdriver.chrome.service import Service as chromeService

# Для клавиши Пробел.
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time


def connection_browser_driver(browser: str = "firefox"):
    ''' Создаём драйвер, с помощью которого будем открывать страницу и выполнять необходимые действия
        > почему-то у меня не работае Chrome -- сразу закрвается...
    '''
    # Размещение веб-драйверов на моей машине
    webdriver_firefox_path = r"C:\Programs\Anaconda3\envs\scrapy\Scripts\geckodriver.exe"
    webdriver_chrome_path =  r"C:\Programs\WebDriver\chromedriver.exe"

    # веб-драйвер для FireFox
    if browser.upper() == "firefox".upper():

        webdriver_firefox_service = Service(webdriver_firefox_path)
        # profile = FirefoxProfile()  # --устарело, не рекомендуется использовать

        options = Options()  # экземпляр класса опций

        options.set_preference('permissions.default.image', 1)  # вкл. картинок
        # options.set_preference('permissions.default.image', 2)  # отключение картинок
        # отключение/вкл. JavaScript
        options.set_preference("javascript.enabled", True)
        # Disable (2) or Enable (1) CSS
        options.set_preference('permissions.default.stylesheet', 1)

        # отключение всплывающих окон для Windows ???
        options.set_preference('dom.ipc.plugins.enabled.npswf32.dll', 'false')
        # Disable Flash (всплывающие окна, Linux) ???
        options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

        # откл. интерфейса
        # options.add_argument('--headless')

        driver = webdriver.Firefox(options=options, service=webdriver_firefox_service)
        return driver

    # web driver для Хром-а
    if browser.upper() == "chrome".upper():
        webdriver_chrome_service = chromeService(webdriver_chrome_path)
        driver = webdriver.Chrome(service=webdriver_chrome_service)
        return driver

    # Браузер определить не удалось!
    return None

''' ПОЕХАЛИ! '''

with connection_browser_driver('firefox') as driver:
    # firefox chrome
    url = 'https://quotes.toscrape.com/scroll'
    # url = 'http://books.toscrape.com/'
    # url = 'http://quotes.toscrape.com/js/'
    driver.get(url)  # Запускаем браузер с нашей страничкой

    # Ждём, когда загрузится div со всеми цитатами 'guotes'
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "quotes")))
    # WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "row")))

    body_height = driver.execute_script("return document.body.scrollHeight")
    actions = ActionChains(driver)

    index_repeat = 0
    while (index_repeat < 2):
        driver.execute_script(f"window.scrollTo(0, {body_height})")
        # actions.send_keys(Keys.SPACE).perform()
        time.sleep(0.5)  # ждём обновления странички
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == body_height:
            index_repeat += 1
            print(f"{new_height = } repeat")
        else:
            index_repeat = 0
            body_height = new_height
            print(f"{new_height = }")
        pass

    print("Листание завершено")
    quotes = driver.find_elements(By.CLASS_NAME, 'quote')
    print(f"Количество цитат найдено: {len(quotes)=}")
    # html = driver.page_source  # html загруженной страницы

    time.sleep(10)  # полюбуемся!
    print("Браузер должен закрыться!")
    # driver.quit()  # закрываем браузер!

pass
