import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class DateDriver:
    url = "http://wkawka.vicp.net:27890"
    driver_path = 'D:/Program Files/Python310/chromedriver.exe'
    username = 'hongaoqing'
    password = 'Qw123456'  # 1234qweR
    planning = '金属（演示）'
    URL_RETRY_WAIT = int(os.getenv("URL_RETRY_WAIT", 60))