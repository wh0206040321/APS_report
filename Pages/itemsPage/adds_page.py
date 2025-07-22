from time import sleep

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.base_page import BasePage


class AddsPaes(BasePage):
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

    def batch_modify_input(self, xpath_list=[], new_value=""):
        """批量修改输入框"""
        for xpath in xpath_list:
            try:
                self.enter_texts(xpath, new_value)
            except NoSuchElementException:
                print(f"未找到元素: {xpath}")
            except Exception as e:
                print(f"操作 {xpath} 时出错: {str(e)}")

    def batch_modify_dialog_box(self, xpath_list=[], new_value=""):
        """批量修改对话框"""
        for xpath in xpath_list:
            try:
                self.click_button(xpath)
                self.click_button(new_value)
                self.click_button('(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[last()]//span[text()="确定"]')
            except NoSuchElementException:
                print(f"未找到元素: {xpath}")
            except Exception as e:
                print(f"操作 {xpath} 时出错: {str(e)}")

    def batch_modify_code_box(self, xpath_list=[], new_value=""):
        """批量修改代码对话框"""
        for xpath in xpath_list:
            try:
                self.click_button(xpath)
                ActionChains(self.driver).double_click(self.get_find_element_xpath(new_value)).perform()
                self.click_button('(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[last()]//span[text()="确定"]')
            except NoSuchElementException:
                print(f"未找到元素: {xpath}")
            except Exception as e:
                print(f"操作 {xpath} 时出错: {str(e)}")

    def batch_modify_select_input(self, xpath_list=[]):
        """批量修改下拉框"""
        for idx, d in enumerate(xpath_list, start=1):
            self.click_button(d['select'])
            self.click_button(d['value'])


    def batch_modify_time_input(self, xpath_list=[]):
        """批量修改时间"""
        for index, xpath in enumerate(xpath_list, start=1):
            try:
                self.click_button(xpath)
                self.click_button(f'(//span[@class="ivu-date-picker-cells-cell ivu-date-picker-cells-cell-today ivu-date-picker-cells-focused"])[1]')
                self.click_button(f'(//div[@class="ivu-picker-confirm"])[{index}]/button[3]')
            except NoSuchElementException:
                print(f"未找到元素: {xpath}")
            except Exception as e:
                print(f"操作 {xpath} 时出错: {str(e)}")

    def batch_acquisition_input(self, xpath_list=[], text_value=""):
        """批量获取输入框"""
        values = []
        for index, xpath in enumerate(xpath_list, 1):
            try:
                value = self.get_find_element_xpath(xpath).get_attribute("value")
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

    def go_settings_page(self):
        """
        进入设置页面
        """
        self.click_button('(//i[@class="icon-wrapper el-tooltip font21 line-height-15 m-r-12"])[1]')
        self.click_button('//div[text()=" 显示设置 "]')
        ele = self.get_find_element_xpath('(//div[@class="vxe-table--body-wrapper body--wrapper"])[4]')
        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", ele)
        sleep(1)
        num = self.get_find_element_xpath('(//div[@class="vxe-table--fixed-left-wrapper"])[3]//table[@class="vxe-table--body"]//tr[last()]//div').text
        self.click_button('(//div[@class="demo-drawer-footer"])[2]//span[text()="确定"]')
        return num