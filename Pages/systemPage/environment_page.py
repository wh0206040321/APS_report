from time import sleep

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.base_page import BasePage


class EnvironmentPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)  # 调用基类构造函数

    def enter_texts(self, xpath, text):
        """输入文字."""
        self.enter_text(By.XPATH, xpath, text)

    def click_button(self, xpath):
        """点击按钮."""
        self.click(By.XPATH, xpath)

    def get_find_element_xpath(self, xpath):
        """获取用户头像元素，返回该元素。如果元素未找到，返回None。"""
        try:
            return self.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return None

    def click_save_button(self):
        """点击保存按钮"""
        self.click_button('//p[text()="保存"]')

    def get_find_message(self):
        """获取错误信息"""
        message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="ivu-message"]//span')
            )
        )
        return message.text

    def get_check_box_status(self, xpath):
        """获取复选框状态"""
        checkbox = self.get_find_element_xpath(xpath)
        return checkbox.get_attribute("class")

    def enter_number_input(self, num=""):
        """输入 备份文件最大数 数字输入框"""
        xpth = '//div[label[text()="备份文件最大数:"]]//input'
        ele = self.get_find_element_xpath(xpth)
        ele.send_keys(Keys.CONTROL, 'a')
        ele.send_keys(Keys.DELETE)
        if num != "":
            self.enter_texts(xpth, num)
        value = self.get_find_element_xpath(xpth).get_attribute("value")
        return value