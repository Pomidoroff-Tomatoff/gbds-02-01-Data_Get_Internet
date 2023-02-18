# Selenium 4 для Python
# DRIVER DOWNLOAD MANAGER:
#   webdriver-manager 3.8.5 (python 3.7, 3.8, 3.9, 3.10)
#   https://pypi.org/project/webdriver-manager/

from selenium import webdriver

from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions  # опции запуска
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions  # опции запуска
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions  # опции запуска
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver.ie.service import Service as IEService
from selenium.webdriver.ie.options import Options as IEOptions  # опции запуска
from webdriver_manager.microsoft import IEDriverManager

from webdriver_manager.opera import OperaDriverManager

import time


web_driver_name = 'firefox'   # OK!
# web_driver_name = 'chrome'  # OK!
# web_driver_name = 'opera'   # не работает: код примера с сайта...
# web_driver_name = 'edge'    # ошибки...
# web_driver_name = 'ie'      # проблемы с настройками зоны...



# веб-драйвер для FireFox
if web_driver_name.upper() == "firefox".upper():
    service = FirefoxService(GeckoDriverManager().install())  # webdriver-manager 3.8.5
    # service = FirefoxService(GeckoDriverManager().download_and_install('latest'))  # webdrivermanager 0.10.0
    options = FirefoxOptions()
    driver = webdriver.Firefox(options=options, service=service)


# web driver для Хром-а
if web_driver_name.upper() == "chrome".upper():
    options = ChromeOptions()
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service)


if web_driver_name.upper() == "opera".upper():   # НЕ РАБОТАЕТ
    options = ChromeOptions()
    executable_path = OperaDriverManager().install()
    driver = webdriver.Opera(executable_path=executable_path, options=options)


if web_driver_name.upper() == "edge".upper():
    options = EdgeOptions()
    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.ChromiumEdge(options=options, service=service)
    # ChromiumEdge или Edge

if web_driver_name.upper() == "ie".upper():
    service = IEService(IEDriverManager().install())
    options = IEOptions()
    driver = webdriver.Ie(options=options, service=service)


driver.get('http://books.toscrape.com/')
time.sleep(10)
driver.close()
