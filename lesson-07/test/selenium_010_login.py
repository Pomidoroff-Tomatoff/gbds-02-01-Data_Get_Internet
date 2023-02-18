# Selenium для Python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Современный способ подключения драйвера с использованием службы (Service)
from selenium.webdriver.firefox.service import Service as firefoxService
from selenium.webdriver.chrome.service import Service as chromeService

import time


def connection_browser_driver(browser: str = "firefox"):
    ''' Создаём драйвер, с помощью которого будем открывать страницу и выполнять необходимые действия
    '''
    # Размещение веб-драйверов
    webdriver_firefox_path = r"C:\Programs\Anaconda3\envs\scrapy\Scripts\geckodriver.exe"
    webdriver_chrome_path =  r"C:\Programs\WebDriver\chromedriver.exe"

    # Веб-драйвер для FireFox
    if browser.upper() == "firefox".upper():
        webdriver_firefox_service = firefoxService(webdriver_firefox_path)
        driver = webdriver.Firefox(service=webdriver_firefox_service)
        return driver

    # Web driver для Хром-а
    if browser.upper() == "chrome".upper():
        webdriver_chrome_service = chromeService(webdriver_chrome_path)
        driver = webdriver.Chrome(service=webdriver_chrome_service)
        return driver


'''
ПОЕХАЛИ!
'''
url = 'https://quotes.toscrape.com/login'
driver = connection_browser_driver()
driver.get(url)

# Ждём, когда загрузится страничка входа-логина, определяя по появлению объекта "username"
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'username')))

# ИМЯ: находим поле "username" и вводим имя пользователя "admin"
login_name = driver.find_element(By.ID, 'username')
# login_name = driver.find_element(By.XPATH, "//input[@id='username']")
login_name.send_keys('admin')

time.sleep(3)  # подождём, чтобы полюбоваться результатами

# ПАПРОЛЬ: находим поле ввода пароля "password" и вводим пароль 'admin'
login_password = driver.find_element(By.ID, 'password').send_keys('admin')
# login_password = driver.find_element('id', 'password').send_keys('admin')
# login_password.send_keys('admin')

time.sleep(3)  # подождём, чтобы полюбоваться

# Находим кнопку отправки данных на сервер и нажимаем её (кликаем)
login_btn = driver.find_element(By.XPATH, '//input[@value="Login"]').click()
# login_btn.click()  # и кликнули

html = driver.page_source  # html загруженной страницы
# quotes = driver.find_elements(By.XPATH, '//*[@class="quote"]')
quotes = driver.find_elements(By.CLASS_NAME, 'quote')
print(f"Количество цитат найдено: {len(quotes)=}")

time.sleep(3)  # полюбуемся!
driver.quit()  # закрываем браузер!
