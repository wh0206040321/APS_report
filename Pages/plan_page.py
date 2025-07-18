from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from Pages.base_page import BasePage


class PlanPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)  # 调用基类构造函数

    def enter_texts(self, xpath, text):
        """输入文字."""
        self.enter_text(By.XPATH, xpath, text)

    def click_button(self, xpath):
        """点击按钮."""
        self.click(By.XPATH, xpath)

    def click_plan(self):
        """点击执行计划."""
        self.click(By.XPATH, '//button[@class="m-l-10 ivu-btn ivu-btn-primary"]')

    def get_find_element_xpath(self, xpath):
        """获取用户头像元素，返回该元素。如果元素未找到，返回None。"""
        try:
            return self.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return None
