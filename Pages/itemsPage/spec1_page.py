from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from Pages.base_page import BasePage


class Spec1Page(BasePage):
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

    def add_layout(self, layout):
        """添加布局."""
        self.click_button('//div[@class="newDropdown"]//i')
        self.click_button('//li[text()="添加新布局"]')
        self.enter_texts(
            '//div[text()="当前布局:"]/following-sibling::div//input', f"{layout}"
        )
        checkbox1 = self.get_find_element_xpath(
            '//div[text()="是否默认启动:"]/following-sibling::label/span'
        )

        # 检查复选框是否未被选中
        if checkbox1.get_attribute("class") == "ivu-checkbox":
            # 如果未选中，则点击复选框进行选中
            self.click_button(
                '//div[text()="是否默认启动:"]/following-sibling::label/span'
            )
        sleep(1)

        self.click_button('(//div[text()=" 显示设置 "])[1]')
        # 获取是否可见选项的复选框元素
        checkbox2 = self.get_find_element_xpath(
            '(//div[./div[text()="是否可见:"]])[1]/label/span'
        )
        # 检查复选框是否未被选中
        if checkbox2.get_attribute("class") == "ivu-checkbox":
            # 如果未选中，则点击复选框进行选中
            self.click_button('(//div[./div[text()="是否可见:"]])[1]/label/span')
            # 点击确定按钮保存设置
            self.click_button('(//div[@class="demo-drawer-footer"])[3]/button[2]')
        else:
            # 如果已选中，直接点击确定按钮保存设置
            self.click_button('(//div[@class="demo-drawer-footer"])[3]/button[2]')

    def add_input_all(self, name, num):
        """输入框全部输入保存"""
        if name != "":
            # 输入代码
            self.enter_texts('(//label[text()="代码"])[1]/parent::div//input', f"{name}")
            self.enter_texts('(//label[text()="名称"])[1]/parent::div//input', f"{name}")
            # 显示颜色下拉框
            self.click_button('(//label[text()="显示颜色"])[1]/parent::div//i')
            # 显示颜色
            self.click_button('//span[text()="RGB(100,255,178)"]')
            ele = self.get_find_element_xpath(
                '(//label[text()="显示顺序"])[1]/parent::div//input'
            )
            ele.send_keys(Keys.CONTROL, "a")
            ele.send_keys(Keys.DELETE)
            # 显示顺序框输入文字字母符号数字
            self.enter_texts(
                '(//label[text()="显示顺序"])[1]/parent::div//input', f"{num}"
            )
            self.enter_texts('(//label[text()="备注"])[1]/parent::div//input', f"{name}")
            prefixes = ["单批上限", "合批上限", "合批期间"]  # 三种前缀

            for prefix in prefixes:  # 遍历三种类型
                for i in range(1, 8):  # 遍历 1~7
                    xpath = f'(//label[text()="{prefix}{i}"])[1]/parent::div//input'
                    self.enter_texts(xpath, str(num))
            self.click_button('(//button[@type="button"]/span[text()="确定"])[4]')

