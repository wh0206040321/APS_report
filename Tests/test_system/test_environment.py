from time import sleep

import allure
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.itemsPage.adds_page import AddsPaes
from Pages.itemsPage.personal_page import PersonalPage
from Pages.systemPage.environment_page import EnvironmentPage
from Pages.itemsPage.login_page import LoginPage
from Utils.data_driven import DateDriver
from Utils.driver_manager import create_driver, safe_quit


@pytest.fixture  # (scope="class")这个参数表示整个测试类共用同一个浏览器，默认一个用例执行一次
def login_to_environment():
    """初始化并返回 driver"""
    driver_path = DateDriver().driver_path
    driver = create_driver(driver_path)
    driver.implicitly_wait(3)

    # 初始化登录页面
    page = LoginPage(driver)  # 初始化登录页面
    page.navigate_to(DateDriver().url)  # 导航到登录页面
    page.login(DateDriver().username, DateDriver().password, DateDriver().planning)
    page.click_button('(//span[text()="系统管理"])[1]')  # 点击系统管理
    page.click_button('(//span[text()="单元设置"])[1]')  # 点击单元设置
    page.click_button('(//span[text()="环境设置"])[1]')  # 点击环境设置
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("环境设置页用例")
@pytest.mark.run(order=201)
class TestEnvironmentPage:

    @allure.story("全体页面-数字框只运行输入数字")
    # @pytest.mark.run(order=1)
    def test_environment_numsel(self, login_to_environment):
        driver = login_to_environment  # WebDriver 实例
        environment = EnvironmentPage(driver)  # 用 driver 初始化 EnvironmentPage
        value = environment.enter_number_input("11111111111111111111")
        assert value == "100000"
        assert not environment.has_fail_message()

    @allure.story("全体页面-不输入备份文件不允许保存")
    # @pytest.mark.run(order=1)
    def test_environment_clearnum(self, login_to_environment):
        driver = login_to_environment  # WebDriver 实例
        environment = EnvironmentPage(driver)  # 用 driver 初始化 EnvironmentPage
        value = environment.enter_number_input()
        environment.click_save_button()
        message = environment.get_find_message()
        assert value == "" and message == "请填写信息"
        assert not environment.has_fail_message()

    @allure.story("全体页面-输入备份文件只允许输入数字，点击保存，保存成功")
    # @pytest.mark.run(order=1)
    def test_environment_numsuccess(self, login_to_environment):
        driver = login_to_environment  # WebDriver 实例
        environment = EnvironmentPage(driver)  # 用 driver 初始化 EnvironmentPage
        before_value = environment.enter_number_input("QAseE1@!><?+_+=-3.3")
        environment.click_save_button()
        message = environment.get_find_message()
        driver.refresh()
        sleep(1)
        after_value = environment.get_find_element_xpath('//div[label[text()="备份文件最大数:"]]//input').get_attribute("value")
        assert before_value == after_value == "133" and message == "保存成功"
        assert not environment.has_fail_message()