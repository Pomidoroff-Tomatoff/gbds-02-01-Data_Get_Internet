# Selenium для Python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Современный способ подключения драйвера с использованием службы (Service)
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service as chromeService

import time


def connection_browser_driver(browser: str = "firefox"):
    ''' Создаём драйвер, с помощью которого будем открывать страницу и выполнять необходимые действия
    '''
    # Размещение веб-драйверов
    webdriver_firefox_path = r"C:\Programs\Anaconda3\envs\scrapy\Scripts\geckodriver.exe"
    webdriver_chrome_path =  r"C:\Programs\WebDriver\chromedriver.exe"

    # веб-драйвер для FireFox
    if browser.upper() == "firefox".upper():
        webdriver_firefox_service = Service(webdriver_firefox_path)
        driver = webdriver.Firefox(service=webdriver_firefox_service)
        return driver

    # web driver для Хром-а
    if browser.upper() == "chrome".upper():
        webdriver_chrome_service = chromeService(webdriver_chrome_path)
        driver = webdriver.Chrome(service=webdriver_chrome_service)
        return driver


'''
ПОЕХАЛИ!
'''

url = 'https://quotes.toscrape.com/scroll'
driver = connection_browser_driver()
driver.get(url)

# Ждём, когда загрузится div со всеми цитатами 'guotes'
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "quotes")))

# Получим все страницы бесконечного сайта
# -- Получим начальную высоту блока body

body_height = driver.execute_script("return document.body.scrollHeight")
print(f"{body_height = }")
while True:
    driver.execute_script(f"window.scrollTo(0, {body_height})")
    time.sleep(1)  # ждём обновления странички
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == body_height:
        break
    else:
        body_height = new_height
        print(f"{new_height = }")
    pass

print("Листание завершено")
quotes = driver.find_elements(By.CLASS_NAME, 'quote')
print(f"{len(quotes)=}")

# login_btn.click()  # и кликнули

# html = driver.page_source  # html загруженной страницы
# quotes = driver.find_elements(By.XPATH, '//*[@class="quote"]')
# print(f"Количество цитат найдено: {len(quotes)=}")

time.sleep(3)  # полюбуемся!
driver.quit()  # закрываем браузер!
