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
from Pages.systemPage.synchronize_page import SynchronizePage
from Pages.itemsPage.login_page import LoginPage
from Utils.data_driven import DateDriver
from Utils.driver_manager import create_driver, safe_quit, capture_screenshot


@pytest.fixture  # (scope="class")这个参数表示整个测试类共用同一个浏览器，默认一个用例执行一次
def login_to_synchronize():
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
    page.click_button('(//span[text()="系统管理"])[1]')  # 点击系统管理
    page.click_button('(//span[text()="单元设置"])[1]')  # 点击单元设置
    page.click_button('(//span[text()="配置同步"])[1]')  # 点击配置同步
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("配置同步页用例")
@pytest.mark.run(order=204)
class TestSynchronizePage:

    @allure.story("不勾选单元点击同步弹出错误提示")
    # @pytest.mark.run(order=1)
    def test_synchronize_all_numsel(self, login_to_synchronize):
        driver = login_to_synchronize  # WebDriver 实例
        synchronize = SynchronizePage(driver)  # 用 driver 初始化 SynchronizePage
        synchronize.click_synchronize_button()
        message = synchronize.get_find_message()
        assert message == "请勾选当前和目的计划单元"
        assert not synchronize.has_fail_message()

    @allure.story("同步单个psi成功")
    # @pytest.mark.run(order=1)
    def test_synchronize_all_psi(self, login_to_synchronize):
        driver = login_to_synchronize  # WebDriver 实例
        synchronize = SynchronizePage(driver)  # 用 driver 初始化 SynchronizePage
        name1 = [
            "1测试psi1",
        ]
        name2 = [
            "AA",
        ]
        synchronize.click_checkbox_value(name1, name2, "1")
        synchronize.click_synchronize_button()
        synchronize.click_synchronize_pop(True)
        message = synchronize.get_find_message()
        synchronize.switch_plane(name2[0], 1)
        plan_value = synchronize.finds_elements(By.XPATH,
                                                f'//table[@class="vxe-table--body"]//tr/td[2]//span[text()="{name1[0]}"]')
        assert message == "同步成功"
        assert len(plan_value) == 1
        assert not synchronize.has_fail_message()

    @allure.story("重复同步同一个psi不会报错，会继续同步")
    # @pytest.mark.run(order=1)
    def test_synchronize_all_repeatpsi(self, login_to_synchronize):
        driver = login_to_synchronize  # WebDriver 实例
        synchronize = SynchronizePage(driver)  # 用 driver 初始化 SynchronizePage
        name1 = [
            "1测试psi1",
        ]
        name2 = [
            "AA",
        ]
        synchronize.click_checkbox_value(name1, name2, "1")
        synchronize.click_synchronize_button()
        synchronize.click_synchronize_pop(True)
        message = synchronize.get_find_message()
        synchronize.switch_plane(name2[0], 1)
        plan_value = synchronize.finds_elements(By.XPATH,
                                                f'//table[@class="vxe-table--body"]//tr/td[2]//span[text()="{name1[0]}"]')
        assert message == "同步成功"
        assert len(plan_value) == 1
        assert not synchronize.has_fail_message()

    @allure.story("同步多个psi到一个计划单元成功")
    # @pytest.mark.run(order=1)
    def test_synchronize_all_psis(self, login_to_synchronize):
        driver = login_to_synchronize  # WebDriver 实例
        synchronize = SynchronizePage(driver)  # 用 driver 初始化 SynchronizePage
        name1 = [
            "1测试psi1",
            "1测试psi2",
        ]
        name2 = [
            "AA",
        ]
        synchronize.click_checkbox_value(name1, name2, "1")
        synchronize.click_synchronize_button()
        synchronize.click_synchronize_pop(True)
        message = synchronize.get_find_message()
        synchronize.switch_plane(name2[0], 1)
        plan_value1 = synchronize.finds_elements(By.XPATH,
                                                f'//table[@class="vxe-table--body"]//tr/td[2]//span[text()="{name1[0]}"]')
        plan_value2 = synchronize.finds_elements(By.XPATH,
                                                f'//table[@class="vxe-table--body"]//tr/td[2]//span[text()="{name1[1]}"]')
        assert message == "同步成功"
        assert len(plan_value1) == 1 and len(plan_value2) == 1
        assert not synchronize.has_fail_message()

    # @allure.story("同步多个psi到一个计划单元成功")
    # # @pytest.mark.run(order=1)
    # def test_synchronize_all_psis(self, login_to_synchronize):
    #     driver = login_to_synchronize  # WebDriver 实例
    #     synchronize = SynchronizePage(driver)  # 用 driver 初始化 SynchronizePage
    #     name1 = [
    #         "1测试psi1",
    #         "1测试psi2",
    #     ]
    #     name2 = [
    #         "AA",
    #     ]
    #     synchronize.click_checkbox_value(name1, name2, "1")
    #     synchronize.click_synchronize_button()
    #     synchronize.click_synchronize_pop(True)
    #     message = synchronize.get_find_message()
    #     synchronize.switch_plane(name2[0], 1)
    #     plan_value1 = synchronize.finds_elements(By.XPATH,
    #                                              f'//table[@class="vxe-table--body"]//tr/td[2]//span[text()="{name1[0]}"]')
    #     plan_value2 = synchronize.finds_elements(By.XPATH,
    #                                              f'//table[@class="vxe-table--body"]//tr/td[2]//span[text()="{name1[1]}"]')
    #     assert message == "同步成功"
    #     assert len(plan_value1) == 1 and len(plan_value2) == 1
    #     assert not synchronize.has_fail_message()