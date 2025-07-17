import random
from time import sleep

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By


from Pages.base_page import BasePage


class ChangeI(BasePage):
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

    def add_input_all(self, num):
        """输入框全部输入保存"""
        if num != "":
            code1 = "1测试资源A"
            code2 = "2339-50"
            # 点击资源
            self.click_button(
                '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[1]'
            )
            # 勾选框
            rows = self.driver.find_elements(By.XPATH, f"//table[.//tr[td[3]//span[text()='{code1}']]]//tr")
            for index, row in enumerate(rows, start=1):
                td3_text = row.find_elements(By.TAG_NAME, "td")[2].text.strip()
                if f"{code1}" == td3_text:
                    print(f"✅ 找到匹配行，行号为：{index}")

                    # 3. 使用这个行号 idx 构造另一个 XPath
                    target_xpath = f'(//table[.//tr[{index}]/td[2][contains(@class,"col--checkbox")]])[2]//tr[{index}]/td[2]/div/span'
                    target_element = self.get_find_element_xpath(target_xpath)

                    # 4. 操作目标元素
                    target_element.click()
                    break  # 如果只处理第一个匹配行，可以 break
            self.click_button(
                '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
            )

            # 点击前目录
            self.click_button(
                '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[2]'
            )
            # 勾选框
            self.click_button(
                f'(//table[.//tr[3]/td[2][contains(@class,"col--checkbox")]])[2]//tr[4]/td[.//span[@class="vxe-cell--checkbox"]]//div/span')
            self.click_button(
                '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
            )

            # 点击后目录
            self.click_button(
                '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[3]'
            )
            # 勾选框
            self.click_button(
                f'(//table[.//tr[3]/td[2][contains(@class,"col--checkbox")]])[2]//tr[3]/td[.//span[@class="vxe-cell--checkbox"]]//div/span')
            self.click_button(
                '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
            )

            name = ["切换时间(分钟)", "优先度", "备注"]
            for index, value in enumerate(name, start=1):
                ele = self.get_find_element_xpath(f'//label[text()="{value}"][1]/parent::div//input')
                ele.send_keys(Keys.CONTROL, "a")
                ele.send_keys(Keys.DELETE)
                ele.send_keys(num)

            self.click_button('//label[text()="切换时间调整表达式"]/following-sibling::div//i')
            xpth = self.get_find_element_xpath('//span[text()="绝对值函数"]')
            ActionChains(self.driver).double_click(xpth).perform()
            sleep(1)
            self.click_button('(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[last()]//span[text()="确定"]')

            # 获取勾选的资源
            resource = self.get_find_element_xpath(
                '(//label[text()="资源"])[1]/parent::div//input'
            ).get_attribute("value")
            # 获取前目录
            item1 = self.get_find_element_xpath(
                '(//label[text()="前品目"])[1]/parent::div//input'
            ).get_attribute("value")
            sleep(1)
            # 获取后目录
            item2 = self.get_find_element_xpath(
                '(//label[text()="后品目"])[1]/parent::div//input'
            ).get_attribute("value")
            sleep(1)
            time = self.get_find_element_xpath(
                '(//label[text()="切换时间调整表达式"])[1]/parent::div//input'
            ).get_attribute("value")

            self.click_button(
                '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
            )
            return resource, item1, item2, time
