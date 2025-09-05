from time import sleep
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.base_page import BasePage
from Pages.itemsPage.adds_page import AddsPages


class RolePage(BasePage):
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

    def get_find_message(self):
        """获取错误信息"""
        message = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="ivu-message"]//span')
            )
        )
        return message.text

    def get_message(self):
        """获取信息"""
        message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="el-message el-message--success"]/p')
            )
        )
        return message.text

    def right_refresh(self, name="角色管理"):
        """右键刷新."""
        but = self.get_find_element_xpath(f'//div[@class="scroll-body"]/div[.//div[text()=" {name} "]]')
        but.click()
        # 右键点击
        ActionChains(self.driver).context_click(but).perform()
        self.click_button('//li[text()="刷新"]')
        self.wait_for_loading_to_disappear()

    # 等待加载遮罩消失
    def wait_for_loading_to_disappear(self, timeout=10):
        """
        显式等待加载遮罩元素消失。

        参数:
        - timeout (int): 超时时间，默认为10秒。

        该方法通过WebDriverWait配合EC.invisibility_of_element_located方法，
        检查页面上是否存在class中包含'el-loading-mask'且style中不包含'display: none'的div元素，
        以此判断加载遮罩是否消失。
        """
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(
                (By.XPATH, '//div[contains(@class, "el-loading-mask") and not(contains(@style, "display: none"))]')
            )
        )
        sleep(1)

    def click_all_button(self, name):
        """点击按钮."""
        self.click_button(f'//div[@class="flex-alignItems-center background-ffffff h-36px w-b-100 toolbar-container"]//p[text()="{name}"]')

    def add_role(self, name, module):
        """添加角色管理."""
        add = AddsPages(self.driver)
        self.click_all_button("新增")
        list_ = [
            '//div[label[text()="角色代码"]]//input',
            '//div[label[text()="角色名称"]]//input',
        ]
        add.batch_modify_input(list_, name)

        list_sel = [
            {"select": '//div[label[text()="计划单元名称"]]//div[@class="ivu-select-selection"]',
             "value": f'//li[text()="{module}"]'},
        ]
        add.batch_modify_select_input(list_sel)

    def update_role(self, before_name, after_name, module):
        """添加角色管理."""
        add = AddsPages(self.driver)
        self.select_input(before_name)
        sleep(1)
        self.click_button(f'//table[@class="vxe-table--body"]//tr/td[2]//span[text()="{before_name}"]')
        self.click_all_button("编辑")
        list_ = [
            '//div[label[text()="角色名称"]]//input',
        ]
        add.batch_modify_input(list_, after_name)

        list_sel = [
            {"select": '//div[label[text()="计划单元名称"]]//div[@class="ivu-select-selection"]',
             "value": f'//li[text()="{module}"]'},
        ]
        add.batch_modify_select_input(list_sel)

    def select_input(self, name):
        """选择输入框."""
        self.enter_texts('//div[div[p[text()="角色代码"]]]//input', name)

    def click_sel_button(self):
        """点击查询按钮."""
        self.click(By.XPATH, '//p[text()="查询"]')

    def loop_judgment(self, xpath):
        """循环判断"""
        eles = self.finds_elements(By.XPATH, xpath)
        code = [ele.text for ele in eles]
        return code

