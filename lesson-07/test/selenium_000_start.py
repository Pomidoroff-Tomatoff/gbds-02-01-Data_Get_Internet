# Selenium для Python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Современный способ подключения драйвера с использованием службы (Service)
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.chrome.service import Service as chromeService

# Edge
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions  # опции запуска
# IE
from selenium.webdriver.ie.service import Service as IeService
from selenium.webdriver.ie.options import Options as IeOptions  # опции запуска

import time

'''
Создаём драйвер, с помощью которого будем открывать страницу и выполнять необходимые действия

firefox_gekodriver_path = r"C:\Programs\Anaconda3\pkgs\geckodriver-0.32.0-h611cf2b_0\Scripts\geckodriver.exe"
webdriver_chrome_path = r"C:\Programs\Anaconda3\envs\scrapy\Lib\site-packages\chromedriver_binary\chromedriver.exe"
'''

# Размещение веб-драйверов

webdriver_firefox_path = r"C:\Programs\Anaconda3\envs\scrapy\Scripts\geckodriver.exe"
webdriver_chrome_path = r"C:\Programs\WebDriver\chromedriver.exe"
webdriver_edge_path = r"C:\Programs\WebDriver\msedgedriver.exe"
webdriver_ie_path = r"C:\Programs\WebDriver\IEDriverServer.exe"


web_driver_name = 'firefox'
# web_driver_name = 'chrome'


# веб-драйвер для FireFox
if web_driver_name.upper() == "firefox".upper():
    webdriver_firefox_service = Service(webdriver_firefox_path)
    profile = FirefoxProfile()
    profile.set_preference('permissions.default.image', 2)  # отключение картинок
    driver = webdriver.Firefox(profile, service=webdriver_firefox_service)
    driver.get('http://books.toscrape.com/')
    time.sleep(10)
    driver.close()


# web driver для Хром-а
if web_driver_name.upper() == "chrome".upper():
    webdriver_chrome_service = chromeService(webdriver_chrome_path)
    driver = webdriver.Chrome(service=webdriver_chrome_service)
    driver.get('http://books.toscrape.com/')
    time.sleep(10)
    driver.close()

if web_driver_name.upper() == "edge".upper():
    service = EdgeService(webdriver_edge_path)
    driver = webdriver.Edge(service=service)
    driver.get('http://books.toscrape.com/')
    time.sleep(10)
    driver.close()

if web_driver_name.upper() == "ie".upper():
    service = IeService(webdriver_ie_path)
    driver = webdriver.Ie(service=service)
    driver.get('http://books.toscrape.com/')
    time.sleep(10)
    driver.close()

