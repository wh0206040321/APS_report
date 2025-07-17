import random
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from Pages.base_page import BasePage


class Coverage(BasePage):
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
            sleep(1)
            self.click_button(
                '(//div[@class="h-40px flex-justify-end vxe-modal-footer1 flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
            )
            sleep(1)
            # 获取勾选的资源代码
            resource = self.get_find_element_xpath(
                '//div[@id="2ssy7pog-1nb7"]//input'
            ).get_attribute("value")

            # 开始时间
            self.click_button(
                '//div[@id="dnj11joa-anmy"]//input'
            )
            self.click_button('(//em[text()="13"])[1]')
            self.click_button(
                '(//button[@class="ivu-btn ivu-btn-primary ivu-btn-small"])[1]'
            )
            start = self.get_find_element_xpath(
                '(//input[@class="ivu-input ivu-input-default ivu-input-with-suffix"])[1]'
            ).get_attribute("value")
            sleep(1)
            # 结束时间
            self.click_button(
                '//div[@id="qqs38txd-vd0r"]//input'
            )
            self.click_button('(//em[text()="20"])[2]')
            self.click_button(
                '(//button[@class="ivu-btn ivu-btn-primary ivu-btn-small"])[2]'
            )
            end = self.get_find_element_xpath(
                '(//input[@class="ivu-input ivu-input-default ivu-input-with-suffix"])[2]'
            ).get_attribute("value")

            # 时序
            self.enter_texts(
                '//div[@id="tg89jocr-6to2"]//input', f"{start};{end}"
            )
            # 时间标记
            self.click_button(
                '(//input[@class="ivu-input ivu-input-default ivu-input-with-suffix"])[3]'
            )
            self.click_button('(//em[text()="20"])[3]')
            self.click_button(
                '(//button[@class="ivu-btn ivu-btn-primary ivu-btn-small"])[3]'
            )

            # 点击下拉框
            self.click_button('//span[text()="请选择"]/following-sibling::i')
            self.click_button('//span[text()="RGB(100,255,178)"]')


            for index in range(1, 7):
                if index == 2 or index == 4 or index == 5 or index == 6:
                    self.enter_texts(f'(//input[@class="ivu-input ivu-input-default"])[{index}]', num)

            sel = self.get_find_element_xpath('//div[@class="checkBoxComp position-absolute"]/label/span')
            if sel.get_attribute("class") == "ivu-checkbox":
                self.click_button(
                    '//div[@class="checkBoxComp position-absolute"]/label'
                )
            selClass = self.get_find_element_xpath('//div[@class="checkBoxComp position-absolute"]/label/span').get_attribute("class")

            self.click_button(
                '//div[@class="h-40px flex-justify-end vxe-modal-footer1 flex-align-items-end b-t-s-d9e3f3"]//span[text()="确定"]'
            )
            return resource, selClass, start, end
