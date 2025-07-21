import random
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from Pages.base_page import BasePage


class Calendar(BasePage):
    def __init__(self, driver):
        super().__init__(driver)  # 调用基类构造函数

    def click_add_button(self):
        """点击添加按钮."""
        self.click(By.XPATH, '//p[text()="新增"]')

    def click_edi_button(self):
        """点击修改按钮."""
        self.click(By.XPATH, '//p[text()="编辑"]')

    def click_del_button(self):
        """点击删除按钮."""
        self.click(By.XPATH, '//p[text()="删除"]')

    def click_sel_button(self):
        """点击查询按钮."""
        self.click(By.XPATH, '//p[text()="查询"]')

    def click_ref_button(self):
        """点击刷新按钮."""
        self.click(By.XPATH, '//p[text()="刷新"]')

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

    def get_find_element_class(self, classname):
        """获取用户头像元素，返回该元素。如果元素未找到，返回None。"""
        try:
            return self.find_element(By.CLASS_NAME, classname)
        except NoSuchElementException:
            return None

    def get_error_message(self, xpath):
        """获取错误消息元素，返回该元素。如果元素未找到，返回None。"""
        try:
            return self.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return None

    def add_layout(self):
        """添加布局."""
        self.click_button('//div[@class="newDropdown"]//i')
        self.click_button('//li[text()="添加新布局"]')

    def add_input_all(self, num):
        """输入框全部输入保存"""
        if num != "":
            # 点击资源
            self.click_button(
                '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[1]'
            )
            # 勾选框
            random_int = random.randint(2, 10)
            sleep(1)
            self.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int}]')

            self.click_button(
                '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
            )
            sleep(1)
            resource = self.get_find_element_xpath('//label[text()="资源"][1]/parent::div//input').get_attribute("value")

            # 点击班次
            self.click_button(
                '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[2]'
            )
            # 勾选框
            random_int1 = random.randint(2, 10)
            sleep(1)
            self.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int1}]')
            self.click_button(
                '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
            )
            sleep(1)
            shift = self.get_find_element_xpath('//label[text()="班次"][1]/parent::div//input').get_attribute("value")

            name = ["优先级", "资源量", "备注"]
            for index, value in enumerate(name, start=1):
                ele = self.get_find_element_xpath(f'//label[text()="{value}"][1]/parent::div//input')
                ele.send_keys(Keys.CONTROL, "a")
                ele.send_keys(Keys.DELETE)
                ele.send_keys(num)


            self.click_button('(//div[text()=" 星期 "])[1]')
            self.click_button(
                '//div[@class="d-flex"]/label/span'
            )
            self.click_button(
                '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
            )
            return resource, shift

