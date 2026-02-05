import random
import re
from time import sleep

import allure
import pytest
from selenium import webdriver
from selenium.webdriver import Keys
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
    page.click_button('(//span[text()="物控管理"])[1]')  # 点击计划管理
    page.click_button('(//span[text()="物控业务数据"])[1]')  # 点击计划基础数据
    page.click_button('(//span[text()="物料库存"])[1]')  # 点击物品
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("物料库存测试用例")
@pytest.mark.run(order=117)
class TestItemPage:
    @pytest.fixture(autouse=True)
    def setup(self, login_to_item):
        self.driver = login_to_item
        self.item = WarehouseLocationPage(self.driver)

    @allure.story("添加库存信息 不填写数据点击确认 不允许提交")
    # @pytest.mark.run(order=1)
    def test_materialInventory_addfail(self, login_to_item):
        sleep(3)
        # divs = self.driver.find_elements(By.CLASS_NAME, "tabsDivItem")
        # find_layout = self.driver.find_elements(By.XPATH, '//div[text()=" 测试布局A "]')
        # if len(find_layout) == 0 and len(divs) > 1:
        #     layout = "测试布局A"
        #     self.item.add_layout(layout)
        self.item.click_add_button()
        # 在途库存单据号xpath
        input_box = self.item.get_find_element_xpath(
            "//div[@id='p34nag46-7evf']//input"
        )
        # 在途数量xpath
        inputname_box = self.item.get_find_element_xpath(
            "//div[@id='ywz9q11i-sp3b']//input"
        )

        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="确定"]')
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        border_color = input_box.value_of_css_property("border-color")
        bordername_color = inputname_box.value_of_css_property("border-color")
        expected_color = "rgb(255, 0, 0)"  # 红色的 rgb 值
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="取消"]')
        assert (
            border_color == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{border_color}"
        assert (
            bordername_color == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{bordername_color}"
        # assert layout == name
        assert not self.item.has_fail_message()

    @allure.story("添加物料库存信息，只填写物料代码，不填写仓库代码等，不允许提交")
    # @pytest.mark.run(order=2)
    def test_materialInventory_addcodefail(self, login_to_item):

        self.item.click_add_button()
        self.item.enter_texts(
            "//div[@id='p34nag46-7evf']//input", "text1231"
        )
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="确定"]')
        input_box = self.item.get_find_element_xpath(
            "//div[@id='ywz9q11i-sp3b']//input"
        )
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        border_color = input_box.value_of_css_property("border-color")
        expected_color = "rgb(255, 0, 0)"  # 红色的 rgb 值
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="取消"]')
        assert (
            border_color == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{border_color}"
        assert not self.item.has_fail_message()

    @allure.story("添加数据成功")
    # @pytest.mark.run(order=1)
    def test_materialInventory_addsuccess(self, login_to_item):

        self.item.click_add_button()  # 检查点击添加
        # 物料代码
        self.item.enter_texts("//div[@id='p34nag46-7evf']//input", "111")
        # 仓库编码
        self.item.enter_texts("//div[@id='ywz9q11i-sp3b']//input", "111")
        # 库存编码
        self.item.enter_texts("//div[@id='x1k7t87i-tvc3']//input", "111")
        # 批次号
        self.item.enter_texts("//div[@id='u2tgl5h9-otp1']//input", "111")
        # 库存日期
        self.item.enter_texts("//div[@id='ol0ayk71-opoa']//input", "2025/07/22 00:00:00")

        # 点击确定
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="确定"]')
        sleep(1)
        adddata = self.item.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="111"]]]/td[2]'
        ).text
        assert adddata == "111", f"预期数据是111，实际得到{adddata}"
        assert not self.item.has_fail_message()

    @allure.story("添加数据重复")
    # @pytest.mark.run(order=1)
    def test_materialInventory_addrepeat(self, login_to_item):

        self.item.click_add_button()  # 检查点击添加
        # 物料代码
        self.item.enter_texts("//div[@id='p34nag46-7evf']//input", "111")
        # 仓库编码
        self.item.enter_texts("//div[@id='ywz9q11i-sp3b']//input", "111")
        # 库存编码
        self.item.enter_texts("//div[@id='x1k7t87i-tvc3']//input", "111")
        # 批次号
        self.item.enter_texts("//div[@id='u2tgl5h9-otp1']//input", "111")
        # 库存日期
        self.item.enter_texts("//div[@id='ol0ayk71-opoa']//input", "2025/07/22 00:00:00")
        # 点击确定
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="确定"]')
        sleep(1)
        # 获取重复弹窗文字
        error_popup = self.item.finds_elements(By.XPATH,'//div[text()=" 记录已存在,请检查！ "]')
        self.item.click_button('//button[@type="button"]/span[text()="关闭"]')
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="取消"]')
        assert (
            len(error_popup) == 1
        ), f"预期数据是记录已存在,请检查，实际得到{error_popup}"
        assert not self.item.has_fail_message()

    @allure.story("取消删除数据")
    # @pytest.mark.run(order=1)
    def test_materialInventory_delcancel(self, login_to_item):
        # 定位内容为‘111’的行
        self.item.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
        self.item.click_del_button()  # 点击删除
        sleep(1)
        # 点击取消
        self.item.click_button('//div[@class="ivu-modal-confirm-footer"]//span[text()="取消"]')
        sleep(1)
        # 定位内容为‘111’的行
        itemdata = self.item.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="111"]]]/td[2]'
        ).text
        assert itemdata == "111", f"预期{itemdata}"
        assert not self.item.has_fail_message()

    @allure.story("添加测试数据")
    # @pytest.mark.run(order=1)
    def test_materialInventory_addsuccess1(self, login_to_item):

        self.item.click_add_button()  # 检查点击添加
        # 物料代码
        self.item.enter_texts("//div[@id='p34nag46-7evf']//input", "1测试A")
        # 仓库编码
        self.item.enter_texts("//div[@id='ywz9q11i-sp3b']//input", "1测试A")
        # 库存编码
        self.item.enter_texts("//div[@id='x1k7t87i-tvc3']//input", "1测试A")
        # 批次号
        self.item.enter_texts("//div[@id='u2tgl5h9-otp1']//input", "1测试A")
        # 库存日期
        self.item.enter_texts("//div[@id='ol0ayk71-opoa']//input", "2025/07/22 00:00:00")
        # 点击确定
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="确定"]')
        sleep(1)
        adddata = self.item.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="1测试A"]]]/td[2]'
        ).text
        assert adddata == "1测试A", f"预期数据是1测试A，实际得到{adddata}"
        assert not self.item.has_fail_message()

    @allure.story("修改物料代码成功")
    # @pytest.mark.run(order=1)
    def test_materialInventory_editcodesuccess(self, login_to_item):
        # 选中1测试A物料代码
        self.item.click_button('//tr[./td[2][.//span[text()="1测试A"]]]/td[2]')
        # 点击修改按钮
        self.item.click_edi_button()
        sleep(1)

        text = "1测试A5"
        # 物料员代码输入
        self.item.enter_texts(
            "//div[@id='mbh7ra45-w560']//input", f"{text}"
        )
        # 点击确定
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="确定"]')
        sleep(3)
        # 定位表格内容
        itemdata = self.item.get_find_element_xpath(
            '//tr[./td[2][.//span[contains(text(),"1测试A")]]]/td[2]'
        ).text
        assert itemdata == text, f"预期{itemdata}"
        assert not self.item.has_fail_message()

    @allure.story("把修改后的物料代码改回来")
    # @pytest.mark.run(order=1)
    def test_materialInventory_editcodesuccess2(self, login_to_item):
        # 选中1测试A物料代码
        self.item.click_button('//tr[./td[2][.//span[contains(text(),"1测试A")]]]/td[2]')
        # 点击修改按钮
        self.item.click_edi_button()
        # 物料代码输入
        self.item.enter_texts("//div[@id='mbh7ra45-w560']//input", "1测试A")
        # 点击确定
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="确定"]')
        sleep(1)
        # 定位表格内容
        itemdata = self.item.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="1测试A"]]]/td[2]'
        ).text
        assert itemdata == "1测试A", f"预期{itemdata}"
        assert not self.item.has_fail_message()

    @allure.story("修改物料员代码重复")
    # @pytest.mark.run(order=1)
    def test_materialInventory_editrepeat(self, login_to_item):

        # 选中1测试A工厂代码
        self.item.click_button('//tr[./td[2][.//span[text()="1测试A"]]]/td[2]')
        # 点击修改按钮
        self.item.click_edi_button()
        # 物料代码等输入111
        input_xpath_list = [
            "//div[@id='mbh7ra45-w560']//input",
            "//div[@id='iywd9qev-4vy4']//input",
            "//div[@id='fie6kuba-cfam']//input",
            "//div[@id='fupxj7hi-szmt']//input",
        ]
        text_str = "111"
        self.item.batch_modify_input(input_xpath_list, text_str)
        # 点击确定
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="确定"]')
        sleep(2)
        # 获取重复弹窗文字
        error_popup = self.item.finds_elements(By.XPATH,
            '//div[text()=" 记录已存在,请检查！ "]'
        )
        self.item.click_button('//button[@type="button"]/span[text()="关闭"]')
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="取消"]')
        assert len(error_popup) == 1, f"预期数据{error_popup}"
        assert not self.item.has_fail_message()

    @allure.story("删除数据成功")
    # @pytest.mark.run(order=1)
    def test_materialInventory_delsuccess1(self, login_to_item):
        # self.driver.refresh()
        self.item.wait_for_loading_to_disappear()
        # 定位内容为‘111’的行
        self.item.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
        self.item.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        self.item.click_button('//div[@class="ivu-modal-confirm-footer"]//span[text()="确定"]')
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
    def test_materialInventory_editnamesuccess(self, login_to_item):
        # 输入框要修改的值
        text_str = "111"
        text_data = '2025/07/22 00:00:00'

        # 输入框的xpath
        input_xpath_list = [
            "//div[@id='fupxj7hi-szmt']//input",
            "//div[@id='zo2th84z-lzcg']//input",
            "//div[@id='ut62fa19-gqyk']//input",
            "//div[@id='n43xlnyi-8vxq']//input",
            "//div[@id='j7e4dz0t-7bu7']//input",
            "//div[@id='e7jp9yzi-3jrr']//input",
            "//div[@id='umifk57o-6nj0']//input",
            "//div[@id='f48ogbqr-1fyp']//input",
            "//div[@id='8hhvl5a5-dg4a']//input",
            "//div[@id='5irc95ma-qlzd']//input",
            "//div[@id='b3454i51-rjs9']//input",
            "//div[@id='ajr6t1t4-st8n']//input",
            "//div[@id='l1jwux78-7e0b']//input"
        ]
        date_xpath_list = [
            "//div[@id='5byn7w43-z68c']//input",
            "//div[@id='ix0na2xh-iett']//input",
            "//div[@id='z89r55rm-tc4a']//input",
            "//div[@id='mfqqixga-6491']//input",
            "//div[@id='4fspdcgb-r6yu']//input",
            "//div[@id='1t48zhco-fwz6']//input",
            "//div[@id='tn39rj1c-kfyx']//input",
        ]
        sleep(6)
        # 选中工厂代码
        self.item.click_button('//tr[./td[2][.//span[text()="1测试A"]]]/td[2]')
        # 点击修改按钮
        self.item.click_edi_button()
        sleep(1)

        input_icon_list = [
            "//div[@id='mbh7ra45-w560']//i",
            "//div[@id='ryeanffg-5o1d']//i",
        ]
        text_list = self.item.batch_modify_dialog_box(
            input_icon_list,
            '(//div[@id="dialogCanvas"]//table//tr[1]/td[2])'
        )

        input_icon_list2 = [
            "//div[@id='iywd9qev-4vy4']//i",
        ]
        input_icon_list3 = [
            "//div[@id='fie6kuba-cfam']//i",
        ]
        text_list2 = self.item.batch_modify_dialog_box(
            input_icon_list2,
            '(//div[@id="dialogCanvas"]//table//tr[1]/td[3])'
        )

        text_list3 = self.item.batch_modify_dialog_box(
            input_icon_list3,
            '(//div[@id="dialogCanvas"]//table//tr[1]/td[5])'
        )
        # 批量修改输入框
        self.item.batch_modify_input(input_xpath_list, text_str)
        self.item.batch_modify_input(date_xpath_list, text_data)

        sleep(1)
        # 点击确定
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="确定"]')
        sleep(1)
        # 选中物料员代码
        self.item.click_button('//tr[./td[7][.//span[text()="111"]]]/td[2]')
        # 点击编辑按钮
        self.item.click_edi_button()
        sleep(1)
        # 批量获取输入框的value
        input_values = self.item.batch_acquisition_input(input_xpath_list, text_str)
        date_values = self.item.batch_acquisition_input(date_xpath_list, text_data)
        # 批量获取弹窗式输入框的value
        pop_input_val = self.item.batch_acquisition_input_list([
            "//div[@id='mbh7ra45-w560']//input",
            "//div[@id='ryeanffg-5o1d']//input",
        ], text_list)
        pop_input_val2 = self.item.batch_acquisition_input_list([
            "//div[@id='iywd9qev-4vy4']//input",
        ], text_list2)
        pop_input_val3 = self.item.batch_acquisition_input_list([
            "//div[@id='fie6kuba-cfam']//input"
        ], text_list3)
        print('input_values', input_values)
        sleep(1)
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="取消"]')
        assert (
                len(input_xpath_list) == len(input_values) and
                len(date_xpath_list) == len(date_values) and
                len(pop_input_val) == len(input_icon_list) and
                len(pop_input_val2) == len(input_icon_list2) and
                len(pop_input_val3) == len(input_icon_list3)
        )
        assert not self.item.has_fail_message()

    @allure.story("删除测试数据成功")
    # @pytest.mark.run(order=1)
    def test_materialInventory_delsuccess2(self, login_to_item):

        # 定位内容为‘1测试A’的行
        self.item.click_button('//tr[./td[7][.//span[text()="111"]]]/td[2]')
        self.item.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        self.item.click_button('//div[@class="ivu-modal-confirm-footer"]//span[text()="确定"]')
        self.item.click_ref_button()
        sleep(1)
        # 定位内容为‘1测试A’的行
        itemdata = self.driver.find_elements(
            By.XPATH, '//tr[./td[2][.//span[text()="1测试A"]]]/td[2]'
        )
        assert len(itemdata) == 0
        assert not self.item.has_fail_message()

    @allure.story("刷新成功")
    # @pytest.mark.run(order=1)
    def test_materialInventory_refreshsuccess(self, login_to_item):

        filter_results = self.item.filter_method('//span[text()=" 物料代码"]/ancestor::div[3]//span//span//span')
        print('filter_results', filter_results)
        assert filter_results
        assert not self.item.has_fail_message()

    @allure.story("新增全部数据测试")
    # @pytest.mark.run(order=1)
    def test_materialInventory_add_success(self, login_to_item):
        # 输入框的xpath
        input_xpath_list = [
            "//div[@id='u2tgl5h9-otp1']//input",
            "//div[@id='o7c9sdve-vat3']//input",
            "//div[@id='ctfddy1k-hbmj']//input",
            "//div[@id='z0h20cps-xzrs']//input",
            "//div[@id='0t8pfkrw-y5i1']//input",
            "//div[@id='7z1rv7fs-trb6']//input",
            "//div[@id='8sgoh6vh-0pz5']//input",
            "//div[@id='hguo4esk-gii0']//input",
            "//div[@id='poxayyhi-9bss']//input",
            "//div[@id='13j55ae1-8hj2']//input",
            "//div[@id='zxc6ccwu-bnwe']//input",
            "//div[@id='15qig6pt-sj1x']//input",
            "//div[@id='wcmoz0yh-ws7q']//input",
        ]
        input_xpath_list2 = [
            "//div[@id='fupxj7hi-szmt']//input",
            "//div[@id='zo2th84z-lzcg']//input",
            "//div[@id='ut62fa19-gqyk']//input",
            "//div[@id='n43xlnyi-8vxq']//input",
            "//div[@id='j7e4dz0t-7bu7']//input",
            "//div[@id='e7jp9yzi-3jrr']//input",
            "//div[@id='umifk57o-6nj0']//input",
            "//div[@id='f48ogbqr-1fyp']//input",
            "//div[@id='8hhvl5a5-dg4a']//input",
            "//div[@id='5irc95ma-qlzd']//input",
            "//div[@id='b3454i51-rjs9']//input",
            "//div[@id='ajr6t1t4-st8n']//input",
            "//div[@id='l1jwux78-7e0b']//input"
        ]
        # 日期的xpath
        date_xpath_list = [
            "//div[@id='ol0ayk71-opoa']//input",
            "//div[@id='pl90foml-jz2e']//input",
            "//div[@id='11ew19wa-ewfe']//input",
            "//div[@id='c3shlmru-g5i5']//input",
            "//div[@id='lirza5xs-rqhz']//input",
            "//div[@id='jlqyf2aj-bbmd']//input",
            "//div[@id='eyfbw7wv-2mom']//input",
        ]
        date_xpath_list2 = [
            "//div[@id='5byn7w43-z68c']//input",
            "//div[@id='ix0na2xh-iett']//input",
            "//div[@id='z89r55rm-tc4a']//input",
            "//div[@id='mfqqixga-6491']//input",
            "//div[@id='4fspdcgb-r6yu']//input",
            "//div[@id='1t48zhco-fwz6']//input",
            "//div[@id='tn39rj1c-kfyx']//input",
        ]
        sleep(4)
        # 输入框要修改的值
        text_str = "111"
        # 日期要修改的值
        date_str = "2025/07/17 00:00:00"
        self.item.click_add_button()  # 点击添加
        sleep(1)

        input_icon_list = [
            "//div[@id='p34nag46-7evf']//i",
            "//div[@id='fgobbtop-s46e']//i",
        ]
        text_list = self.item.batch_modify_dialog_box(
            input_icon_list,
            '(//div[@id="dialogCanvas"]//table//tr[1]/td[2])'
        )

        input_icon_list2 = [
            "//div[@id='ywz9q11i-sp3b']//i",
        ]
        text_list2 = self.item.batch_modify_dialog_box(
            input_icon_list2,
            '(//div[@id="dialogCanvas"]//table//tr[1]/td[3])'
        )

        input_icon_list3 = [
            "//div[@id='x1k7t87i-tvc3']//i",
        ]

        text_list3 = self.item.batch_modify_dialog_box(
            input_icon_list3,
            '(//div[@id="dialogCanvas"]//table//tr[1]/td[5])'
        )

        print('text_list', text_list)
        print('text_list2', text_list2)
        print('text_list3', text_list3)

        # 批量修改输入框
        self.item.batch_modify_input(input_xpath_list, text_str)
        # 批量修改日期
        self.item.batch_modify_input(date_xpath_list, date_str)

        sleep(1)
        # 点击确定
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="确定"]')
        sleep(1)
        # 选中物料代码
        self.item.click_button('//tr[./td[7][.//span[text()="111"]]]/td[2]')
        # 点击编辑按钮
        self.item.click_edi_button()
        sleep(1)
        # 批量获取输入框的value
        input_values = self.item.batch_acquisition_input(input_xpath_list2, text_str)
        # 批量获取日期的value
        date_values = self.item.batch_acquisition_input(date_xpath_list2, date_str)
        # 批量获取弹窗式输入框的value
        pop_input_val = self.item.batch_acquisition_input_list([
            "//div[@id='mbh7ra45-w560']//input",
            "//div[@id='ryeanffg-5o1d']//input",
        ], text_list)
        pop_input_val2 = self.item.batch_acquisition_input_list([
            "//div[@id='iywd9qev-4vy4']//input",
        ], text_list2)
        pop_input_val3 = self.item.batch_acquisition_input_list([
            "//div[@id='fie6kuba-cfam']//input",
        ], text_list3)
        sleep(1)
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="取消"]')
        assert (
                len(input_xpath_list) == len(input_values)
                and len(date_xpath_list) == len(date_values)
                and len(pop_input_val) == len(input_icon_list)
                and len(pop_input_val2) == len(input_icon_list2)
                and len(pop_input_val3) == len(input_icon_list3)
        )
        assert not self.item.has_fail_message()

    @allure.story("查询物料代码成功")
    # @pytest.mark.run(order=1)
    def test_materialInventory_selectcodesuccess(self, login_to_item):
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
        item.click_button('//div[text()="批次号" and contains(@optid,"opt_")]')
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
        item.click_select_button()
        # 定位第一行是否为产品A
        itemcode = item.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[1]/td[7]'
        ).text
        # 定位第二行没有数据
        itemcode2 = driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[2]/td[2]',
        )
        assert itemcode == "111" and len(itemcode2) == 0
        assert not item.has_fail_message()

    @allure.story("没有数据时显示正常")
    # @pytest.mark.run(order=1)
    def test_materialInventory_selectnodatasuccess(self, login_to_item):

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
        # 点击物料代码
        self.item.click_button('//div[text()="物料代码" and contains(@optid,"opt_")]')
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
        self.item.click_select_button()
        itemcode = self.driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[1]/td[2]',
        )
        self.item.click_ref_button()
        assert len(itemcode) == 0
        assert not self.item.has_fail_message()

    @allure.story("过滤条件查询，一个不选，显示正常")
    # @pytest.mark.run(order=1)
    def test_materialInventory_select2(self, login_to_item):
        self.item.click_button('//div[div[span[text()=" 物料代码"]]]//i[contains(@class,"suffixIcon")]')
        sleep(1)
        eles = self.item.get_find_element_xpath(
            '(//div[@class="vxe-pulldown--panel-wrapper"])//label/span').get_attribute(
            "class")
        if eles == "ivu-checkbox ivu-checkbox-checked":
            self.item.click_button('(//div[@class="vxe-pulldown--panel-wrapper"])//label/span')
            self.item.click_button('//div[@class="filter-btn-bar"]/button')
        sleep(1)
        self.item.click_button('//div[div[span[text()=" 物料代码"]]]//input')
        eles = self.item.finds_elements(By.XPATH, '//table[@class="vxe-table--body"]//tr//td[2]')
        self.item.right_refresh('物料库存')
        assert len(eles) == 0
        assert not self.item.has_fail_message()

    @allure.story("过滤条件查询，设置包含条件查询成功")
    # @pytest.mark.run(order=1)
    def test_materialInventory_select3(self, login_to_item):
        name = self.item.get_find_element_xpath(
            '//div[@class="vxe-table--body-wrapper body--wrapper"]/table[@class="vxe-table--body"]//tr[2]//td[2]'
        ).get_attribute('innerText')
        first_char = name[:1] if name else ""
        self.item.click_button('//div[div[span[text()=" 物料代码"]]]//i[contains(@class,"suffixIcon")]')
        self.item.hover("包含")
        sleep(1)
        self.item.select_input('物料代码', first_char)
        sleep(1)
        eles = self.item.finds_elements(By.XPATH, '//table[@class="vxe-table--body"]//tr//td[2]')
        sleep(1)
        list_ = [ele.text for ele in eles]
        self.item.right_refresh('物料库存')
        assert all(first_char in text for text in list_)
        assert not self.item.has_fail_message()

    @allure.story("过滤条件查询，设置符合开头查询成功")
    # @pytest.mark.run(order=1)
    def test_materialInventory_select4(self, login_to_item):
        name = self.item.get_find_element_xpath(
            '//div[@class="vxe-table--body-wrapper body--wrapper"]/table[@class="vxe-table--body"]//tr[2]//td[2]'
        ).get_attribute('innerText')
        first_char = name[:1] if name else ""
        self.item.click_button('//div[div[span[text()=" 物料代码"]]]//i[contains(@class,"suffixIcon")]')
        self.item.hover("符合开头")
        sleep(1)
        self.item.select_input('物料代码', first_char)
        sleep(1)
        eles = self.item.finds_elements(By.XPATH, '//table[@class="vxe-table--body"]//tr//td[2]')
        sleep(1)
        list_ = [ele.text for ele in eles]
        self.item.right_refresh('物料库存')
        assert all(str(item).startswith(first_char) for item in list_)
        assert not self.item.has_fail_message()

    @allure.story("过滤条件查询，设置符合结尾查询成功")
    # @pytest.mark.run(order=1)
    def test_materialInventory_select5(self, login_to_item):
        name = self.item.get_find_element_xpath(
            '//div[@class="vxe-table--body-wrapper body--wrapper"]/table[@class="vxe-table--body"]//tr[2]//td[2]'
        ).get_attribute('innerText')
        last_char = name[-1:] if name else ""
        self.item.click_button('//div[div[span[text()=" 物料代码"]]]//i[contains(@class,"suffixIcon")]')
        self.item.hover("符合结尾")
        sleep(1)
        self.item.select_input('物料代码', last_char)
        sleep(1)
        eles = self.item.finds_elements(By.XPATH, '//table[@class="vxe-table--body"]//tr//td[2]')
        sleep(1)
        list_ = [ele.text for ele in eles]
        self.item.right_refresh('物料库存')
        assert all(str(item).endswith(last_char) for item in list_)
        assert not self.item.has_fail_message()

    @allure.story("清除筛选效果成功")
    # @pytest.mark.run(order=1)
    def test_materialInventory_clear(self, login_to_item):
        name = "3"
        sleep(1)
        self.item.click_button('//div[div[span[text()=" 物料代码"]]]//i[contains(@class,"suffixIcon")]')
        self.item.hover("包含")
        sleep(1)
        self.item.select_input('物料代码', name)
        sleep(1)
        self.item.click_button('//div[div[span[text()=" 物料代码"]]]//i[contains(@class,"suffixIcon")]')
        self.item.hover("清除所有筛选条件")
        sleep(1)
        ele = self.item.get_find_element_xpath(
            '//div[div[span[text()=" 物料代码"]]]//i[contains(@class,"suffixIcon")]').get_attribute(
            "class")
        self.item.right_refresh('物料库存')
        assert ele == "vxe-icon-funnel suffixIcon"
        assert not self.item.has_fail_message()

    @allure.story("模拟ctrl+i添加重复")
    # @pytest.mark.run(order=1)
    def test_materialInventory_ctrlIrepeat(self, login_to_item):
        self.item.click_button('//table[@class="vxe-table--body"]//tr[2]//td[2]')
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('i').key_up(Keys.CONTROL).perform()
        ele1 = self.item.get_find_element_xpath('(//table[@class="vxe-table--body"]//tr[1]/td[2])[2]').get_attribute(
            "innerText")
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="确定"]')
        message = self.item.get_find_element_xpath('//div[text()=" 记录已存在,请检查！ "]').get_attribute("innerText")
        self.item.click_button('//div[@class="ivu-modal-footer"]//span[text()="关闭"]')
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="取消"]')
        assert message == '记录已存在,请检查！'
        assert not self.item.has_fail_message()

    @allure.story("模拟ctrl+i添加")
    # @pytest.mark.run(order=1)
    def test_materialInventory_ctrlI(self, login_to_item):
        self.item.click_button('//table[@class="vxe-table--body"]//tr[2]//td[2]')
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('i').key_up(Keys.CONTROL).perform()
        self.item.click_button('(//table[@class="vxe-table--body"]//tr[1]/td[2])[2]')
        self.item.enter_texts('(//table[@class="vxe-table--body"]//tr[1]/td[2])[2]//input', '1没有数据添加')
        sleep(1)
        ele1 = self.item.get_find_element_xpath(
            '(//table[@class="vxe-table--body"]//tr[1]/td[2])[2]//input').get_attribute(
            "value")
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="确定"]')
        self.item.get_find_message()
        self.item.select_input('物料代码', '1没有数据添加')
        ele2 = self.item.get_find_element_xpath('(//table[@class="vxe-table--body"]//tr[1]/td[2])[1]').get_attribute(
            "innerText")
        assert ele1 == ele2 == '1没有数据添加'
        assert not self.item.has_fail_message()

    @allure.story("模拟ctrl+m修改")
    # @pytest.mark.run(order=1)
    def test_materialInventory_ctrlM(self, login_to_item):
        self.item.click_button('//table[@class="vxe-table--body"]//tr[1]//td[2]')
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('m').key_up(Keys.CONTROL).perform()
        self.item.click_button('(//table[@class="vxe-table--body"]//tr[1]/td[2])[2]')
        self.item.enter_texts('(//table[@class="vxe-table--body"]//tr[1]/td[2])[2]//input', '1没有数据修改')
        ele1 = self.item.get_find_element_xpath(
            '(//table[@class="vxe-table--body"]//tr[1]/td[2])[2]//input').get_attribute(
            "value")
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="确定"]')
        self.item.get_find_message()
        self.item.select_input('物料代码', '1没有数据修改')
        ele2 = self.item.get_find_element_xpath('(//table[@class="vxe-table--body"]//tr[1]/td[2])[1]').get_attribute(
            "innerText")
        assert ele1 == ele2
        assert not self.item.has_fail_message()

    @allure.story("模拟多选删除")
    # @pytest.mark.run(order=1)
    def test_materialInventory_shiftdel(self, login_to_item):
        self.item.right_refresh('物料库存')
        elements = ['(//table[@class="vxe-table--body"]//tr[1]//td[1])[2]',
                    '(//table[@class="vxe-table--body"]//tr[2]//td[1])[2]']
        self.item.click_button(elements[0])
        # 第二个单元格 Shift+点击（选择范围）
        cell2 = self.item.get_find_element_xpath(elements[1])
        ActionChains(self.driver).key_down(Keys.SHIFT).click(cell2).key_up(Keys.SHIFT).perform()
        sleep(1)
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('i').key_up(Keys.CONTROL).perform()
        self.item.click_button('(//table[@class="vxe-table--body"]//tr[1]/td[2])[2]')
        self.item.enter_texts('(//table[@class="vxe-table--body"]//tr[1]/td[2])[2]//input', '1没有数据修改1')
        self.item.click_button('(//table[@class="vxe-table--body"]//tr[2]/td[2])[2]')
        self.item.enter_texts('(//table[@class="vxe-table--body"]//tr[2]/td[2])[2]//input', '1没有数据修改12')
        sleep(1)
        ele1 = self.item.get_find_element_xpath(
            '(//table[@class="vxe-table--body"]//tr[1]/td[2])[2]').text
        ele2 = self.item.get_find_element_xpath(
            '(//table[@class="vxe-table--body"]//tr[2]/td[2])[2]//input').get_attribute("value")
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="确定"]')
        self.item.get_find_message()
        self.item.select_input('物料代码', '1没有数据修改1')
        ele11 = self.item.get_find_element_xpath('(//table[@class="vxe-table--body"]//tr[1]/td[2])[1]').get_attribute(
            "innerText")
        ele22 = self.item.get_find_element_xpath('(//table[@class="vxe-table--body"]//tr[2]/td[2])[1]').get_attribute(
            "innerText")
        assert ele1 == ele11 and ele2 == ele22
        assert not self.item.has_fail_message()
        self.item.select_input('物料代码', '1没有数据修改')
        before_data = self.item.get_find_element_xpath('(//span[contains(text(),"条记录")])[1]').text
        before_count = int(re.search(r'\d+', before_data).group())
        elements = ['(//table[@class="vxe-table--body"]//tr[1]//td[1])[2]',
                    '(//table[@class="vxe-table--body"]//tr[2]//td[1])[2]',
                    '(//table[@class="vxe-table--body"]//tr[3]//td[1])[2]']
        self.item.click_button(elements[0])
        # 第二个单元格 Shift+点击（选择范围）
        cell2 = self.item.get_find_element_xpath(elements[2])
        ActionChains(self.driver).key_down(Keys.SHIFT).click(cell2).key_up(Keys.SHIFT).perform()
        sleep(1)
        self.item.click_del_button()
        self.item.click_button('//div[@class="ivu-modal-confirm-footer"]//span[text()="确定"]')
        message = self.item.get_find_message()
        self.item.wait_for_loading_to_disappear()
        after_data = self.item.get_find_element_xpath('(//span[contains(text(),"条记录")])[1]').text
        after_count = int(re.search(r'\d+', after_data).group())
        assert message == "删除成功！"
        assert before_count - after_count == 3, f"删除失败: 删除前 {before_count}, 删除后 {after_count}"
        assert not self.item.has_fail_message()

    @allure.story("模拟ctrl+c复制可查询")
    # @pytest.mark.run(order=1)
    def test_materialInventory_ctrlC(self, login_to_item):
        self.item.right_refresh('物料库存')
        self.item.click_button('//table[@class="vxe-table--body"]//tr[2]//td[2]')
        before_data = self.item.get_find_element_xpath('//table[@class="vxe-table--body"]//tr[2]//td[2]').text
        sleep(1)
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
        self.item.click_button('//div[div[span[text()=" 物料代码"]]]//input')
        sleep(1)
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        eles = self.item.finds_elements(By.XPATH, '//table[@class="vxe-table--body"]//tr[2]//td[2]')
        eles = [ele.text for ele in eles]
        self.item.right_refresh('物料库存')
        assert all(before_data in ele for ele in eles)
        assert not self.item.has_fail_message()

    @allure.story("模拟Shift+点击可多选ctrl+i添加")
    # @pytest.mark.run(order=1)
    def test_materialInventory_shift(self, login_to_item):
        elements = ['(//table[@class="vxe-table--body"]//tr[1]//td[1])[2]',
                    '(//table[@class="vxe-table--body"]//tr[2]//td[1])[2]']
        self.item.click_button(elements[0])
        # 第二个单元格 Shift+点击（选择范围）
        cell2 = self.item.get_find_element_xpath(elements[1])
        ActionChains(self.driver).key_down(Keys.SHIFT).click(cell2).key_up(Keys.SHIFT).perform()
        sleep(1)
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('i').key_up(Keys.CONTROL).perform()
        num = self.item.finds_elements(By.XPATH, '(//table[@class="vxe-table--body"])[last()]//tr')
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="取消"]')
        assert len(num) == 2
        assert not self.item.has_fail_message()

    @allure.story("模拟Shift+点击可多选ctrl+m编辑")
    # @pytest.mark.run(order=1)
    def test_materialInventory_ctrls(self, login_to_item):
        elements = ['(//table[@class="vxe-table--body"]//tr[1]//td[1])[2]',
                    '(//table[@class="vxe-table--body"]//tr[2]//td[1])[2]']
        self.item.click_button(elements[0])
        # 第二个单元格 Shift+点击（选择范围）
        cell2 = self.item.get_find_element_xpath(elements[1])
        ActionChains(self.driver).key_down(Keys.CONTROL).click(cell2).key_up(Keys.CONTROL).perform()
        sleep(1)
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('m').key_up(Keys.CONTROL).perform()
        num = self.item.finds_elements(By.XPATH, '(//table[@class="vxe-table--body"])[last()]//tr')
        self.item.click_button('//div[@class="vxe-modal--footer"]//span[text()="确定"]')
        message = self.item.get_find_message()
        assert len(num) == 2 and message == "保存成功"
        assert not self.item.has_fail_message()

    @allure.story("删除数据成功")
    # @pytest.mark.run(order=1)
    def test_materialInventory_delsuccess3(self, login_to_item):
        # 定位内容为‘111’的行
        self.item.wait_for_loading_to_disappear()
        self.item.click_button('//tr[./td[7][.//span[text()="111"]]]/td[2]')
        self.item.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        self.item.click_button('//div[@class="ivu-modal-confirm-footer"]//span[text()="确定"]')
        self.item.click_ref_button()
        sleep(1)
        layout = self.driver.find_elements(By.CLASS_NAME, "tabsDivItem")
        layout_name = "测试布局A"
        if len(layout) > 1:
            self.item.del_layout(layout_name)
        # 定位内容为‘111’的行
        itemdata = self.driver.find_elements(
            By.XPATH, '//tr[./td[2][.//span[text()="111"]]]/td[2]'
        )
        assert len(itemdata) == 0
        assert not self.item.has_fail_message()

    # def test_demo(self, login_to_item):
    #     # 获取所有button子元素
    #     sleep(5)
    #     layout = self.driver.find_elements(By.CLASS_NAME, "tabsDivItem")
    #     print('layout',len(layout))
    #     input()
