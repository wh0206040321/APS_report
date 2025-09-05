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
from Pages.systemPage.role_page import RolePage
from Pages.itemsPage.login_page import LoginPage
from Utils.data_driven import DateDriver
from Utils.driver_manager import create_driver, safe_quit, capture_screenshot


@pytest.fixture  # (scope="class")这个参数表示整个测试类共用同一个浏览器，默认一个用例执行一次
def login_to_role():
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
    list_ = ["系统管理", "系统设置", "角色管理"]
    for v in list_:
        page.click_button(f'(//span[text()="{v}"])[1]')
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("角色管理页用例")
@pytest.mark.run(order=205)
class TestRolePage:

    @allure.story("点击新增不输入数据点击保存，不允许保存")
    # @pytest.mark.run(order=1)
    def test_role_addfail1(self, login_to_role):
        driver = login_to_role  # WebDriver 实例
        role = RolePage(driver)  # 用 driver 初始化 PlanUnitPage
        add = AddsPages(driver)
        list_ = [
            '//div[label[text()="角色代码"]]//input',
            '//div[label[text()="角色名称"]]//input',
            '//div[label[text()="计划单元名称"]]//div[@class="ivu-select-selection"]'
        ]
        sleep(0.5)
        role.click_all_button("新增")
        sleep(0.5)
        role.click_all_button("保存")
        sleep(2)
        value_list = add.get_border_color(list_)
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert all(value == expected_color for value in value_list)
        assert not add.has_fail_message()

    @allure.story("点击只输入角色代码点击保存，不允许保存")
    # @pytest.mark.run(order=1)
    def test_role_addfail2(self, login_to_role):
        driver = login_to_role  # WebDriver 实例
        role = RolePage(driver)  # 用 driver 初始化 PlanUnitPage
        add = AddsPages(driver)
        name = "1测试角色代码1"
        list_ = [
            '//div[label[text()="角色名称"]]//input',
            '//div[label[text()="计划单元名称"]]//div[@class="ivu-select-selection"]'
        ]
        sleep(0.5)
        role.click_all_button("新增")
        role.enter_texts('//div[label[text()="角色代码"]]//input', name)
        role.click_all_button("保存")
        sleep(2)
        value_list = add.get_border_color(list_)
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert all(value == expected_color for value in value_list)
        assert not add.has_fail_message()

    @allure.story("点击输入角色代码和名称点击保存，不允许保存")
    # @pytest.mark.run(order=1)
    def test_role_addfail3(self, login_to_role):
        driver = login_to_role  # WebDriver 实例
        role = RolePage(driver)  # 用 driver 初始化 PlanUnitPage
        add = AddsPages(driver)
        name = "1测试角色代码1"
        list_ = [
            '//div[label[text()="计划单元名称"]]//div[@class="ivu-select-selection"]'
        ]
        sleep(0.5)
        role.click_all_button("新增")
        role.enter_texts('//div[label[text()="角色代码"]]//input', name)
        role.enter_texts('//div[label[text()="角色名称"]]//input', name)
        role.click_all_button("保存")
        sleep(2)
        value_list = add.get_border_color(list_)
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert all(value == expected_color for value in value_list)
        assert not add.has_fail_message()

    @allure.story("添加数据不选择菜单不允许添加")
    # @pytest.mark.run(order=1)
    def test_role_addfail4(self, login_to_role):
        driver = login_to_role  # WebDriver 实例
        role = RolePage(driver)  # 用 driver 初始化 PlanUnitPage
        name = "1测试角色代码1"
        module = "1测试A"
        role.add_role(name, module)
        role.click_all_button("保存")
        ele = role.finds_elements(By.XPATH, f'//div[text()="请选择菜单"]')
        role.click_button('//div[@class="ivu-modal-confirm-footer"]/button')
        assert len(ele) == 1
        assert not role.has_fail_message()

    @allure.story("添加角色成功，勾选所有菜单,并且增加该用户权限，可切换新建单元")
    # @pytest.mark.run(order=1)
    def test_role_success1(self, login_to_role):
        driver = login_to_role  # WebDriver 实例
        role = RolePage(driver)  # 用 driver 初始化 PlanUnitPage
        date_driver = DateDriver()
        name = "1测试角色代码1"
        module = "1测试A"
        role.add_role(name, module)
        num = len(role.finds_elements(By.XPATH, '//div[@class="ivu-tree"]//li/label/span'))
        for i in range(1, num):
            role.click_button(f'(//div[@class="ivu-tree"]//li/label/span)[{i}]')
        role.click_all_button("保存")
        role.right_refresh()
        role.select_input(name)
        ele = role.finds_elements(By.XPATH, f'//table[@class="vxe-table--body"]//tr/td[2]//span[text()="{name}"]')

        role.click_button('(//span[text()="用户权限管理"])[1]')
        role.enter_texts('//div[div[p[text()="用户代码"]]]//input', date_driver.username)
        sleep(1)
        role.click_button(f'(//table[@class="vxe-table--body"]//span[text()="{date_driver.username}"])[1]')
        role.click_all_button("编辑")

        role.select_input(name)
        sleep(2)
        role.click_button('(//table[@class="vxe-table--body"]//tr[1]/td[2]/div/span)[2]')
        role.click_all_button("保存")
        message = role.get_find_message()

        driver.refresh()
        role.click_button(f'//div[contains(text(),"{date_driver.planning}")]')

        role.click_button(f'//ul/li[text()="{module}"]')
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located(
                (By.XPATH, '//div[@class="loadingbox"]')
            )
        )
        num_ = len(role.finds_elements(By.XPATH, f'//div[@class="listDivCon"]/div'))
        swich_name = role.get_find_element_xpath(f'//div[@class="ivu-dropdown-rel"]/div').text
        assert len(ele) == 1 and message == "保存成功" and num_ >= 7 and swich_name == module
        assert not role.has_fail_message()

    @allure.story("添加角色成功，关键字筛选搜索成功，只勾选一个菜单,并且增加该用户权限，可切换新建单元")
    # @pytest.mark.run(order=1)
    def test_role_success2(self, login_to_role):
        driver = login_to_role  # WebDriver 实例
        role = RolePage(driver)  # 用 driver 初始化 PlanUnitPage
        date_driver = DateDriver()
        name = "1测试角色代码2"
        module = "1测试计划单元小日程"
        role.add_role(name, module)

        role.enter_texts('//input[@placeholder="请输入关键字筛选"]', '需求管理')
        role.click_button('//div[@class="ivu-tree"]/ul[1]//label/span')
        te = role.get_find_element_xpath('//div[@class="ivu-tree"]/ul[1]//span[@class="font14"]').text
        role.click_all_button("保存")
        role.right_refresh()
        role.select_input(name)
        ele = role.finds_elements(By.XPATH, f'//table[@class="vxe-table--body"]//tr/td[2]//span[text()="{name}"]')

        role.click_button('(//span[text()="用户权限管理"])[1]')
        role.enter_texts('//div[div[p[text()="用户代码"]]]//input', date_driver.username)
        sleep(1)
        role.click_button(f'(//table[@class="vxe-table--body"]//span[text()="{date_driver.username}"])[1]')
        role.click_all_button("编辑")

        role.select_input(name)
        sleep(2)
        role.click_button('(//table[@class="vxe-table--body"]//tr[1]/td[2]/div/span)[2]')
        role.click_all_button("保存")
        message = role.get_find_message()

        driver.refresh()
        role.click_button(f'//div[contains(text(),"{date_driver.planning}")]')

        role.click_button(f'//ul/li[text()="{module}"]')
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located(
                (By.XPATH, '//div[@class="loadingbox"]')
            )
        )
        num_ = len(role.finds_elements(By.XPATH, f'//div[@class="listDivCon"]/div'))
        swich_name = role.get_find_element_xpath(f'//div[@class="ivu-dropdown-rel"]/div').text
        assert len(ele) == 1 and message == "保存成功" and num_ == 1 and swich_name == module and te == "需求管理"
        assert not role.has_fail_message()

    @allure.story("添加重复名称，不允许添加")
    # @pytest.mark.run(order=1)
    def test_role_addrepeat(self, login_to_role):
        driver = login_to_role  # WebDriver 实例
        role = RolePage(driver)  # 用 driver 初始化 PlanUnitPage
        name = "1测试角色代码2"
        module = "1测试计划单元CTB"
        role.add_role(name, module)

        role.enter_texts('//input[@placeholder="请输入关键字筛选"]', '需求管理')
        role.click_button('//div[@class="ivu-tree"]/ul[1]//label/span')
        role.click_all_button("保存")
        ele = role.finds_elements(By.XPATH, '//div[text()=" 记录已存在,请检查！ "]')
        assert len(ele) == 1
        assert not role.has_fail_message()

    @allure.story("添加测试数据")
    # @pytest.mark.run(order=1)
    def test_role_addtestdata(self, login_to_role):
        driver = login_to_role  # WebDriver 实例
        role = RolePage(driver)  # 用 driver 初始化 PlanUnitPage
        date_driver = DateDriver()
        name = "1测试角色代码3"
        module = "1测试计划单元CTB"
        role.add_role(name, module)
        num = len(role.finds_elements(By.XPATH, '//div[@class="ivu-tree"]//li/label/span'))
        for i in range(1, num):
            role.click_button(f'(//div[@class="ivu-tree"]//li/label/span)[{i}]')
        role.click_all_button("保存")
        role.right_refresh()
        role.select_input(name)
        ele = role.finds_elements(By.XPATH, f'//table[@class="vxe-table--body"]//tr/td[2]//span[text()="{name}"]')

        role.click_button('(//span[text()="用户权限管理"])[1]')
        role.enter_texts('//div[div[p[text()="用户代码"]]]//input', date_driver.username)
        sleep(1)
        role.click_button(f'(//table[@class="vxe-table--body"]//span[text()="{date_driver.username}"])[1]')
        role.click_all_button("编辑")

        role.select_input(name)
        sleep(2)
        role.click_button('(//table[@class="vxe-table--body"]//tr[1]/td[2]/div/span)[2]')
        role.click_all_button("保存")
        message = role.get_find_message()

        driver.refresh()
        role.click_button(f'//div[contains(text(),"{date_driver.planning}")]')

        role.click_button(f'//ul/li[text()="{module}"]')
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located(
                (By.XPATH, '//div[@class="loadingbox"]')
            )
        )
        num_ = len(role.finds_elements(By.XPATH, f'//div[@class="listDivCon"]/div'))
        swich_name = role.get_find_element_xpath(f'//div[@class="ivu-dropdown-rel"]/div').text
        assert len(ele) == 1 and message == "保存成功" and num_ >= 7 and swich_name == module
        assert not role.has_fail_message()

    @allure.story("修改和角色名称成功，并且可切换计划单元")
    # @pytest.mark.run(order=1)
    def test_role_updatedata1(self, login_to_role):
        driver = login_to_role  # WebDriver 实例
        role = RolePage(driver)  # 用 driver 初始化 PlanUnitPage
        date_driver = DateDriver()
        before_name = "1测试角色代码3"
        after_name = "修改角色名称"
        module = "1测试计划单元标准"
        role.update_role(before_name, after_name, module)
        role.click_all_button("保存")
        message = role.get_find_message()
        role.select_input(before_name)
        ele = role.finds_elements(By.XPATH, f'//table[@class="vxe-table--body"]//tr/td[3]//span[text()="{after_name}"]')

        driver.refresh()
        role.click_button(f'//div[contains(text(),"{date_driver.planning}")]')

        role.click_button(f'//ul/li[text()="{module}"]')
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located(
                (By.XPATH, '//div[@class="loadingbox"]')
            )
        )
        num_ = len(role.finds_elements(By.XPATH, f'//div[@class="listDivCon"]/div'))
        swich_name = role.get_find_element_xpath(f'//div[@class="ivu-dropdown-rel"]/div').text
        assert len(ele) == 1 and message == "保存成功" and num_ >= 7 and swich_name == module
        assert not role.has_fail_message()

    @allure.story("修改菜单成功，并且可切换计划单元")
    # @pytest.mark.run(order=1)
    def test_role_updatedata2(self, login_to_role):
        driver = login_to_role  # WebDriver 实例
        role = RolePage(driver)  # 用 driver 初始化 PlanUnitPage
        date_driver = DateDriver()
        before_name = "1测试角色代码3"
        after_name = "修改角色名称"
        module = "1测试计划单元标准"
        role.select_input(before_name)
        sleep(1)
        role.click_button(f'//table[@class="vxe-table--body"]//tr/td[2]//span[text()="{before_name}"]')
        role.click_all_button("编辑")
        role.click_all_button("保存")
        message = role.get_find_message()
        role.select_input(before_name)
        ele = role.finds_elements(By.XPATH, f'//table[@class="vxe-table--body"]//tr/td[3]//span[text()="{after_name}"]')
        num = len(role.finds_elements(By.XPATH, '//div[@class="ivu-tree"]//li/label/span'))
        for i in range(1, num):
            role.click_button(f'(//div[@class="ivu-tree"]//li/label/span)[{i}]')

        role.enter_texts('//input[@placeholder="请输入关键字筛选"]', '需求管理')
        role.click_button('//div[@class="ivu-tree"]/ul[1]//label/span')
        te = role.get_find_element_xpath('//div[@class="ivu-tree"]/ul[1]//span[@class="font14"]').text
        role.click_all_button("保存")
        message = role.get_find_message()
        driver.refresh()
        role.click_button(f'//div[contains(text(),"{date_driver.planning}")]')

        role.click_button(f'//ul/li[text()="{module}"]')
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located(
                (By.XPATH, '//div[@class="loadingbox"]')
            )
        )
        num_ = len(role.finds_elements(By.XPATH, f'//div[@class="listDivCon"]/div'))
        swich_name = role.get_find_element_xpath(f'//div[@class="ivu-dropdown-rel"]/div').text
        assert len(ele) == 1 and message == "保存成功" and num_ == 1 and swich_name == module and te == "需求管理"
        assert not role.has_fail_message()