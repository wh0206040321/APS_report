import logging
import os
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
from Pages.itemsPage.login_page import LoginPage
from Pages.systemPage.expression_page import ExpressionPage
from Utils.data_driven import DateDriver
from Utils.driver_manager import create_driver, safe_quit, capture_screenshot


@pytest.fixture  # (scope="class")这个参数表示整个测试类共用同一个浏览器，默认一个用例执行一次
def login_to_menu():
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
    list_ = ["系统管理", "系统设置", "菜单组件"]
    for v in list_:
        page.click_button(f'(//span[text()="{v}"])[1]')
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("菜单组件页用例")
@pytest.mark.run(order=213)
class TestSMenuPage:

    @allure.story("新增直接点击保存不允许添加")
    # @pytest.mark.run(order=1)
    def test_menu_addfail1(self, login_to_menu):
        driver = login_to_menu  # WebDriver 实例
        menu = ExpressionPage(driver)  # 用 driver 初始化 ExpressionPage
        sleep(1)
        menu.click_all_button("新增")
        sleep(1)
        menu.click_all_button("保存")
        message = menu.get_find_message()
        assert message == "请填写完整的信息才能提交"
        assert not menu.has_fail_message()


    @allure.story("新增只填写名称点击保存不允许添加")
    # @pytest.mark.run(order=1)
    def test_expression_addfail2(self, login_to_expression):
        driver = login_to_expression  # WebDriver 实例
        expression = ExpressionPage(driver)  # 用 driver 初始化 ExpressionPage
        name = '1测试表达式管理1'
        sleep(1)
        expression.click_all_button("新增")
        expression.enter_texts('//div[p[text()="名称: "]]//input', name)
        expression.click_all_button("保存")
        message = expression.get_find_message()
        assert message == "请填写完整的信息才能提交"
        assert not expression.has_fail_message()

    @allure.story("新增填写名称和分类点击保存不允许添加")
    # @pytest.mark.run(order=1)
    def test_expression_addfail3(self, login_to_expression):
        driver = login_to_expression  # WebDriver 实例
        expression = ExpressionPage(driver)  # 用 driver 初始化 ExpressionPage
        sleep(1)
        name = '1测试表达式管理1'
        expression.click_all_button("新增")
        expression.enter_texts('//div[p[text()="名称: "]]//input', name)
        expression.click_button('//div[p[text()="分类: "]]//input[@type="text"]')
        expression.click_button('//li[text()="图棒显示颜色"]')
        expression.click_all_button("保存")
        message = expression.get_find_message()
        assert message == "请填写完整的信息才能提交"
        assert not expression.has_fail_message()

    @allure.story("添加表达式管理成功")
    # @pytest.mark.run(order=1)
    def test_expression_addsuccess(self, login_to_expression):
        driver = login_to_expression  # WebDriver 实例
        expression = ExpressionPage(driver)  # 用 driver 初始化 ExpressionPage
        sleep(1)
        name = '1测试表达式管理1'
        expression.click_all_button("新增")
        expression.enter_texts('//div[p[text()="名称: "]]//input', name)
        expression.click_button('//div[p[text()="分类: "]]//input[@type="text"]')
        expression.click_button('//li[text()="图棒显示颜色"]')
        expression.enter_texts('//div[p[text()="表达式: "]]//textarea', name)
        expression.click_all_button("保存")
        message = expression.get_find_message()
        expression.select_input_expression(name)
        eles = expression.get_find_element_xpath('//table[@class="vxe-table--body"]//tr[1]/td[2]').text
        assert eles == name
        assert message == "保存成功"
        assert not expression.has_fail_message()

    @allure.story("添加表达式管理重复不允许添加")
    # @pytest.mark.run(order=1)
    def test_expression_addrepeat1(self, login_to_expression):
        driver = login_to_expression  # WebDriver 实例
        expression = ExpressionPage(driver)  # 用 driver 初始化 ExpressionPage
        sleep(1)
        name = '1测试表达式管理1'
        expression.click_all_button("新增")
        expression.enter_texts('//div[p[text()="名称: "]]//input', name)
        expression.click_button('//div[p[text()="分类: "]]//input[@type="text"]')
        expression.click_button('//li[text()="图棒显示颜色"]')
        expression.enter_texts('//div[p[text()="表达式: "]]//textarea', name)
        expression.click_all_button("保存")
        message = expression.get_find_message()
        assert message == "不允许添加重复的表达式名称"
        assert not expression.has_fail_message()

    @allure.story("修改表达式名称成功")
    # @pytest.mark.run(order=1)
    def test_expression_updatesuccess1(self, login_to_expression):
        driver = login_to_expression  # WebDriver 实例
        expression = ExpressionPage(driver)  # 用 driver 初始化 ExpressionPage
        sleep(1)
        before_name = '1测试表达式管理1'
        afert_name = '1测试表达式管理2'
        expression.select_input_expression(before_name)
        expression.click_button('//table[@class="vxe-table--body"]//tr[1]/td[2]')
        expression.click_all_button("编辑")
        expression.enter_texts('//div[p[text()="名称: "]]//input', afert_name)
        expression.click_all_button("保存")
        message = expression.get_find_message()
        expression.select_input_expression(afert_name)
        sleep(1)
        eles = expression.get_find_element_xpath('//table[@class="vxe-table--body"]//tr[1]/td[2]').text
        assert eles == afert_name
        assert message == "保存成功"
        assert not expression.has_fail_message()

    @allure.story("修改分类和表达式成功")
    # @pytest.mark.run(order=1)
    def test_expression_updatesuccess2(self, login_to_expression):
        driver = login_to_expression  # WebDriver 实例
        expression = ExpressionPage(driver)  # 用 driver 初始化 ExpressionPage
        sleep(1)
        name = '1测试表达式管理2'
        text = '1111'
        expression.select_input_expression(name)
        expression.click_button('//table[@class="vxe-table--body"]//tr[1]/td[2]')
        expression.click_all_button("编辑")
        expression.click_button('//div[p[text()="分类: "]]//input[@type="text"]')
        expression.click_button('//li[text()="分派规则"]')
        expression.enter_texts('//div[p[text()="表达式: "]]//textarea', text)
        expression.click_all_button("保存")
        message = expression.get_find_message()
        expression.select_input_expression(name)
        sleep(1)
        eles = expression.get_find_element_xpath('//table[@class="vxe-table--body"]//tr[1]/td[3]').text
        testarea = expression.get_find_element_xpath('//div[p[text()="表达式: "]]//textarea').get_attribute('value')
        assert eles == '反派规则' and testarea == text
        assert message == "保存成功"
        assert not expression.has_fail_message()

    @allure.story("修改表达式管理重复不允许添加")
    # @pytest.mark.run(order=1)
    def test_expression_addrepeat2(self, login_to_expression):
        driver = login_to_expression  # WebDriver 实例
        expression = ExpressionPage(driver)  # 用 driver 初始化 ExpressionPage
        sleep(1)
        before_name = '1测试表达式管理2'
        afert_name = '客户'
        expression.select_input_expression(before_name)
        expression.click_button('//table[@class="vxe-table--body"]//tr[1]/td[2]')
        expression.click_all_button("编辑")
        expression.enter_texts('//div[p[text()="名称: "]]//input', afert_name)
        expression.click_all_button("保存")
        message = expression.get_find_message()
        expression.select_input_expression(afert_name)
        assert message == "不允许添加重复的表达式名称"
        assert not expression.has_fail_message()