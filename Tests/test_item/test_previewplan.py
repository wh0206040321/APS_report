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

from Pages.login_page import LoginPage
from Pages.operationPlan_page import operationPlanPage
from Pages.previewPlan_page import PreviewPlanPage
from Utils.data_driven import DateDriver
from Utils.shared_data_util import SharedDataUtil
from Utils.driver_manager import create_driver, safe_quit, all_driver_instances


@pytest.fixture  # (scope="class")这个参数表示整个测试类共用同一个浏览器，默认一个用例执行一次
def login_to_previewPlan():
    """初始化并返回 driver"""
    driver_path = DateDriver().driver_path
    driver = create_driver(driver_path)
    driver.implicitly_wait(3)

    # 初始化登录页面
    page = LoginPage(driver)  # 初始化登录页面
    page.navigate_to(DateDriver().url)  # 导航到登录页面
    page.login(DateDriver().username, DateDriver().password, DateDriver().planning)
    page.click_button('(//span[text()="计划管理"])[1]')  # 点击计划管理
    page.click_button('(//span[text()="计划业务数据"])[1]')  # 点击计划业务数据
    page.click_button('(//span[text()="工作指示一览"])[1]')  # 点击工作指示一览
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("工作指示一览表测试用例")
@pytest.mark.run(order=21)
class TestPreviewPlanPage:
    @allure.story("工作指示发布成功，工作指示一览显示成功")
    # @pytest.mark.run(order=1)
    def test_previewPlan_select(self, login_to_previewPlan):
        driver = login_to_previewPlan  # WebDriver 实例
        previewPlan = PreviewPlanPage(driver)  # 用 previewPlan 初始化 PreviewPlanPage
        shared_data = SharedDataUtil.load_data()
        resource1 = shared_data.get("master_res1")
        resource2 = shared_data.get("master_res2")
        previewPlan.enter_texts(
            '//div[./p[text()="订单代码"]]/parent::div//input', "1测试C订单"
        )
        ele_code1 = previewPlan.get_find_element_xpath(
            '//table[.//td[4]//span[text()="1测试C订单"]]//tr[1]/td[4]'
        ).text
        ele_resource1 = previewPlan.get_find_element_xpath(
            '//table[.//td[4]//span[text()="1测试C订单"]]//tr[1]/td[7]'
        ).text
        ele_code2 = previewPlan.get_find_element_xpath(
            '//table[.//td[4]//span[text()="1测试C订单"]]//tr[2]/td[4]'
        ).text
        ele_resource2 = previewPlan.get_find_element_xpath(
            '//table[.//td[4]//span[text()="1测试C订单"]]//tr[2]/td[7]'
        ).text
        assert (
            ele_code1 == "1测试C订单"
            and ele_resource1 == resource1
            and ele_code2 == "1测试C订单"
            and ele_resource2 == resource2
        )
        assert not previewPlan.has_fail_message()

    @allure.story("删除工作指示成功，并且工作指示发布重新可以查询信息")
    # @pytest.mark.run(order=1)
    def test_previewPlan_delete(self, login_to_previewPlan):
        driver = login_to_previewPlan  # WebDriver 实例
        previewPlan = PreviewPlanPage(driver)  # 用 previewPlan 初始化 PreviewPlanPage
        operationPlan = operationPlanPage(driver)
        shared_data = SharedDataUtil.load_data()
        resource1 = shared_data.get("master_res1")
        resource2 = shared_data.get("master_res2")
        previewPlan.enter_texts(
            '//div[./p[text()="订单代码"]]/parent::div//input', "1测试C订单"
        )
        ele_resource1 = previewPlan.get_find_element_xpath(
            '//table[.//td[4]//span[text()="1测试C订单"]]//tr[1]/td[7]'
        ).text
        ele_resource2 = previewPlan.get_find_element_xpath(
            '//table[.//td[4]//span[text()="1测试C订单"]]//tr[2]/td[7]'
        ).text
        if ele_resource1 == resource1 and ele_resource2 == resource2:
            sleep(2)
            previewPlan.click_button(
                '(//span[@class="vxe-checkbox--icon vxe-icon-checkbox-unchecked"])[2]'
            )
            sleep(1)
            previewPlan.click_del_button()
            previewPlan.click_button('(//button[@class="ivu-btn ivu-btn-primary"])[2]')
        sleep(1)
        ele_none = driver.find_elements(
            By.XPATH, '//table[.//td[4]//span[text()="1测试C订单"]]/tbody//tr'
        )

        previewPlan.click_button('(//span[text()="工作指示发布"])[1]')
        # 搜索框输入资源代码
        operationPlan.enter_texts(
            '(//div[./p[text()="资源代码"]]/following-sibling::div//input)[1]',
            f"{resource1}",
        )
        # 勾选资源
        sleep(1)
        row_number = driver.execute_script(
            "return document.evaluate("
            f'"count(//tr[.//span[text()=\\"{resource1}\\"]]/preceding-sibling::tr) + 1",'
            "document, null, XPathResult.NUMBER_TYPE, null"
            ").numberValue;"
        )
        print(f"行号: {int(row_number)}")
        operationPlan.click_button(
            f'//table[@style="width: 140px; margin-top: 0px;"]//tr[{int(row_number)}]/td[2]//span[1]/span'
        )
        sleep(1)
        # 清除资源代码的输入
        ele = operationPlan.get_find_element_xpath(
            '(//div[./p[text()="资源代码"]]/following-sibling::div//input)[1]'
        )
        ele.send_keys(Keys.CONTROL, "a")
        ele.send_keys(Keys.DELETE)
        # 搜索框输入资源代码
        operationPlan.enter_texts(
            '(//div[./p[text()="资源代码"]]/following-sibling::div//input)[1]',
            f"{resource2}",
        )
        sleep(1)
        # 勾选资源
        row_number2 = driver.execute_script(
            "return document.evaluate("
            f'"count(//tr[.//span[text()=\\"{resource2}\\"]]/preceding-sibling::tr) + 1",'
            "document, null, XPathResult.NUMBER_TYPE, null"
            ").numberValue;"
        )
        print(f"行号: {int(row_number2)}")
        operationPlan.click_button(
            f'//table[@style="width: 140px; margin-top: 0px;"]//tr[{int(row_number2)}]/td[2]//span[1]/span'
        )
        # 清除资源代码的输入
        ele = operationPlan.get_find_element_xpath(
            '(//div[./p[text()="资源代码"]]/following-sibling::div//input)[1]'
        )
        ele.send_keys(Keys.CONTROL, "a")
        ele.send_keys(Keys.DELETE)

        # 打开时间段选择弹窗（点击时间选择按钮）
        operationPlan.click_inputbutton()
        # 选择当前日期（点击带有 today 和 focused 样式的日期单元格）
        operationPlan.click_button(
            '//span[@class="ivu-date-picker-cells-cell ivu-date-picker-cells-cell-today ivu-date-picker-cells-focused"]'
        )
        # 点击下月按钮
        operationPlan.click_button(
            '(//span[@class="ivu-picker-panel-icon-btn ivu-date-picker-next-btn ivu-date-picker-next-btn-arrow"])[2]/i')
        sleep(0.5)
        operationPlan.click_button(
            '(//span[@class="ivu-picker-panel-icon-btn ivu-date-picker-next-btn ivu-date-picker-next-btn-arrow"])[2]/i')
        # 选择具体的时间点（例如：28 日）
        operationPlan.click_button('(//em[text()="28"])[last()]')
        # 点击确认按钮以完成时间段的选择
        operationPlan.click_okbutton()

        # 点击查询
        operationPlan.click_selebutton()
        operationPlan.enter_texts(
            '//div[./p[text()="订单代码"]]/parent::div//input', "1测试C订单"
        )

        input_text1 = operationPlan.get_find_element_xpath(
            f'(//table[.//span[text()="{resource1}"]])[last()]//tr[1]//td[7]'
        ).text
        input_text2 = operationPlan.get_find_element_xpath(
            f'(//table[.//span[text()="{resource2}"]])[last()]//tr[2]//td[7]'
        ).text
        input_text3 = driver.find_elements(
            By.XPATH, '(//tr[.//span[text()="1测试C订单"]])[3]'
        )

        operationPlan.click_button('//p[text()="工作指示发布"]')
        operationPlan.click_button('(//button[@class="ivu-btn ivu-btn-primary"])[2]')
        sleep(2)
        after_text = driver.find_elements(
            By.XPATH, '(//table[@class="vxe-table--body"])[3]/tbody//tr'
        )

        # 验证提示信息是否符合预期
        assert (
            input_text1 == resource1
            and input_text2 == resource2
            and len(input_text3) == 0
            and len(ele_none) == 0
            and len(after_text) == 0
        )
        assert not previewPlan.has_fail_message()
