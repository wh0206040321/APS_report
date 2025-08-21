# pages/base_page.py
import logging
from time import sleep

import allure
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        try:
            driver.maximize_window()
        except Exception as e:
            print(f"⚠️ 无法最大化窗口：{e}")
            driver.set_window_size(1920, 1080)  # 使用默认分辨率

    def find_element(self, by, value, wait_time=10):
        """查找单个元素，失败时截图"""
        logging.info(f"查找元素：{by} = {value}")
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            logging.warning(f"❌ 未找到元素：{by} = {value}，等待超时 {wait_time}s")
            raise

    def finds_elements(self, by, value):
        """查找多个元素，并返回这些元素."""
        logging.info(f"查找元素：{by} = {value}")
        return self.driver.find_elements(by, value)

    def click(self, by_or_element, value=None, wait_time=10):
        if value is not None:
            by = by_or_element
            logging.info(f"点击元素：By = {by}, Value = {value}")
            try:
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.element_to_be_clickable((by, value))
                )
            except TimeoutException:
                logging.warning(f"❌ 点击超时：元素 {by} = {value} 未在 {wait_time} 秒内变为可点击")
                raise TimeoutException(f"点击失败，找不到元素：{by} = {value}")
        else:
            logging.info("点击元素：WebElement 对象")
            element = by_or_element

        try:
            element.click()
        except ElementClickInterceptedException:
            logging.warning("⚠️ 原生点击被拦截，尝试使用 JS 点击")
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            logging.warning(f"点击失败：{e}")
            raise Exception(f"点击失败：{e}")

    def enter_text(self, by, value, text, wait_time=10):
        """在指定位置输入文本，等待元素可见后操作."""
        element = WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located((by, value))
        )
        sleep(0.5)
        element.send_keys(text)

    def navigate_to(self, url):
        """导航到指定URL，若提供wait_for_element，则等待该元素加载完成."""
        self.driver.get(url)

    def close(self):
        """关闭浏览器驱动."""
        self.driver.quit()

    def has_fail_message(self):
        """获取服务器内部错误."""
        mes = self.finds_elements(By.XPATH, '//div[@class="ivu-modal-content"]//div[text()=" 对不起,在处理您的请求期间,产生了一个服务器内部错误! "]')
        return bool(mes)  # 有元素返回 True，无元素返回 False
