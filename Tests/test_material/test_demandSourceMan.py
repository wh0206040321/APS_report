import random
from time import sleep

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.materialPage.warehouseLocation_page import WarehouseLocationPage
from Pages.itemsPage.login_page import LoginPage
from Utils.data_driven import DateDriver
from Utils.driver_manager import create_driver, safe_quit, all_driver_instances


@pytest.fixture(scope="module")
def login_to_item():
    """初始化并返回 driver"""
    driver_path = DateDriver().driver_path
    driver = create_driver(driver_path)
    driver.implicitly_wait(3)

    # 初始化登录页面
    page = LoginPage(driver)  # 初始化登录页面
    page.navigate_to(DateDriver().url)  # 导航到登录页面
    page.login(DateDriver().username, DateDriver().password, DateDriver().planning)
    page.click_button('(//span[text()="计划运行"])[1]')  # 点击计划管理
    page.click_button('(//span[text()="方案管理"])[1]')  # 点击计划基础数据
    page.click_button('(//span[text()="物控需求定义"])[1]')  # 点击物料交付答复
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("物控需求定义测试用例")
@pytest.mark.run(order=110)
class TestItemPage:
    @pytest.fixture(autouse=True)
    def setup(self, login_to_item):
        self.driver = login_to_item
        self.item = WarehouseLocationPage(self.driver)

    @allure.story("添加信息 不填写数据点击确认 不允许提交")
    # @pytest.mark.run(order=1)
    def test_warehouselocation_addfail(self, login_to_item):
        # 点击新增按钮
        self.item.click_add_button()
        # 点击确定
        self.item.click_button('(//button[@type="button"]/span[text()="确定"])[2]')
        sleep(1)
        message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="ivu-message"]//span')
            )
        )
        # 检查元素是否包含子节点
        assert message.text == "请填写表单必填项!"
        assert not self.item.has_fail_message()

    @allure.story("添加信息，有多个必填只填写一项，不允许提交")
    # @pytest.mark.run(order=2)
    def test_item_addcodefail(self, login_to_item):
        # 点击新增按钮
        self.item.click_add_button()
        # 输入第一个必填项
        xpath_list = [
            "//div[text()=' 需求来源编码: ']/following-sibling::div/input",
            "//div[text()=' 需求来源名称: ']/following-sibling::div/input",
        ]
        self.item.batch_modify_input(xpath_list, '2')
        # 点击确定
        self.item.click_button('(//button[@type="button"]/span[text()="确定"])[2]')
        sleep(1)
        # 声明必填项的xpath和判断的边框颜色
        message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="ivu-message"]//span')
            )
        )
        # 检查元素是否包含子节点
        assert message.text == "请填写表单必填项!"
        assert not self.item.has_fail_message()

    @allure.story("添加必填数据成功")
    # @pytest.mark.run(order=1)
    def test_item_addsuccess(self, login_to_item):

        self.item.click_add_button()  # 检查点击添加
        # 创建一个 ActionChains 对象
        actions = ActionChains(self.driver)
        # 输入框要修改的值
        text_str = "111"
        # 新增输入框的xpath
        input_xpath_list = [
            "//div[text()=' 需求来源编码: ']/following-sibling::div/input",
            "//div[text()=' 需求来源名称: ']/following-sibling::div/input",
        ]
        sleep(1)
        # 批量修改输入框
        self.item.batch_modify_input(input_xpath_list, text_str)
        self.item.click_button("//div[text()=' 需求类型: ']/following-sibling::div/label")
        # 点击数据库名称下拉
        self.item.click_button("//div[text()=' 数据库名称: ']/following-sibling::div")
        sleep(1)
        self.item.click_button("//div[text()=' 数据库名称: ']/following-sibling::div//ul[@class='ivu-select-dropdown-list']/li[1]")

        sleep(1)
        # 点击表或视图名下拉
        self.item.click_button("//div[text()=' 表或视图名: ']/following-sibling::div")
        sleep(1)
        self.item.click_button(
            "//div[text()=' 表或视图名: ']/following-sibling::div//ul[@class='ivu-select-dropdown-list']/li[2]")

        # 点击表格【需求来源标识】字段名称下拉
        self.item.click_button("//span[text()='需求来源标识']/ancestor::td/following-sibling::td[2]")
        sleep(1)
        self.item.click_button("//span[text()='需求来源标识']/ancestor::td/following-sibling::td[2]//div[@class='ivu-select-selection']")
        sleep(1)
        self.item.click_button("//span[text()='需求来源标识']/ancestor::td/following-sibling::td[2]//ul[@class='ivu-select-dropdown-list']/li[1]")

        # 点击表格【订单代码】字段名称下拉
        sleep(1)
        element_to_double_click = self.driver.find_element(
            By.XPATH,
            "//span[text()='订单代码']/ancestor::td/following-sibling::td[2]",
        )
        actions.double_click(element_to_double_click).perform()
        self.item.click_button("//span[text()='订单代码']/ancestor::td/following-sibling::td[2]")
        sleep(1)
        self.item.click_button(
            "//span[text()='订单代码']/ancestor::td/following-sibling::td[2]//div[@class='ivu-select-selection']")
        sleep(1)
        self.item.click_button(
            "//span[text()='订单代码']/ancestor::td/following-sibling::td[2]//ul[@class='ivu-select-dropdown-list']/li[2]")

        # 点击表格【物料编码】字段名称下拉
        sleep(1)
        element_to_double_click = self.driver.find_element(
            By.XPATH,
            "//span[text()='物料编码']/ancestor::td/following-sibling::td[2]",
        )
        actions.double_click(element_to_double_click).perform()
        sleep(1)
        self.item.click_button("//span[text()='物料编码']/ancestor::td/following-sibling::td[2]")
        sleep(1)
        self.item.click_button(
            "//span[text()='物料编码']/ancestor::td/following-sibling::td[2]//div[@class='ivu-select-selection']")
        sleep(1)
        self.item.click_button(
            "//span[text()='物料编码']/ancestor::td/following-sibling::td[2]//ul[@class='ivu-select-dropdown-list']/li[3]")

        # 点击表格【计划开始时间】字段名称下拉
        sleep(1)
        element_to_double_click = self.driver.find_element(
            By.XPATH,
            "//span[text()='计划开始时间']/ancestor::td/following-sibling::td[2]",
        )
        actions.double_click(element_to_double_click).perform()
        sleep(1)
        self.item.click_button(
            "//span[text()='计划开始时间']/ancestor::td/following-sibling::td[2]")
        sleep(1)
        self.item.click_button(
            "//span[text()='计划开始时间']/ancestor::td/following-sibling::td[2]//div[@class='ivu-select-selection']")
        sleep(1)
        self.item.click_button(
            "//span[text()='计划开始时间']/ancestor::td/following-sibling::td[2]//ul[@class='ivu-select-dropdown-list']/li[4]")

        # 点击表格【计划数量】字段名称下拉
        sleep(1)
        element_to_double_click = self.driver.find_element(
            By.XPATH,
            "//span[text()='计划数量']/ancestor::td/following-sibling::td[2]",
        )
        actions.double_click(element_to_double_click).perform()
        sleep(1)
        self.item.click_button(
            "//span[text()='计划数量']/ancestor::td/following-sibling::td[2]")
        sleep(1)
        self.item.click_button(
            "//span[text()='计划数量']/ancestor::td/following-sibling::td[2]//div[@class='ivu-select-selection']")
        sleep(1)
        self.item.click_button(
            "//span[text()='计划数量']/ancestor::td/following-sibling::td[2]//ul[@class='ivu-select-dropdown-list']/li[5]")

        # 点击表格【BOM版本】字段名称下拉
        sleep(1)
        element_to_double_click = self.driver.find_element(
            By.XPATH,
            "//span[text()='BOM版本']/ancestor::td/following-sibling::td[2]",
        )
        actions.double_click(element_to_double_click).perform()
        sleep(1)
        self.item.click_button("//span[text()='BOM版本']/ancestor::td/following-sibling::td[2]")
        sleep(1)
        self.item.click_button(
            "//span[text()='BOM版本']/ancestor::td/following-sibling::td[2]//div[@class='ivu-select-selection']")
        sleep(1)
        self.item.click_button(
            "//span[text()='BOM版本']/ancestor::td/following-sibling::td[2]//ul[@class='ivu-select-dropdown-list']/li[6]")

        # 点击确定
        self.item.click_button('(//button[@type="button"]/span[text()="确定"])[2]')
        # 编辑输入框的xpath（判断是否新增成功用的）
        input_xpath_list2 = [
            "//p[text()=' 需求来源编码: ']/following-sibling::div/input",
            "//p[text()=' 需求来源名称: ']/following-sibling::div/input",
            "//p[text()=' 数据库名称: ']/following-sibling::div/input",
            "//p[text()=' 表或视图名: ']/following-sibling::div/input",
        ]
        text_xpath_list = [
            "//span[text()='Code']",
            "//span[text()='Comments']",
            "//span[text()='ID']",
            "//span[text()='PlanUnitCode']",
            "//span[text()='StatusFlagExt']",
            "//span[text()='TenantId']"
        ]
        value_list = [
            "111",
            "111",
            "$CurrentDB",
            "a_a"
        ]
        value_list2 = [
            "Code"
            "Comments"
            "ID"
            "PlanUnitCode"
            "StatusFlagExt"
            "TenantId"
        ]


        sleep(1)
        # 点击确定
        self.item.click_button('(//button[@type="button"]/span[text()="查看映射"])[1]')
        sleep(1)
        # 批量获取输入框的value
        input_values = self.item.batch_acquisition_input(input_xpath_list2, value_list)
        text_values = self.item.batch_acquisition_input(text_xpath_list, value_list2)
        print('input_values', input_values)
        assert (
                len(input_xpath_list) == len(value_list) and
                len(text_values) == len(value_list2)
        )
        assert not self.item.has_fail_message()

    @allure.story("取消删除数据")
    # @pytest.mark.run(order=1)
    def test_item_delcancel(self, login_to_item):

        # 定位内容为‘111’的行
        self.item.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
        self.item.click_del_button()  # 点击删除
        sleep(1)
        # 点击取消
        self.item.click_button('//button[@class="ivu-btn ivu-btn-text"]')
        sleep(1)
        # 定位内容为‘111’的行
        itemdata = self.item.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="111"]]]/td[2]'
        ).text
        assert itemdata == "111", f"预期{itemdata}"
        assert not self.item.has_fail_message()

    @allure.story("添加测试数据")
    # @pytest.mark.run(order=1)
    def test_item_addsuccess1(self, login_to_item):

        self.item.click_add_button()  # 检查点击添加
        # 输入框要修改的值
        text_str = "222"
        date_str = "2025/07/23 00:00:00"
        # 新增输入框的xpath
        input_xpath_list = [
            "//div[@id='rta286cd-4col']//input",
            "//div[@id='66fs3ka3-ul4k']//input",
            "//div[@id='xvo43ah2-gj6p']//input",
            "//div[@id='qh1vnphz-0cqy']//input",
            "//div[@id='ddn5nlv3-myjg']//input"
        ]
        # 编辑输入框的xpath（判断是否新增成功用的）
        input_xpath_list2 = [
            "//div[@id='bj6kxqe3-e8d6']//input",
            "//div[@id='2xq4wbqm-i07g']//input",
            "//div[@id='xr3hl02y-kvwd']//input",
            "//div[@id='q2eosdwd-mk2k']//input",
            "//div[@id='9o985n3x-9hdz']//input"
        ]

        # 新增日期选择框的xpath
        date_xpath_list = ["//div[@id='9tbuqose-wzrv']//input"]
        # 编辑新增日期选择框的xpath
        date_xpath_list2 = ["//div[@id='gq66qiep-c94c']//input"]

        sleep(1)
        # 批量修改输入框
        self.item.batch_modify_input(input_xpath_list, text_str)
        self.item.batch_modify_input(date_xpath_list, date_str)

        sleep(1)
        # 点击确定
        self.item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 选中新增行
        self.item.click_button('//tr[./td[2][.//span[text()="222"]]]/td[2]')
        # 点击编辑按钮
        self.item.click_edi_button()
        sleep(1)
        # 批量获取输入框的value
        input_values = self.item.batch_acquisition_input(input_xpath_list2, text_str)
        # 批量获取日期选择框的value
        input_values2 = self.item.batch_acquisition_input(date_xpath_list2, date_str)

        sleep(1)
        assert (
                len(input_xpath_list) == len(input_values) and
                len(date_xpath_list) == len(input_values2)
        )
        assert not self.item.has_fail_message()

    @allure.story("修改测试数据成功")
    # @pytest.mark.run(order=1)
    def test_item_editcodesuccess(self, login_to_item):

        # 输入框要修改的值
        text_str = "333"
        date_str = "2025/07/23 00:00:00"
        # 输入框的xpath
        input_xpath_list = [
            "//div[@id='bj6kxqe3-e8d6']//input",
            "//div[@id='2xq4wbqm-i07g']//input",
            "//div[@id='xr3hl02y-kvwd']//input",
            "//div[@id='q2eosdwd-mk2k']//input",
            "//div[@id='9o985n3x-9hdz']//input"
        ]
        input_xpath_list2 = [
            "//div[@id='gq66qiep-c94c']//input"
        ]

        # 选中刚刚新增的测试数据
        self.item.click_button('//tr[./td[2][.//span[text()="222"]]]/td[2]')
        # 点击修改按钮
        self.item.click_edi_button()
        sleep(1)

        # 批量修改输入框
        self.item.batch_modify_input(input_xpath_list, text_str)
        self.item.batch_modify_input(input_xpath_list2, date_str)

        sleep(1)
        # 点击确定
        self.item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 选中刚刚编辑的数据
        self.item.click_button('//tr[./td[2][.//span[text()="333"]]]/td[2]')
        # 点击编辑按钮
        self.item.click_edi_button()
        sleep(1)
        # 批量获取输入框的value
        input_values = self.item.batch_acquisition_input(input_xpath_list, text_str)
        input_values2 = self.item.batch_acquisition_input(input_xpath_list2, date_str)
        sleep(1)
        assert (
                len(input_xpath_list) == len(input_values) and
                len(input_xpath_list2) == len(input_values2)
        )
        assert not self.item.has_fail_message()

    @allure.story("修改数据重复")
    # @pytest.mark.run(order=1)
    def test_item_editrepeat(self, login_to_item):

        # 选中1测试A工厂代码
        self.item.click_button('//tr[./td[2][.//span[text()="333"]]]/td[2]')
        # 点击修改按钮
        self.item.click_edi_button()

        # 物料代码等输入111
        input_xpath_list = [
            "//div[@id='bj6kxqe3-e8d6']//input",
            "//div[@id='2xq4wbqm-i07g']//input",
            "//div[@id='xr3hl02y-kvwd']//input",
            "//div[@id='q2eosdwd-mk2k']//input",
            "//div[@id='9o985n3x-9hdz']//input"
        ]
        text_str = "111"
        self.item.batch_modify_input(input_xpath_list, text_str)
        # 点击确定
        self.item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 获取重复弹窗文字
        error_popup = self.item.get_find_element_xpath(
            '//div[text()=" 记录已存在,请检查！ "]'
        ).text
        assert error_popup == "记录已存在,请检查！", f"预期数据{error_popup}"
        assert not self.item.has_fail_message()

    @allure.story("删除数据成功")
    # @pytest.mark.run(order=1)
    def test_item_delsuccess1(self, login_to_item):
        # 定位内容为‘111’的行
        self.item.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
        self.item.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        parent = self.item.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        self.item.click_ref_button()
        sleep(1)
        # 定位内容为‘111’的行
        itemdata = self.driver.find_elements(
            By.XPATH, '//tr[./td[2][.//span[text()="111"]]]/td[2]'
        )
        assert len(itemdata) == 0
        assert not self.item.has_fail_message()

    @allure.story("编辑全部选项成功")
    # @pytest.mark.run(order=1)
    def test_item_editnamesuccess(self, login_to_item):

        # 输入框要修改的值
        text_str = "111"
        date_str = "2025/07/23 00:00:00"
        # 输入框的xpath
        input_xpath_list = [
            "//div[@id='bj6kxqe3-e8d6']//input",
            "//div[@id='2xq4wbqm-i07g']//input",
            "//div[@id='xr3hl02y-kvwd']//input",
            "//div[@id='q2eosdwd-mk2k']//input",
            "//div[@id='9o985n3x-9hdz']//input",
            "//div[@id='8lu6yii9-5qrd']//input",
            "//div[@id='7qvr4cye-w9by']//input",
            "//div[@id='45quehzf-xoqb']//input",
            "//div[@id='ybwol3cn-51x9']//input",
            "//div[@id='qqauyzxt-70m3']//input",
            "//div[@id='fu1twc2l-p4h3']//input",
            "//div[@id='p25v0w1d-muy8']//input",
            "//div[@id='wpt6qhgf-xoe3']//input",
            "//div[@id='fl2ddlpx-61g5']//input",
            "//div[@id='sz2npi5v-tby5']//input",
            "//div[@id='gkeusaiz-bhx4']//input"

        ]
        input_xpath_list2 = [
            "//div[@id='gq66qiep-c94c']//input",
            "//div[@id='cbr0bpfr-e188']//input",
            "//div[@id='kb30r1yv-g6tm']//input",
            "//div[@id='3txdu8sc-d6q5']//input",
            "//div[@id='toaqsqvo-ikyu']//input",
            "//div[@id='n7botdee-jfwx']//input"
        ]

        # 选中编辑数据
        self.item.click_button('//tr[./td[2][.//span[text()="333"]]]/td[2]')
        # 点击修改按钮
        self.item.click_edi_button()
        sleep(1)

        # 批量修改输入框
        self.item.batch_modify_input(input_xpath_list, text_str)
        self.item.batch_modify_input(input_xpath_list2, date_str)

        sleep(1)
        # 点击确定
        self.item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 选中刚刚编辑的数据行
        self.item.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
        # 点击编辑按钮
        self.item.click_edi_button()
        sleep(1)
        # 批量获取输入框的value
        input_values = self.item.batch_acquisition_input(input_xpath_list, text_str)
        input_values2 = self.item.batch_acquisition_input(input_xpath_list2, date_str)
        sleep(1)
        assert (
            len(input_xpath_list) == len(input_values) and
            len(input_xpath_list2) == len(input_values2)
        )
        assert not self.item.has_fail_message()

    @allure.story("删除测试数据成功")
    # @pytest.mark.run(order=1)
    def test_item_delsuccess2(self, login_to_item):

        # 定位内容为‘111’的行
        self.item.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
        self.item.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        parent = self.item.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        self.item.click_ref_button()
        sleep(1)
        # 定位内容为‘111’的行
        itemdata = self.driver.find_elements(
            By.XPATH, '//tr[./td[2][.//span[text()="111"]]]/td[2]'
        )
        assert len(itemdata) == 0
        assert not self.item.has_fail_message()

    @allure.story("过滤刷新成功")
    # @pytest.mark.run(order=1)
    def test_item_refreshsuccess(self, login_to_item):

        filter_results = self.item.filter_method('//span[text()=" 交付单号"]/ancestor::div[3]//span//span//span')
        print('filter_results', filter_results)
        assert filter_results
        assert not self.item.has_fail_message()

    @allure.story("新增全部数据测试")
    # @pytest.mark.run(order=1)
    def test_item_add_success(self, login_to_item):
        # 输入框的xpath
        input_xpath_list = [
            "//div[@id='rta286cd-4col']//input",
            "//div[@id='xvo43ah2-gj6p']//input",
            "//div[@id='66fs3ka3-ul4k']//input",
            "//div[@id='qh1vnphz-0cqy']//input",
            "//div[@id='o8y69510-yd03']//input",
            "//div[@id='ddn5nlv3-myjg']//input",
            "//div[@id='chqcnvv6-owm6']//input",
            "//div[@id='88u7apyw-pu3s']//input",
            "//div[@id='sdfncnku-1awa']//input",
            "//div[@id='6oq7pcn8-mm4i']//input",
            "//div[@id='gz1o8ytv-ynrc']//input",
            "//div[@id='1z9v7ath-0yn5']//input",
            "//div[@id='ab90zrkw-l8zm']//input",
            "//div[@id='va8oy1t3-ksxz']//input",
            "//div[@id='3yeovk6j-gay9']//input",
            "//div[@id='sgqyksh5-5bi4']//input"
        ]
        # 编辑的输入框xpath（用来判断新增是否成功）
        input_xpath_list2 = [
            "//div[@id='bj6kxqe3-e8d6']//input",
            "//div[@id='2xq4wbqm-i07g']//input",
            "//div[@id='xr3hl02y-kvwd']//input",
            "//div[@id='q2eosdwd-mk2k']//input",
            "//div[@id='9o985n3x-9hdz']//input",
            "//div[@id='8lu6yii9-5qrd']//input",
            "//div[@id='7qvr4cye-w9by']//input",
            "//div[@id='45quehzf-xoqb']//input",
            "//div[@id='ybwol3cn-51x9']//input",
            "//div[@id='qqauyzxt-70m3']//input",
            "//div[@id='fu1twc2l-p4h3']//input",
            "//div[@id='p25v0w1d-muy8']//input",
            "//div[@id='wpt6qhgf-xoe3']//input",
            "//div[@id='fl2ddlpx-61g5']//input",
            "//div[@id='sz2npi5v-tby5']//input",
            "//div[@id='gkeusaiz-bhx4']//input"
        ]
        # 日期的xpath
        date_xpath_list = [
            "//div[@id='9tbuqose-wzrv']//input",
            "//div[@id='oo3qbl0o-1a5k']//input",
            "//div[@id='m1i2tpyu-d9u4']//input",
            "//div[@id='jr551mgt-7hpc']//input",
            "//div[@id='9fyoemci-4fgo']//input",
            "//div[@id='lf1nryjc-yr2m']//input"
        ]
        # 编辑的日期选择框xpath（用来判断新增是否成功）
        date_xpath_list2 = [
            "//div[@id='gq66qiep-c94c']//input",
            "//div[@id='cbr0bpfr-e188']//input",
            "//div[@id='kb30r1yv-g6tm']//input",
            "//div[@id='3txdu8sc-d6q5']//input",
            "//div[@id='toaqsqvo-ikyu']//input",
            "//div[@id='n7botdee-jfwx']//input"
        ]
        # 输入框要修改的值
        text_str = "111"
        # 日期要修改的值
        date_str = "2025/07/17 00:00:00"
        self.item.click_add_button()  # 点击添加
        sleep(1)

        # 批量修改输入框
        self.item.batch_modify_input(input_xpath_list, text_str)
        # 批量修改日期
        self.item.batch_modify_input(date_xpath_list, date_str)

        sleep(1)
        # 点击确定
        self.item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 选中物料代码
        self.item.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
        # 点击编辑按钮
        self.item.click_edi_button()
        sleep(1)
        # 批量获取输入框的value
        input_values = self.item.batch_acquisition_input(input_xpath_list2, text_str)
        # 批量获取日期的value
        date_values = self.item.batch_acquisition_input(date_xpath_list2, date_str)
        sleep(1)
        assert (
                len(input_xpath_list) == len(input_values)
                and len(date_xpath_list) == len(date_values)
        )
        assert not self.item.has_fail_message()

    @allure.story("查询测试数据成功")
    # @pytest.mark.run(order=1)
    def test_item_selectcodesuccess(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
        item = WarehouseLocationPage(driver)  # 用 driver 初始化 ItemPage

        # 点击查询
        item.click_sel_button()
        sleep(1)
        # 定位名称输入框
        element_to_double_click = driver.find_element(
            By.XPATH,
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[4]',
        )
        # 创建一个 ActionChains 对象
        actions = ActionChains(driver)
        # 双击命令
        actions.double_click(element_to_double_click).perform()
        sleep(1)
        # 点击工厂代码
        item.click_button('//div[text()="交付单号" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        item.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        item.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "111",
        )
        sleep(1)

        # 点击确认
        item.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[2]'
        )
        sleep(1)
        # 定位第一行是否为产品A
        itemcode = item.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]'
        ).text
        # 定位第二行没有数据
        itemcode2 = driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][2]/td[2]',
        )
        assert itemcode == "111" and len(itemcode2) == 0
        assert not item.has_fail_message()

    @allure.story("没有数据时显示正常")
    # @pytest.mark.run(order=1)
    def test_item_selectnodatasuccess(self, login_to_item):

        # 点击查询
        self.item.click_sel_button()
        sleep(1)
        # 定位名称输入框
        element_to_double_click = self.driver.find_element(
            By.XPATH,
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[4]',
        )
        # 创建一个 ActionChains 对象
        actions = ActionChains(self.driver)
        # 双击命令
        actions.double_click(element_to_double_click).perform()
        sleep(1)
        # 点击交付单号
        self.item.click_button('//div[text()="交付单号" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        self.item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        self.item.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        self.item.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "没有数据",
        )
        sleep(1)

        # 点击确认
        self.item.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[2]'
        )
        sleep(1)
        itemcode = self.driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]',
        )
        assert len(itemcode) == 0
        assert not self.item.has_fail_message()

    @allure.story("删除数据成功")
    # @pytest.mark.run(order=1)
    def test_item_delsuccess3(self, login_to_item):
        # 定位内容为‘111’的行
        self.item.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
        self.item.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        parent = self.item.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        self.item.click_ref_button()
        sleep(1)
        # 定位内容为‘111’的行
        itemdata = self.driver.find_elements(
            By.XPATH, '//tr[./td[2][.//span[text()="111"]]]/td[2]'
        )
        assert len(itemdata) == 0
        assert not self.item.has_fail_message()
