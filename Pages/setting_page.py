from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.base_page import BasePage


class SettingPage(BasePage):
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

    def add_layout(self):
        """添加布局."""
        self.click_button('//div[@class="newDropdown"]//i')
        self.click_button('//li[text()="添加新布局"]')

    def add_pivot_table(self):
        """添加透视表."""
        self.click_button('//div[@class="newDropdown"]//i')
        self.click_button('//li[text()="添加透视表"]')

    def click_setting_button(self):
        """点击设置按钮."""
        self.click_button('(//i[@style="cursor: pointer;"])[2]')

    def get_find_message(self):
        """获取错误信息"""
        message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="ivu-message"]//span')
            )
        )
        return message

    def click_ref_button(self):
        """点击刷新按钮."""
        self.click(By.XPATH, '//p[text()="刷新"]')

    def add_statistics(self, num='', data="", name="", code1='', code2='', code3=''):
        """添加统计."""
        self.click_button('(//i[@style="cursor: pointer;"])[3]')
        self.click_button('//div[./span[text()=" 统计 "]]//i')
        self.click_button(f'//h2[text()="图表"]/following-sibling::div/div[{num}]')
        if data:  # 如果 data 不为空，则输入
            self.click_button('//h2[text()="数据源"]/following-sibling::div[1]//i')
            sleep(1)
            self.click_button(f'//li[text()="{data}" and @class="ivu-select-item"]')
        if name:  # 如果 name 不为空，则输入
            self.enter_texts('//span[text()="图表名"]/following-sibling::div[1]//input', f"{name}")
        if code1 != '' and code2 != '':
            # 定义文本元素和目标输入框的 XPath
            text_elements = [
                f'//span[text()="{code1}"]',
                f'//span[text()="{code2}"]',
            ]

            input_elements = [
                '//h3[text()="X轴(维度)"]/following-sibling::div[1]',
                '//h3[text()="Y轴(数值)"]/following-sibling::div[1]',
            ]

            # 使用循环进行拖放操作
            for text_xpath, input_xpath in zip(text_elements, input_elements):
                sleep(1)
                text_element = self.get_find_element_xpath(text_xpath)
                input_element = self.get_find_element_xpath(input_xpath)
                ActionChains(self.driver).drag_and_drop(text_element, input_element).perform()

            sleep(1)
        elif code2 != '' and code3 != '':
            # 定义文本元素和目标输入框的 XPath
            text_elements = [
                f'//span[text()="{code2}"]',
                f'//span[text()="{code3}"]',
            ]

            input_elements = [
                '//h3[text()="Y轴(数值)"]/following-sibling::div[1]',
                '//h3[text()="分组"]/following-sibling::div[1]',
            ]

            # 使用循环进行拖放操作
            for text_xpath, input_xpath in zip(text_elements, input_elements):
                text_element = self.get_find_element_xpath(text_xpath)
                input_element = self.get_find_element_xpath(input_xpath)
                ActionChains(self.driver).drag_and_drop(text_element, input_element).perform()

    def add_lable(self, name=''):
        """添加标签."""
        self.click_button('(//i[@style="cursor: pointer;"])[4]')
        self.click_button('(//i[@class="el-tooltip ivu-icon ivu-icon-md-add"])[2]')
        if name:
            self.enter_texts('//div[text()="标签名："]/following-sibling::div/input', f"{name}")
