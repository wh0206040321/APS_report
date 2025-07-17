import random

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from Pages.base_page import BasePage


class OrderPage(BasePage):
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

    def add_order(self, code, order_item):
        self.click_add_button()
        # 填写订单代码
        self.enter_texts('(//label[text()="订单代码"])[1]/parent::div//input', code)
        # 物料
        self.click_button('//label[text()="物料"]/parent::div/div//i')
        self.click_button(
            f'(//table[.//td[2]//span[text()="{order_item}"]])[2]//td[2]//span[text()="{order_item}"]'
        )
        self.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[last()]/button[1]'
        )

        # 填写交货期
        self.click_button('(//label[text()="交货期"])[1]/parent::div//input')
        self.click_button(
            '//div[@class="ivu-select-dropdown ivu-date-picker-transfer setZindex"]//div[@class="ivu-date-picker-header"]//span[@class="ivu-picker-panel-icon-btn ivu-date-picker-next-btn ivu-date-picker-next-btn-arrow"]/i'
        )
        self.click_button(
            '//div[@class="ivu-select-dropdown ivu-date-picker-transfer setZindex"]//div[@class="ivu-date-picker-cells"]//em[text()="20"]'
        )
        self.click_button(
            '//div[@class="ivu-select-dropdown ivu-date-picker-transfer setZindex"]//div[@class="ivu-picker-confirm"]//button[3]'
        )

        # 计划数量
        num = self.get_find_element_xpath(
            '(//label[text()="计划数量"])[1]/parent::div//input'
        )
        num.send_keys(Keys.CONTROL, "a")
        num.send_keys(Keys.BACK_SPACE)
        self.enter_texts('(//label[text()="计划数量"])[1]/parent::div//input', "200")

        # 点击确定
        self.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[5]/button[1]'
        )

    def delete_order(self, code):
        # 判断是否存在该订单
        elements = self.driver.find_elements(
            By.XPATH, f'(//span[text()="{code}"])[1]/ancestor::tr[1]/td[2]'
        )
        if not elements:
            print(f"订单 {code} 不存在，跳过删除。")
            return  # 跳过删除操作

        self.click_button(f'(//span[text()="{code}"])[1]/ancestor::tr[1]/td[2]')
        self.click_del_button()  # 点击删除按钮

        # 查找确认框并点击“确定”
        parent = self.get_find_element_class("ivu-modal-confirm-footer")
        if parent is None:
            print("未找到确认框，可能弹窗未出现或页面加载失败。")
            return

        all_buttons = parent.find_elements(By.TAG_NAME, "button")
        if len(all_buttons) > 1:
            all_buttons[1].click()  # 点击第二个按钮（确定）
        else:
            print("确认按钮数量不足，无法点击。")

    def check_order_exists(self, order_name):
        try:
            self.get_find_element_xpath(f'//span[text()="{order_name}"]')
            return True
        except:
            return False

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

    def click_setting_button(self):
        """点击设置按钮."""
        self.click_button('(//i[@style="cursor: pointer;"])[2]')

    def add_layout(self):
        """添加布局."""
        self.click_button('//div[@class="newDropdown"]//i')
        self.click_button('//li[text()="添加新布局"]')
