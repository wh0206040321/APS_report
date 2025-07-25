import random
from time import sleep
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.base_page import BasePage


class WarehouseLocationPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)  # 调用基类构造函数

    def click_add_button(self):
        """点击添加按钮."""
        self.click(By.XPATH, '//p[text()="新增"]')

    def click_edi_button(self):
        """点击修改按钮."""
        self.click(By.XPATH, '//p[text()="编辑"]')

    def filter_method(self, click_xpath):
        """过滤公共方法"""
        sleep(2)
        self.click_button(click_xpath)
        sleep(1)
        self.click_button('//div[@class="filterInput"]//following-sibling::label')
        sleep(1)
        item_code = self.driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]',
        )
        sleep(1)
        self.click_button('//div[@class="filterInput"]//preceding-sibling::div[1]')
        item_code2 = self.driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]',
        )
        return len(item_code) == 0 and len(item_code2) > 0

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

    def batch_modify_input(self, xpath_list=[], new_value=""):
        """批量修改输入框"""
        for xpath in xpath_list:
            try:
                self.enter_texts(xpath, new_value)
            except NoSuchElementException:
                print(f"未找到元素: {xpath}")
            except Exception as e:
                print(f"操作 {xpath} 时出错: {str(e)}")

    def get_demo_num1(self):
        num = 0
        sleep(1)
        num = 1
        return num

    def batch_acquisition_input(self, xpath_list=[], text_value=""):
        """批量获取输入框"""
        values = []
        for index, xpath in enumerate(xpath_list, 1):
            try:
                # 显式等待元素可见（最多等待10秒）
                element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(("xpath", xpath))
                )

                # 获取输入框的值
                value = element.get_attribute("value")
                if value == text_value:
                    values.append(value)

            except TimeoutException:
                raise NoSuchElementException(
                    f"元素未找到（XPath列表第{index}个）: {xpath}"
                )
            except Exception as e:
                raise Exception(
                    f"获取输入框值时发生错误（XPath列表第{index}个）: {str(e)}"
                )

        return values

    def go_item(self):
        """前往物料页面"""
        self.click_button('(//span[text()="物控管理"])[1]')  # 点击物控管理
        self.click_button('(//span[text()="物控基础数据"])[1]')  # 点击物控基础数据
        self.click_button('(//span[text()="仓库库位"])[1]')  # 点击仓库库位

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

    def add_none(self, xpath_list=[], color_value=""):
        """新增弹窗(有必填项)不填写信息，不允许提交公共方法."""
        for index, xpath in enumerate(xpath_list, 1):
            try:
                element = self.get_find_element_xpath(xpath)
                # 获取输入框的值
                if color_value != element.value_of_css_property("border-color"):
                    raise NoSuchElementException(
                        f"边框颜色不对（XPath列表第{index}个）: {xpath}"
                    )
                    return False

            except TimeoutException:
                raise NoSuchElementException(
                    f"元素未找到（XPath列表第{index}个）: {xpath}"
                )
            except Exception as e:
                raise Exception(
                    f"获取输入框值时发生错误（XPath列表第{index}个）: {str(e)}"
                )
        return True

    def add_one(self, xpath_list=[], color_value=""):
        """新增弹窗(有必填项)多项必填只填写一项不允许提交方法，不允许提交公共方法."""
        for index, xpath in enumerate(xpath_list, 1):
            try:
                element = self.get_find_element_xpath(xpath)
                # 获取输入框的值
                if color_value != element.value_of_css_property("border-color"):
                    raise NoSuchElementException(
                        f"边框颜色不对（XPath列表第{index}个）: {xpath}"
                    )
                    return False

            except TimeoutException:
                raise NoSuchElementException(
                    f"元素未找到（XPath列表第{index}个）: {xpath}"
                )
            except Exception as e:
                raise Exception(
                    f"获取输入框值时发生错误（XPath列表第{index}个）: {str(e)}"
                )
        return True
