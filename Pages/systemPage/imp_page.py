from time import sleep
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.base_page import BasePage


class ImpPage(BasePage):
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
        message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="el-message el-message--success"]/p')
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

    def right_refresh(self, name="导入设置"):
        """右键刷新."""
        but = self.get_find_element_xpath(f'//div[@class="scroll-body"]/div[.//div[text()=" {name} "]]')
        but.click()
        # 右键点击
        ActionChains(self.driver).context_click(but).perform()
        self.click_button('//li[text()=" 刷新"]')
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

    def click_impall_button(self, name):
        """点击导入页面各种按钮"""
        self.click_button(f'//div[@class="flex-alignItems-center background-ffffff h-36px w-b-100 m-l-12 toolbar-container"]//p[text()="{name}"]')

    def del_all(self, value=[]):
        """批量删除"""
        for v in value:
            self.click_button('//div[@class="flex-alignItems-center background-ffffff h-36px w-b-100 m-l-12 toolbar-container"]//input[@class="ivu-select-input"]')
            self.click_button(f'//div[@class="d-alIt-ba cursor-pointer m-l-22 col-black font14"]//li[text()="{v}"]')
            self.click_impall_button("删除")
            self.click_button('//div[@class="ivu-modal-confirm-footer"]//span[text()="确定"]')

        self.click_impall_button("保存")

    def add_imp(self, name):
        """添加导入方案"""
        self.click_impall_button("新增")
        self.enter_texts('//div[label[text()="名称"]]//input', name)
        self.click_button('//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"]//span[text()="确定"]')

    def copy_(self, name='', copy_name=''):
        """复制导入方案"""
        self.click_impall_button("复制")
        if name != '':
            self.click_button('//div[label[text()="源方案"]]//input[@type="text"]')
            self.click_button(f'(//ul/li[text()="{name}"])[2]')
        if copy_name != '':
            self.enter_texts('//div[label[text()="目的方案"]]//input[@type="text"]', copy_name)
        self.click_button('(//div[@class="ivu-modal-footer"]//span[text()="确定"])[2]')
