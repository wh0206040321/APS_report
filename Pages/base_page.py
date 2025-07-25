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
            self.safe_screenshot(reason="find_element_timeout", test_name="test")
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
                self.safe_screenshot("click_timeout", test_name="test")
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
            self.safe_screenshot("click_timeout", test_name="test")
            raise Exception(f"点击失败：{e}")

    def enter_text(self, by, value, text, wait_time=10):
        """在指定位置输入文本，等待元素可见后操作."""
        element = WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located((by, value))
        )
        element.clear()  # 清空文本框
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

    def safe_screenshot(self, reason="", test_name=""):
        """
        截图当前页面并附加到 Allure 报告

        此函数旨在当测试过程中遇到需要记录的事件时，对当前页面进行截图，并将截图自动附加到 Allure 测试报告中
        它通过检查驱动程序是否已进行过截图来避免重复截图，确保报告的整洁和高效

        参数:
            reason (str): 进行截图的原因，作为截图文件名的一部分，默认为空字符串
            test_name (str): 测试用例的名称，用于截图文件命名和 Allure 报告中分类截图，默认为空字符串
        """
        from datetime import datetime
        import os
        from Utils.path_helper import get_report_dir
        import allure

        # 检查驱动程序是否已进行过截图，避免重复
        if getattr(self.driver, "_has_screenshot", False):
            return
        self.driver._has_screenshot = True

        # 生成时间戳，用于截图文件命名
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 构造唯一的截图文件名
        filename = f"{test_name}_{reason}_{id(self.driver)}_{ts}.png"
        # 获取截图存储目录
        folder = get_report_dir("screenshots")
        # 组合文件路径
        filepath = os.path.join(folder, filename)

        try:
            # 尝试保存截图
            self.driver.save_screenshot(filepath)
            logging.warning(f"截图已保存：{filepath}")

            # 👉 Allure 报告中附加截图
            allure.attach.file(
                filepath,
                name=f"{test_name}_{reason}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            # 如果截图失败，记录日志
            logging.warning(f"截图失败：{e}")
