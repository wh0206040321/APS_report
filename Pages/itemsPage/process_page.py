from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from Pages.base_page import BasePage


class ProcessPage(BasePage):
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

    def adds_process(self, name, number):
        self.click_add_button()  # 检查点击添加
        # 输入工序代码
        self.enter_texts('(//label[text()="工序代码"])[1]/parent::div//input', f"{name}")
        self.enter_texts('(//label[text()="工序名"])[1]/parent::div//input', f"{name}")
        # 表示顺序数字框输入文字字母符号数字
        element = self.get_find_element_xpath(
            '(//label[text()="表示顺序"])[1]/parent::div//input'
        )
        # 全选后删除
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        sleep(1)
        self.enter_texts(
            '(//label[text()="表示顺序"])[1]/parent::div//input', f"{number}"
        )
        # 点击确定
        self.click_button('(//button[@type="button"]/span[text()="确定"])[4]')

    def add_layout(self):
        """添加布局."""
        self.click_button('//div[@class="newDropdown"]//i')
        self.click_button('//li[text()="添加新布局"]')

    def add_input_all(self, name, num):
        """输入框全部输入保存"""
        if name != "":
            # 输入代码
            self.enter_texts('(//label[text()="工序代码"])[1]/parent::div//input', f"{name}")
            self.enter_texts('(//label[text()="工序名"])[1]/parent::div//input', f"{name}")
            # 显示颜色下拉框
            self.click_button('(//label[text()="显示颜色"])[1]/parent::div//i')
            # 显示颜色
            self.click_button('//span[text()="RGB(100,255,178)"]')
            ele = self.get_find_element_xpath(
                '(//label[text()="表示顺序"])[1]/parent::div//input'
            )
            ele.send_keys(Keys.CONTROL, "a")
            ele.send_keys(Keys.DELETE)
            # 显示顺序框输入文字字母符号数字
            self.enter_texts(
                '(//label[text()="表示顺序"])[1]/parent::div//input', f"{num}"
            )
            self.enter_texts('(//label[text()="备注"])[1]/parent::div//input', f"{name}")
            ele = self.get_find_element_xpath(
                '//label[text()="无效标志"]/following-sibling::div/label/span'
            )
            if ele.get_attribute("class") == 'ivu-checkbox':
                ele.click()

            self.click_button('(//button[@type="button"]/span[text()="确定"])[4]')