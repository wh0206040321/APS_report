from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.base_page import BasePage


class ItemPage(BasePage):
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

    def go_item(self):
        """前往物料页面"""
        self.click_button('(//span[text()="计划管理"])[1]')  # 点击计划管理
        self.click_button('(//span[text()="计划基础数据"])[1]')  # 点击计划基础数据
        self.click_button('(//span[text()="物品"])[1]')  # 点击物品

    def add_item(self, material_code, material_name):
        """添加物料信息."""
        self.click_add_button()
        self.enter_texts(
            '(//label[text()="物料代码"])[1]/parent::div//input', material_code
        )
        self.enter_texts(
            '(//label[text()="物料名称"])[1]/parent::div//input', material_name
        )
        self.click_button('(//button[@type="button"]/span[text()="确定"])[4]')

    def delete_item(self, material_code):
        """删除物料信息."""
        # 定位内容为‘1测试A’的行
        self.click_button(
            f'(//span[text()="{material_code}"])[1]/ancestor::tr[1]/td[2]'
        )
        self.click_del_button()  # 点击删除
        # 点击确定
        # 找到共同的父元素
        parent = self.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()

    def check_item_exists(self, item_name):
        """检查物料是否存在."""
        try:
            self.get_find_element_xpath(f'//span[text()="{item_name}"]')
            return True
        except:
            return False

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

    def get_find_message(self):
        """获取错误信息"""
        message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="ivu-message"]//span')
            )
        )
        return message

    def add_layout(self):
        """添加布局."""
        self.click_button('//div[@class="newDropdown"]//i')
        self.click_button('//li[text()="添加新布局"]')
