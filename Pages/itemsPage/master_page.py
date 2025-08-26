import random
from time import sleep

from selenium.common import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.base_page import BasePage


class MasterPage(BasePage):
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

    def add_serial1(self):
        """序号添加按钮."""
        self.click(By.XPATH, '(//button[@class="m-b-10 ivu-btn ivu-btn-default"])[1]')

    def del_serial1(self):
        """序号删除按钮."""
        self.click(By.XPATH, '(//button[@class="m-b-10 ivu-btn ivu-btn-default"])[2]')

    def add_serial2(self):
        """序号添加按钮."""
        self.click(By.XPATH, '(//button[@class="m-b-10 ivu-btn ivu-btn-default"])[3]')

    def del_serial2(self):
        """序号删除按钮."""
        self.click(By.XPATH, '(//button[@class="m-b-10 ivu-btn ivu-btn-default"])[4]')

    def add_serial3(self):
        """序号添加按钮."""
        self.click(By.XPATH, '(//button[@class="m-b-10 ivu-btn ivu-btn-default"])[5]')

    def del_serial3(self):
        """序号删除按钮."""
        self.click(By.XPATH, '(//button[@class="m-b-10 ivu-btn ivu-btn-default"])[6]')

    def add_serial4(self):
        """序号添加按钮."""
        self.click(By.XPATH, '(//button[@class="m-b-10 ivu-btn ivu-btn-default"])[7]')

    def del_serial4(self):
        """序号删除按钮."""
        self.click(By.XPATH, '(//button[@class="m-b-10 ivu-btn ivu-btn-default"])[8]')

    def add_ok_button(self):
        """点击添加确定按钮"""
        self.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )

    def get_find_message(self):
        """获取错误信息"""
        message = WebDriverWait(self.driver, 10).until(
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

    def get_find_element_xpath(self, xpath):
        """获取用户头像元素，返回该元素。如果元素未找到，返回None。"""
        try:
            return self.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return None

    def get_find_elements_xpath(self, xpath):
        """获取用户头像元素，返回该元素。如果元素未找到，返回None。"""
        self.finds_elements(By.XPATH, xpath)

    def get_find_element_class(self, classname):
        """获取用户头像元素，返回该元素。如果元素未找到，返回None。"""
        try:
            return self.find_element(By.CLASS_NAME, classname)
        except NoSuchElementException:
            return None

    def go_item_dialog(self, test_item):
        """选择物料代码"""
        # 填写订物料代码
        self.click_button('//span[text()=" 物料代码： "]/parent::div//i')
        self.click_button(
            f'(//div[@class="vxe-table--body-wrapper body--wrapper"])[last()]/table//tr[.//span[text()="{test_item}"]]/td[.//span[text()="{test_item}"]]'
        )
        sleep(1)
        self.click_button('(//button[@class="ivu-btn ivu-btn-primary"])[last()]')

    def delete_material(self, test_item):
        """删除工艺产能"""
        wait = WebDriverWait(self.driver, 3)
        # 循环删除元素直到不存在
        while True:
            eles = self.driver.find_elements(
                By.XPATH,
                f'//tr[.//span[text()="{test_item}"]]/td[2]//span[text()="{test_item}"]',
            )
            if not eles:
                break  # 没有找到元素时退出循环
                # 存在元素，点击删除按钮
            eles[0].click()
            self.click_del_button()
            # 点击确定
            # 找到共同的父元素
            parent = self.get_find_element_class("ivu-modal-confirm-footer")

            # 获取所有button子元素
            all_buttons = parent.find_elements(By.TAG_NAME, "button")

            # 选择需要的button 第二个确定按钮
            second_button = all_buttons[1]
            second_button.click()
            # 等待元素消失
            try:
                wait.until_not(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            f'//tr[.//span[text()="{test_item}"]]/td[2]//span[text()="{test_item}"]',
                        )
                    )
                )
            except TimeoutException:
                print("警告：元素未在预期时间内消失")
                continue  # 继续下一轮尝试
            else:
                # 不再找到元素，退出循环
                break

    def check_master_exists(self, item_name):
        try:
            self.get_find_element_xpath(
                f'//tr[.//span[text()="{item_name}"]]/td[2]//span[text()="{item_name}"]'
            )
            return True
        except:
            return False

    def is_clickable(self, xpath, timeout=5):
        """
        判断指定的元素是否可点击。
        :param xpath: 要检查的 XPath
        :param timeout: 等待超时时间（秒）
        :return: True/False
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            return True
        except TimeoutException:
            return False
