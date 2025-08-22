import logging
from datetime import datetime
from time import sleep

import allure
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

from Pages.itemsPage.adds_page import AddsPages
from Pages.itemsPage.sched_page import SchedPage
from Pages.systemPage.imp_page import ImpPage
from Pages.systemPage.psi_page import PsiPage
from Pages.systemPage.planUnit_page import PlanUnitPage
from Pages.itemsPage.login_page import LoginPage
from Utils.data_driven import DateDriver
from Utils.driver_manager import create_driver, safe_quit, capture_screenshot


@pytest.fixture  # (scope="class")这个参数表示整个测试类共用同一个浏览器，默认一个用例执行一次
def login_to_planUnit():
    """初始化并返回 driver"""
    date_driver = DateDriver()
    driver = create_driver(date_driver.driver_path)
    driver.implicitly_wait(3)

    # 初始化登录页面
    page = LoginPage(driver)  # 初始化登录页面
    url = date_driver.url
    print(f"[INFO] 正在导航到 URL: {url}")
    # 尝试访问 URL，捕获连接错误
    for attempt in range(2):
        try:
            page.navigate_to(url)
            break
        except WebDriverException as e:
            capture_screenshot(driver, f"login_fail_{attempt + 1}")
            logging.warning(f"第 {attempt + 1} 次连接失败: {e}")
            driver.refresh()
            sleep(date_driver.URL_RETRY_WAIT)
    else:
        logging.error("连接失败多次，测试中止")
        safe_quit(driver)
        raise RuntimeError("无法连接到登录页面")

    page.login(date_driver.username, date_driver.password, date_driver.planning)
    list_ = ["系统管理", "系统设置", "计划单元"]
    for v in list_:
        page.click_button(f'(//span[text()="{v}"])[1]')
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("计划单元页用例")
@pytest.mark.run(order=204)
class TestPlanUnitPage:

    @allure.story("添加计划单元 不填写数据点击确认 不允许提交")
    # @pytest.mark.run(order=1)
    def test_planUnit_addfail(self, login_to_planUnit):
        driver = login_to_planUnit  # WebDriver 实例
        unit = PlanUnitPage(driver)  # 用 driver 初始化 PlanUnitPage
        add = AddsPages(driver)
        layout = "测试布局A"
        add.add_layout(layout)
        # 获取布局名称的文本元素
        name = unit.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        ).text

        unit.click_all_button("新增")
        list_ = [
            '(//label[text()="计划单元"])[1]/parent::div//input',
            '(//label[text()="计划单元名称"])[1]/parent::div//input',
            '(//label[text()="模板名称"])[1]/parent::div//div[@class="ivu-select-selection"]',
        ]
        unit.click_button('(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"]//span[text()="确定"])')
        sleep(1)
        value_list = add.get_border_color(list_)
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert all(value == expected_color for value in value_list)
        assert layout == name
        assert not unit.has_fail_message()

    @allure.story("添加计划单元 填写计划单元，不填写名称和模版 不允许提交")
    # @pytest.mark.run(order=1)
    def test_planUnit_addfail1(self, login_to_planUnit):
        driver = login_to_planUnit  # WebDriver 实例
        unit = PlanUnitPage(driver)  # 用 driver 初始化 PlanUnitPage
        add = AddsPages(driver)
        name = "1测试计划单元"
        unit.click_all_button("新增")
        list_ = [
            '(//label[text()="计划单元名称"])[1]/parent::div//input',
            '(//label[text()="模板名称"])[1]/parent::div//div[@class="ivu-select-selection"]',
        ]
        unit.enter_texts('(//label[text()="计划单元"])[1]/parent::div//input', name)
        unit.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"]//span[text()="确定"])')
        sleep(1)
        value_list = add.get_border_color(list_)
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert all(value == expected_color for value in value_list)
        assert not unit.has_fail_message()

    @allure.story("添加计划单元 填写计划单元，名称不填写模版 不允许提交")
    # @pytest.mark.run(order=1)
    def test_planUnit_addfail2(self, login_to_planUnit):
        driver = login_to_planUnit  # WebDriver 实例
        unit = PlanUnitPage(driver)  # 用 driver 初始化 PlanUnitPage
        add = AddsPages(driver)
        name = "1测试计划单元"
        unit.click_all_button("新增")
        list_ = [
            '(//label[text()="模板名称"])[1]/parent::div//div[@class="ivu-select-selection"]',
        ]
        unit.enter_texts('(//label[text()="计划单元"])[1]/parent::div//input', name)
        unit.enter_texts('(//label[text()="计划单元名称"])[1]/parent::div//input', name)
        unit.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"]//span[text()="确定"])')
        sleep(1)
        value_list = add.get_border_color(list_)
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert all(value == expected_color for value in value_list)
        assert not unit.has_fail_message()