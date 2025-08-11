import logging
import random
from time import sleep

import allure
import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.login_page import LoginPage
from Pages.materialPage.qtProgrammeMan_page import SchedPage
from Utils.data_driven import DateDriver
from Utils.driver_manager import create_driver, safe_quit, all_driver_instances


@pytest.fixture(scope="module")
def login_to_sched():
    """初始化并返回 driver"""
    driver_path = DateDriver().driver_path
    driver = create_driver(driver_path)
    driver.implicitly_wait(3)

    # 初始化登录页面
    page = LoginPage(driver)  # 初始化登录页面
    page.navigate_to(DateDriver().url)  # 导航到登录页面
    page.login(DateDriver().username, DateDriver().password, DateDriver().planning)
    page.click_button('(//span[text()="计划运行"])[1]')  # 点击计划运行
    page.click_button('(//span[text()="方案管理"])[1]')  # 点击方案管理
    page.click_button('(//span[text()="物控方案管理"])[1]')  # 点击计划方案管理
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("物控方案管理表测试用例")
@pytest.mark.run(order=111)
class TestSchedPage:
    @allure.story("添加方案管理信息 不填写数据点击确认 不允许提交")
    # @pytest.mark.run(order=1)
    def test_sched_addfail1(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        sched.click_add_schedbutton()  # 点击添加方案

        sched.click_ok_schedbutton()  # 点击确定
        message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="ivu-message"]//span')
            )
        )
        # 检查元素是否包含子节点
        assert message.text == "请输入"
        assert not sched.has_fail_message()

    @allure.story("添加方案管理信息 只填写复制方案 不允许提交")
    # @pytest.mark.run(order=1)
    def test_sched_addfail2(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage

        sched.click_add_schedbutton()  # 点击添加方案
        sched.click_button(
            '//label[text()="选择复制的方案"]/following-sibling::div/div'
        )  # 点击下拉框
        sched.click_button('//li[text()="测试方案"]')

        sched.click_ok_schedbutton()  # 点击确定
        message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="ivu-message"]//span')
            )
        )
        # 检查元素是否包含子节点
        assert message.text == "请输入"
        assert not sched.has_fail_message()

    @allure.story("添加方案管理信息 添加重复 不允许提交")
    # @pytest.mark.run(order=1)
    def test_sched_addrepeat(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage

        sched.click_add_schedbutton()  # 点击添加方案
        sched.enter_texts(
            '//label[text()="名称"]/following-sibling::div//input', "测试方案"
        )

        sched.click_ok_schedbutton()  # 点击确定
        message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="ivu-message"]//span')
            )
        )
        # 检查元素是否包含子节点
        assert message.text == "物控方案已存在"
        assert not sched.has_fail_message()

    @allure.story("添加复制方案成功")
    # @pytest.mark.run(order=1)
    def test_sched_addrepeatsuccess(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage

        sched.click_add_schedbutton()  # 点击添加方案
        name = "22"
        sched.enter_texts(
            '//label[text()="名称"]/following-sibling::div//input', f"{name}"
        )

        sched.click_button(
            '//label[text()="选择复制的方案"]/following-sibling::div/div'
        )  # 点击下拉框
        sched.click_button('//li[text()="测试方案"]')
        sched.click_ok_schedbutton()  # 点击确定
        sched.click_save_button()  # 点击保存
        sleep(1)

        element = driver.find_element(
            By.XPATH, f'//span[text()="{name}"]/parent::span/preceding-sibling::span'
        )
        driver.execute_script("arguments[0].scrollIntoView();", element)

        # 判断下拉框为打开还是关闭
        sleep(1)
        sel = sched.get_find_element_xpath(
            f'//span[text()="{name}"]/parent::span/preceding-sibling::span'
        )
        if "ivu-tree-arrow" in sel.get_attribute("class"):
            sched.click_button(f'//span[text()="{name}"]/parent::span/preceding-sibling::span')

        addtext = sched.get_find_element_xpath(
            '(//div[@class="ivu-radio-group ivu-radio-group-small ivu-radio-small ivu-radio-group-button"])[2]/label[last()]'
        )
        addtext1 = sched.get_find_element_xpath(
            '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/span[2]'
        )
        addul = driver.find_elements(
            By.XPATH,
            '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/ul',
        )
        assert addtext.text == name and addtext1.text == name and len(addul) > 0
        assert not sched.has_fail_message()

    @allure.story("删除刚才添加的方案")
    # @pytest.mark.run(order=1)
    def test_sched_delsched1(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        # 选中为22的方案
        sched.click_button(
            '(//div[@class="ivu-radio-group ivu-radio-group-small ivu-radio-small ivu-radio-group-button"])[2]/label[text()="22"]'
        )
        sched.click_del_schedbutton()  # 点击删除
        sched.click_button('(//button[@class="ivu-btn ivu-btn-primary"])[2]')

        # 点击保存
        sched.click_save_button()
        ele = driver.find_elements(
            By.XPATH,
            '(//div[@class="ivu-radio-group ivu-radio-group-small ivu-radio-small ivu-radio-group-button"])[2]/label[text()="22"]',
        )
        assert len(ele) == 0
        assert not sched.has_fail_message()

    @allure.story("添加方案成功")
    # @pytest.mark.run(order=1)
    def test_sched_addsuccess(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage

        sched.click_add_schedbutton()  # 点击添加方案
        sched.enter_texts('//label[text()="名称"]/following-sibling::div//input', "33")
        sched.click_ok_schedbutton()  # 点击确定
        sched.click_save_button()  # 点击保存
        sleep(1)
        addtext = sched.get_find_element_xpath(
            '(//div[@class="ivu-radio-group ivu-radio-group-small ivu-radio-small ivu-radio-group-button"])[2]/label[last()]'
        )
        addtext1 = sched.get_find_element_xpath(
            '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/span[2]'
        )
        addul = driver.find_elements(
            By.XPATH,
            '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/ul',
        )
        assert addtext.text == "33" and addtext1.text == "33" and len(addul) == 0
        assert not sched.has_fail_message()

    @allure.story("没有选中行 添加命令 添加失败")
    # @pytest.mark.run(order=1)
    def test_sched_addcommandfail(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage

        # 选中命令点击添加
        sched.click_button(
            '(//div[@class="ivu-radio-group ivu-radio-group-small ivu-radio-small ivu-radio-group-button"])[1]/label[1]'
        )
        sched.click_add_commandbutton()
        message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="ivu-message"]//span')
            )
        )
        # 检查元素是否包含子节点
        sleep(1)
        assert message.text == "请选择操作的行"
        assert not sched.has_fail_message()

    @allure.story("添加命令成功")
    # @pytest.mark.run(order=1)
    def test_sched_addcommandsuccess(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage

        # 选中命令点击添加
        addul1 = driver.find_elements(
            By.XPATH,
            '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/ul',
        )
        # 第一个命令 xpth
        command = '(//div[@class="ivu-radio-group ivu-radio-group-small ivu-radio-small ivu-radio-group-button"])[1]/label[1]'
        sched.click_button(command)
        command_text = sched.get_find_element_xpath(command)

        element = driver.find_element(
            By.XPATH, '//span[text()="33"]/parent::span/preceding-sibling::span'
        )
        driver.execute_script("arguments[0].scrollIntoView();", element)

        # 选中33方案
        sched.click_button(
            '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/span[2]'
        )
        driver.execute_script("window.scrollTo(0, 0);")
        sched.click_add_commandbutton()
        sched.click_save_button()
        addul2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/ul[1]',
                )
            )
        )
        # 判断添加前列表为空 ，添加后命令相同
        sleep(1)
        assert len(addul1) == 0 and addul2.text == command_text.text
        assert not sched.has_fail_message()

    @allure.story("删除命令成功")
    # @pytest.mark.run(order=1)
    def test_sched_delcommandsuccess(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage

        while True:
            sleep(1)
            addul1 = driver.find_elements(
                By.XPATH,
                '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/ul[1]//span[2]',
            )
            if not addul1:
                break  # 没有找到元素时退出循环
                # 存在元素，点击删除按钮
            element = driver.find_element(
                By.XPATH, '//span[text()="33"]/parent::span/preceding-sibling::span'
            )
            driver.execute_script("arguments[0].scrollIntoView();", element)
            addul1[0].click()
            driver.execute_script("window.scrollTo(0, 0);")
            sched.click_del_commandbutton()
            sched.click_ok_schedbutton()

        # 再次确认，元素已删除
        sched.click_save_button()
        addul1_after = driver.find_elements(
            By.XPATH,
            '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/ul',
        )
        sleep(1)
        assert len(addul1_after) == 0
        assert not sched.has_fail_message()

    @allure.story("添加2个命令成功")
    # @pytest.mark.run(order=1)
    def test_sched_addcommandsuccess2(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage

        # 选中命令点击添加
        addul1 = driver.find_elements(
            By.XPATH,
            '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/ul',
        )
        # 第一个命令 xpth
        command = '(//div[@class="ivu-radio-group ivu-radio-group-small ivu-radio-small ivu-radio-group-button"])[1]/label'
        command_text = driver.find_elements(By.XPATH, command)
        command_text[0].click()

        element = driver.find_element(
            By.XPATH, '//span[text()="33"]/parent::span/preceding-sibling::span'
        )
        driver.execute_script("arguments[0].scrollIntoView();", element)

        # 选中33方案
        sched.click_button(
            '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/span[2]'
        )
        driver.execute_script("window.scrollTo(0, 0);")
        sched.click_add_commandbutton()

        # 添加第二个命令
        command_text[1].click()
        sched.click_add_commandbutton()

        sched.click_save_button()
        addul2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                # 查找第一个命令
                (
                    By.XPATH,
                    '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/ul[1]',
                )
            )
        )
        addul3 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                # 查找第二个命令
                (
                    By.XPATH,
                    '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/ul[2]',
                )
            )
        )
        sleep(1)
        # 判断刚开始的命令为0，并且添加的两个命令名称都相等
        assert (
            len(addul1) == 0
            and addul2.text == command_text[0].text
            and addul3.text == command_text[1].text
        )
        assert not sched.has_fail_message()

    @allure.story("向上移动命令")
    # @pytest.mark.run(order=1)
    def test_sched_upcommand(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage

        sleep(3)
        command = sched.get_find_element_xpath(
            '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/ul[2]//span[2]'
        ).text

        element = driver.find_element(
            By.XPATH, '//span[text()="33"]/parent::span/preceding-sibling::span'
        )
        driver.execute_script("arguments[0].scrollIntoView();", element)

        # 选中第二个命令
        sched.click_button(
            '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/ul[2]//span[2]'
        )
        driver.execute_script("window.scrollTo(0, 0);")
        sched.click_up_commandbutton()
        sched.click_save_button()
        sleep(1)
        after_command = sched.get_find_element_xpath(
            '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/ul[1]//span[2]'
        ).text
        assert command == after_command
        assert not sched.has_fail_message()

    @allure.story("向下移动命令")
    # @pytest.mark.run(order=1)
    def test_sched_downcommand(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        sleep(3)
        command = sched.get_find_element_xpath(
            '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/ul[1]//span[2]'
        ).text
        # 选中第一个命令
        sched.click_button(
            '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/ul[1]//span[2]'
        )
        driver.execute_script("window.scrollTo(0, 0);")
        sched.click_down_commandbutton()
        sched.click_save_button()
        sleep(2)
        after_command = sched.get_find_element_xpath(
            '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/ul[2]//span[2]'
        ).text
        assert command == after_command
        assert not sched.has_fail_message()

    @allure.story("删除刚才添加的方案")
    # @pytest.mark.run(order=1)
    def test_sched_delsched2(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        # 选中为33的方案
        sched.click_button(
            '(//div[@class="ivu-radio-group ivu-radio-group-small ivu-radio-small ivu-radio-group-button"])[2]/label[text()="33"]'
        )
        sched.click_del_schedbutton()  # 点击删除
        sched.click_button('(//button[@class="ivu-btn ivu-btn-primary"])[2]')

        # 点击保存
        sched.click_save_button()
        ele = driver.find_elements(
            By.XPATH,
            '(//div[@class="ivu-radio-group ivu-radio-group-small ivu-radio-small ivu-radio-group-button"])[2]/label[text()="22"]',
        )
        assert len(ele) == 0
        assert not sched.has_fail_message()

    @allure.story("添加复制测试方案成功")
    # @pytest.mark.run(order=1)
    def test_sched_addrepeatsuccess1(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage

        sched.click_add_schedbutton()  # 点击添加方案
        name = "标准方案复制"
        sched.enter_texts(
            '//label[text()="名称"]/following-sibling::div//input', f"{name}"
        )

        sched.click_button(
            '//label[text()="选择复制的方案"]/following-sibling::div/div'
        )  # 点击下拉框
        sched.click_button('//li[text()="标准方案"]')
        sched.click_ok_schedbutton()  # 点击确定
        sched.click_save_button()  # 点击保存
        sleep(1)

        element = driver.find_element(
            By.XPATH, f'//span[text()="{name}"]/parent::span/preceding-sibling::span'
        )
        driver.execute_script("arguments[0].scrollIntoView();", element)

        # 判断下拉框为打开还是关闭
        sleep(1)
        sel = sched.get_find_element_xpath(
            f'//span[text()="{name}"]/parent::span/preceding-sibling::span'
        )
        if "ivu-tree-arrow" in sel.get_attribute("class"):
            sched.click_button(f'//span[text()="{name}"]/parent::span/preceding-sibling::span')

        addtext = sched.get_find_element_xpath(
            '(//div[@class="ivu-radio-group ivu-radio-group-small ivu-radio-small ivu-radio-group-button"])[2]/label[last()]'
        )
        addtext1 = sched.get_find_element_xpath(
            '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/span[2]'
        )
        addul = driver.find_elements(
            By.XPATH,
            '//ul[@class="ivu-tree-children" and @visible="visible"]/li/ul[last()]/li/ul',
        )
        assert addtext.text == name and addtext1.text == name and len(addul) > 0
        assert not sched.has_fail_message()

    @allure.story("属性设置-未选择必填项，不允许提交")
    # @pytest.mark.run(order=1)
    def test_sched_attribute1(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "标准方案复制"
        # 选择标准方案复制
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()

        sched.click_button('(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]//span[text()="确定"]')
        # # 点击下拉框
        # sched.click_button('//div[text()="按分派规则顺序排列"]/following-sibling::div')
        # sched.click_button(
        #     '//div[text()="按分派规则顺序排列"]/following-sibling::div//ul[2]/li[2]'
        # )
        # sleep(1)
        # befort_input = sched.get_find_element_xpath(
        #     '//div[text()="按分派规则顺序排列"]/following-sibling::div//input/following-sibling::div/input'
        # ).get_attribute("value")
        # sched.get_after_value(name)
        # after_input = sched.get_find_element_xpath(
        #     '//div[text()="按分派规则顺序排列"]/following-sibling::div//input/following-sibling::div/input'
        # ).get_attribute("value")

        message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="ivu-message-custom-content ivu-message-error"]//span')
            )
        )
        # 检查元素是否包含子节点
        sleep(1)
        assert message.text == "请选择公共数据计划单元"
        assert not sched.has_fail_message()

    @allure.story("属性设置-必填项保存成功")
    # @pytest.mark.run(order=1)
    def test_sched_attribute2(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "标准方案复制"
        # 选择标准方案复制
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击公共数据计划单元下拉框
        sched.click_button('//div[@class="d-flex set-teble-style noBorder h-40px"][1]/div[2]')
        # 点击公共数据计划单元下拉框的第一个选项
        sched.click_button('//div[@class="d-flex set-teble-style noBorder h-40px"][1]//li[@class="ivu-select-item"][1]')

        # 点击需求源选择及数据过滤
        sched.click_button('//div[@class="d-flex set-teble-style noBorder h-40px"][3]/div[2]')
        # 等待弹窗打开，选择第一项数据
        sleep(1)
        sched.click_button('//div[@class="vxe-cell c--tooltip"]/span[@class="vxe-cell--checkbox"]')
        sched.click_button('(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]//span[text()="确定"]')

        # 点击供应源选择及数据过滤
        sched.click_button('//div[@class="d-flex set-teble-style noBorder h-40px"][4]/div[2]')
        # 等待弹窗打开，选择第一项数据
        sleep(1)
        sched.click_button('//div[@class="vxe-cell c--tooltip"]/span[@class="vxe-cell--checkbox"]')
        sched.click_button('(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]//span[text()="确定"]')

        # 点击tab切换齐套指标输出 //div[text()=" 齐套指标输出 "]
        sched.click_button('//div[text()=" 齐套指标输出 "]')
        sleep(1)
        sched.click_button('//div[text()="用户自定义指标项输出 "]/following-sibling::div')
        sched.click_button('//span[text()=" 1.常规齐套率 "]')
        sched.click_button('(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[3]//span[text()="确定"]')

        # 确定提交
        sched.click_button('(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]//span[text()="确定"]')
        # 保存刷新后打开属性设置弹窗
        sched.get_after_value(name)
        # 获取属性设置弹窗齐套供需设置tab的value
        xpath_list = [
            '//div[text()="公共数据计划单元 "]/following-sibling::div//input[@class="ivu-select-input"]',
            '//div[text()="物料需求计算公式 "]/following-sibling::div//input[@class="ivu-select-input"]'
        ]
        val_list = [
            "A10",
            "父项数量*用量(不考虑损耗)"
        ]
        tabs1 = sched.batch_acquisition_input(xpath_list, val_list)
        # 需求源选择及数据过滤文本
        tabs1_text1 = sched.get_find_element_xpath('//div[text()="需求源选择及数据过滤 "]/following-sibling::div//p').text
        # 供应源选择及数据过滤文本
        tabs1_text2 = sched.get_find_element_xpath('//div[text()="供应源选择及数据过滤 "]/following-sibling::div//p').text
        print("tabs1", tabs1)
        print("tabs1_text1", tabs1_text1)
        print("tabs1_text2", tabs1_text2)
        assert len(val_list) == len(tabs1) and tabs1_text1 == "(集合)" and tabs1_text2 == "(集合)"
        assert not sched.has_fail_message()

    @allure.story("属性设置-齐套供需设置保存全部成功")
    # @pytest.mark.run(order=1)
    def test_sched_attribute3(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "标准方案复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        sleep(2)
        # 批量修改表达式
        expression_list = [
            '//div[text()="预占料供应数据筛选 "]/following-sibling::div',
            '//div[text()="标准需求表数据筛选 "]/following-sibling::div',
            '//div[text()="标准供应表数据筛选 "]/following-sibling::div',
            '//div[text()="标准供应表排序条件式 "]/following-sibling::div',
            '//div[text()="供需分配有效条件式 "]/following-sibling::div'
        ]
        sched.expression_click(expression_list)
        sleep(1)
        # 点击标准需求表数据排序
        sched.click_button('//div[text()="标准需求表数据排序 "]/following-sibling::div')
        # 点击+号
        sched.click_button('(//div[@class="flex-j-c-between editButtonPadding"])//button[@class="m-r-5 ivu-btn ivu-btn-primary ivu-btn-small ivu-btn-icon-only"][1]')
        # 点击排序键名称下拉
        sched.click_button('(//div[@class="vxe-select size--mini is--filter"])[1]')
        # 选择第一项 BOM版本
        sched.click_button('(//div[@class="vxe-select-option--wrapper"])[1]//div[1]')
        sleep(1)
        # 点击排序方式下拉
        sched.click_button('(//div[@class="vxe-select size--mini is--filter"])[1]')
        # # 选择第一项 升序
        sleep(1)
        sched.click_button('(//div[@class="vxe-select-option--wrapper"])[2]//div[1]')
        sched.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[3]//span[text()="确定"]')

        # 点击标准供应表排序分组
        sleep(1)
        sched.click_button('//div[text()="标准供应表排序分组 "]/following-sibling::div')
        # 点击+号
        sched.click_button('(//button[@class="SchemeButton ivu-btn ivu-btn-primary ivu-btn-icon-only"])[1]')
        # 输入分组名称
        sched.enter_texts('(//div[@class="inputSlot ivu-input-wrapper ivu-input-wrapper-small ivu-input-type-text"])/input', "测试1")
        # 点击排序规则弹窗
        sleep(1)
        sched.click_button('(//div[@class="inputSlot ivu-input-wrapper ivu-input-wrapper-small ivu-input-type-text"])/ancestor::td/following-sibling::td')
        # 点击+号
        sched.click_button('(//div[@class="flex-j-c-between editButtonPadding"])//button[@class="m-r-5 ivu-btn ivu-btn-primary ivu-btn-small ivu-btn-icon-only"][1]')
        sleep(2)
        # 点击排序键名称下拉
        sched.click_button('(//div[@class="vxe-select size--mini is--filter"])[1]')
        # 选择第二项 仓库编码
        sched.click_button('(//div[@class="vxe-select-option--wrapper"])//div[2]')
        # 点击排序键名称下拉
        sched.click_button('(//div[@class="vxe-select size--mini is--filter"])[1]')
        # 选择第二项
        sched.click_button('(//div[@class="vxe-select-option--wrapper"])[1]//div[2]')
        sleep(2)
        # 点击排序方式下拉
        sched.click_button('(//div[@class="vxe-select size--mini is--filter"])[1]')
        # # 选择第一项 升序
        sched.click_button('(//div[@class="vxe-select-option--wrapper"])[2]//div[1]')
        sched.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[3]//span[text()="确定"]')
        sleep(1)
        # input()
        sched.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[4]//span[text()="确定"]')

        # 设置供需计算是否开启多线程计算
        sleep(1)
        sched.click_button('//div[text()="供需计算是否开启多线程计算 "]/following-sibling::div')
        sched.click_button('//li[text()="是"]')
        # 供需计算开启线程的最大数目设置2
        sleep(1)
        sched.enter_texts('//div[@class="w-b-100 ivu-input-number ivu-input-number-small"]//input', 2)
        sleep(1)
        sched.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]//span[text()="确定"]')
        # 保存刷新后打开属性设置弹窗
        sched.get_after_value(name)

        sleep(1)
        text_xpath_list = [
            '//div[text()="预占料供应数据筛选 "]/following-sibling::div//p',
            '//div[text()="标准需求表数据筛选 "]/following-sibling::div//p',
            '//div[text()="标准需求表数据排序 "]/following-sibling::div//p',
            '//div[text()="标准供应表数据筛选 "]/following-sibling::div//p',
            '//div[text()="标准供应表排序分组 "]/following-sibling::div//p',
            '//div[text()="标准供应表排序条件式 "]/following-sibling::div//p',
            '//div[text()="供需分配有效条件式 "]/following-sibling::div//p',
        ]
        value_list = [
            'Abs(-100.28)',
            'Abs(-100.28)',
            'BOM版本 asc',
            'Abs(-100.28)',
            '测试1',
            'Abs(-100.28)',
            'Abs(-100.28)',
        ]
        res_data = sched.batch_acquisition_text(text_xpath_list, value_list)
        print('rrr', res_data)
        input_xpath_list = [
            '//div[text()="供需计算是否开启多线程计算 "]/following-sibling::div//input[@class="ivu-select-input"]',
            '//div[text()="供需计算开启线程的最大数目 "]/following-sibling::div//input[@class="ivu-input-number-input"]'
        ]
        input_value_list = [
            '是',
            '2'
        ]
        input_res = sched.batch_acquisition_input(input_xpath_list, input_value_list)
        print('input_res', input_res)
        assert len(text_xpath_list) == len(text_xpath_list) and len(input_xpath_list) == len(input_res)
        assert not sched.has_fail_message()

    @allure.story("属性设置-齐套计算规则保存全部成功")
    # @pytest.mark.run(order=1)
    def test_sched_attribute4(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "标准方案复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()

        # 点击tab切换齐套计算规则
        sleep(1)
        sched.click_button('//div[text()=" 齐套计算规则 "]')
        select_xpath_list = [
            '//div[contains(text(),"方案是否循环执行 ")]/following-sibling::div',
            '//div[contains(text(),"物料齐套方式 ")]/following-sibling::div',
            '//div[contains(text(),"是否释放不齐套料 ")]/following-sibling::div',
            '//div[contains(text(),"齐套回答基准项 ")]/following-sibling::div',
            '//div[contains(text(),"是否启用最小齐套量 ")]/following-sibling::div',
            '//div[contains(text(),"是否考虑物料替代 ")]/following-sibling::div',
            # '//div[contains(text(),"是否考虑最小替代量 ")]/following-sibling::div',
            '//div[contains(text(),"物料欠料计算方式 ")]/following-sibling::div',
            '//div[contains(text(),"是否按替代比例拆分订单 ")]/following-sibling::div',
            '//div[contains(text(),"齐套结果是否参与计算 ")]/following-sibling::div'
        ]
        select_xpath_list2 = [
            '//div[contains(text(),"方案是否循环执行 ")]/following-sibling::div//input[@class="ivu-select-input"]',
            '//div[contains(text(),"物料齐套方式 ")]/following-sibling::div//input[@class="ivu-select-input"]',
            '//div[contains(text(),"是否释放不齐套料 ")]/following-sibling::div//input[@class="ivu-select-input"]',
            '//div[contains(text(),"齐套回答基准项 ")]/following-sibling::div//input[@class="ivu-select-input"]',
            '//div[contains(text(),"是否启用最小齐套量 ")]/following-sibling::div//input[@class="ivu-select-input"]',
            '//div[contains(text(),"是否考虑物料替代 ")]/following-sibling::div//input[@class="ivu-select-input"]',
            # '//div[contains(text(),"是否考虑最小替代量 ")]/following-sibling::div',
            '//div[contains(text(),"物料欠料计算方式 ")]/following-sibling::div//input[@class="ivu-select-input"]',
            '//div[contains(text(),"是否按替代比例拆分订单 ")]/following-sibling::div//input[@class="ivu-select-input"]',
            '//div[contains(text(),"齐套结果是否参与计算 ")]/following-sibling::div//input[@class="ivu-select-input"]'
        ]
        select_value_list = [
            '是',
            '分批齐套',
            '否',
            '按下阶齐套标识物料',
            '否',
            '否',
            # '否',
            '考虑替代,产生分配明细',
            '否',
            '否'
        ]
        sched.batch_selection_dropdown(select_xpath_list, select_value_list)

        sleep(1)
        expression_list = [
            '//div[text()="齐套结果供应有效条件式 "]/following-sibling::div'
        ]
        sched.expression_click(expression_list)
        sleep(1)
        # 点击主替代料不混用排序设置
        sched.click_button('//div[contains(text(),"主替代料不混用排序设置 ")]/following-sibling::div')
        # 点击+号
        sched.click_button(
            '(//div[@class="flex-j-c-between editButtonPadding"])//button[@class="m-r-5 ivu-btn ivu-btn-primary ivu-btn-small ivu-btn-icon-only"][1]')
        # 点击排序键名称下拉
        sched.click_button('(//div[@class="vxe-select size--mini is--filter"])[1]')
        # 选择第二项
        sched.click_button('(//div[@class="vxe-select-option--wrapper"])[1]//div[2]')
        sleep(2)
        # 点击排序方式下拉
        sched.click_button('(//div[@class="vxe-select size--mini is--filter"])[1]')
        # # 选择第一项 升序
        sched.click_button('(//div[@class="vxe-select-option--wrapper"])[2]//div[1]')
        sched.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[3]//span[text()="确定"]')
        # 供需计算开启线程的最大数目设置2
        sched.enter_texts('//div[@class="w-b-100 ivu-input-number ivu-input-number-small"]//input', 2)
        sleep(1)
        sched.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]//span[text()="确定"]')
        # 保存刷新后打开属性设置弹窗
        sched.get_after_value(name)

        sleep(1)
        sched.click_button('//div[text()=" 齐套计算规则 "]')
        sleep(1)
        tabs1 = sched.batch_acquisition_input(select_xpath_list2, select_value_list)
        text_xpath_list = [
            '//div[text()="主替代料不混用排序设置 "]/following-sibling::div//p',
            '//div[text()="齐套结果供应有效条件式 "]/following-sibling::div//p'
        ]
        value_list = [
            '主料优先 asc',
            'Abs(-100.28)'
        ]
        res_data = sched.batch_acquisition_text(text_xpath_list, value_list)
        # 下拉框xpath
        tabs1 = sched.batch_acquisition_input(select_xpath_list2, select_value_list)
        number_list = sched.batch_acquisition_input(['//div[contains(text(),"方案循环执行次数 ")]/following-sibling::div//input[@class="ivu-input-number-input"]'], ['2'])
        print('tabs1', tabs1)
        assert len(tabs1) == len(select_xpath_list) and len(res_data) == len(text_xpath_list) and len(number_list) == 1
        assert not sched.has_fail_message()

    @allure.story("属性设置-齐套其它设置保存")
    # @pytest.mark.run(order=1)
    def test_sched_attribute5(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "标准方案复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()

        # 点击tab切换齐套计算规则
        sleep(1)
        sched.click_button('//div[text()=" 齐套其它设置 "]')
        sleep(1)
        # 齐套运算结果保留次数设置5
        ele = sched.get_find_element_xpath(
            '//div[@class="w-b-100 ivu-input-number ivu-input-number-small"]//input'
        )
        ele.send_keys(Keys.CONTROL, "a")
        ele.send_keys(Keys.BACK_SPACE)
        sleep(1)
        sched.enter_texts(
            '//div[@class="w-b-100 ivu-input-number ivu-input-number-small"]//input', "5"
        )
        select_xpath_list = [
            '//div[contains(text(),"齐套运算结果保留方式 ")]/following-sibling::div'
        ]
        select_value_list = [
            '按全局'
        ]
        sched.batch_selection_dropdown(select_xpath_list, select_value_list)

        sched.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]//span[text()="确定"]')
        # 保存刷新后打开属性设置弹窗
        sched.get_after_value(name)

        sleep(1)
        sched.click_button('//div[text()=" 齐套其它设置 "]')
        sleep(1)
        number_list = sched.batch_acquisition_input([
            '//div[contains(text(),"齐套运算结果保留方式 ")]/following-sibling::div//input[@class="ivu-select-input"]',
            '//div[contains(text(),"齐套运算结果保留次数 ")]/following-sibling::div//input[@class="ivu-input-number-input"]'
        ], ['按全局', '5'])
        print('number_list', number_list)
        assert len(number_list) == 2
        assert not sched.has_fail_message()

    @allure.story("属性设置-交付计算规则保存")
    # @pytest.mark.run(order=1)
    def test_sched_attribute5(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "标准方案复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()

        # 点击tab切换齐套计算规则
        sleep(1)
        sched.click_button('//div[text()=" 交付计算规则 "]')
        sleep(1)
        # 交付锁定期间设置5
        ele = sched.get_find_element_xpath(
            '//div[contains(text(),"交付锁定期间 ")]/following-sibling::div//input'
        )
        ele.send_keys(Keys.CONTROL, "a")
        ele.send_keys(Keys.BACK_SPACE)
        sleep(1)
        sched.enter_texts(
            '//div[contains(text(),"交付锁定期间 ")]/following-sibling::div//input', "5"
        )

        # 安全库存天数设置6
        ele = sched.get_find_element_xpath(
            '//div[contains(text(),"安全库存天数 ")]/following-sibling::div//input'
        )
        ele.send_keys(Keys.CONTROL, "a")
        ele.send_keys(Keys.BACK_SPACE)
        sleep(1)
        sched.enter_texts(
            '//div[contains(text(),"安全库存天数 ")]/following-sibling::div//input', "6"
        )

        # 交货提前天数设置2
        ele = sched.get_find_element_xpath(
            '//div[contains(text(),"交货提前天数 ")]/following-sibling::div//input'
        )
        ele.send_keys(Keys.CONTROL, "a")
        ele.send_keys(Keys.BACK_SPACE)
        sleep(1)
        sched.enter_texts(
            '//div[contains(text(),"交货提前天数 ")]/following-sibling::div//input', "2"
        )

        select_xpath_list = [
            '//div[contains(text(),"交付分配方式 ")]/following-sibling::div'
        ]
        select_value_list = [
            '按月'
        ]
        sched.batch_selection_dropdown(select_xpath_list, select_value_list)
        sleep(1)
        # 批量修改表达式
        expression_list = [
            '//div[text()="交付需求数据筛选 "]/following-sibling::div',
            '//div[text()="交付计算开始日期 "]/following-sibling::div',
            '//div[text()="交付计算结束日期 "]/following-sibling::div'
        ]
        sched.expression_click(expression_list)
        sleep(1)

        sched.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]//span[text()="确定"]')
        # 保存刷新后打开属性设置弹窗
        sched.get_after_value(name)

        sleep(1)
        sched.click_button('//div[text()=" 交付计算规则 "]')
        sleep(1)
        number_list = sched.batch_acquisition_input([
            '//div[contains(text(),"交付锁定期间 ")]/following-sibling::div//input',
            '//div[contains(text(),"安全库存天数 ")]/following-sibling::div//input',
            '//div[contains(text(),"交货提前天数 ")]/following-sibling::div//input',
            '//div[contains(text(),"交付分配方式 ")]/following-sibling::div//input[@class="ivu-select-input"]'
        ], ['5', '6', '2', '按月'])

        text_xpath_list = [
            '//div[text()="交付需求数据筛选 "]/following-sibling::div//p',
            '//div[text()="交付计算开始日期 "]/following-sibling::div//p',
            '//div[text()="交付计算结束日期 "]/following-sibling::div//p'
        ]
        value_list = [
            'Abs(-100.28)',
            'Abs(-100.28)',
            'Abs(-100.28)'
        ]
        res_data = sched.batch_acquisition_text(text_xpath_list, value_list)
        print('number_list', number_list)
        assert len(number_list) == 4 and len(res_data) == len(value_list)
        assert not sched.has_fail_message()

    @allure.story("属性设置-设置保存")
    # @pytest.mark.run(order=1)
    def test_sched_attribute6(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "标准方案复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()

        # 点击tab切换齐套计算规则
        sleep(1)
        sched.click_button('//div[text()=" 设置 "]')
        sleep(1)
        sched.enter_texts(
            '//div[contains(text(),"设置生成的计划单(自制)的前缀字符 ")]/following-sibling::div//input', "2"
        )
        sched.enter_texts(
            '//div[contains(text(),"设置生成的计划单(外购)的前缀字符 ")]/following-sibling::div//input', "3"
        )

        select_xpath_list = [
            '//div[contains(text(),"设置生成的计划单(自制)是否包含底层料号 ")]/following-sibling::div',
            '//div[contains(text(),"设置生成的计划单(外购)是否包含底层料号 ")]/following-sibling::div'
        ]
        select_value_list = [
            '是',
            '是'
        ]
        sched.batch_selection_dropdown(select_xpath_list, select_value_list)
        sleep(1)
        # 批量修改表达式
        number_xpath_list = [
            '//div[contains(text(),"设置生成的计划单(自制)的流水号位数 ")]/following-sibling::div//input',
            '//div[contains(text(),"设置生成的计划单(外购)的流水号位数 ")]/following-sibling::div//input'
        ]
        number_value_list = [
            '5',
            '6'
        ]
        sched.batch_modify_input_number(number_xpath_list, number_value_list)
        sleep(1)

        sched.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]//span[text()="确定"]')

        # 保存刷新后打开属性设置弹窗
        sched.get_after_value(name)

        sleep(1)
        sched.click_button('//div[text()=" 设置 "]')
        sleep(1)
        number_list = sched.batch_acquisition_input([
            '//div[contains(text(),"设置生成的计划单(自制)的前缀字符 ")]/following-sibling::div//input',
            '//div[contains(text(),"设置生成的计划单(自制)的流水号位数 ")]/following-sibling::div//input',
            '//div[contains(text(),"设置生成的计划单(自制)是否包含底层料号 ")]/following-sibling::div//input[@class="ivu-select-input"]',
            '//div[contains(text(),"设置生成的计划单(外购)的前缀字符 ")]/following-sibling::div//input',
            '//div[contains(text(),"设置生成的计划单(外购)的流水号位数 ")]/following-sibling::div//input',
            '//div[contains(text(),"设置生成的计划单(外购)是否包含底层料号 ")]/following-sibling::div//input[@class="ivu-select-input"]'
        ], ['2', '5', '是', '3', '6', '是'])
        print('number_list', number_list)
        assert len(number_list) == 6
        assert not sched.has_fail_message()

    @allure.story("属性设置-通用属性")
    # @pytest.mark.run(order=1)
    def test_sched_attribute6(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "标准方案复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()

        # 点击tab切换齐套计算规则
        sleep(1)
        sched.click_button('//div[text()=" 通用属性 "]')
        sleep(1)
        sched.enter_texts(
            '//div[text()="别名 "]/following-sibling::div//input', "测试别名"
        )
        sleep(1)

        sched.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]//span[text()="确定"]')

        # 保存刷新后打开属性设置弹窗
        sched.get_after_value(name)

        sleep(1)
        sched.click_button('//div[text()=" 通用属性 "]')
        sleep(1)
        number_list = sched.batch_acquisition_input([
            '//div[text()="别名 "]/following-sibling::div//input'
        ], ['测试别名'])
        print('number_list', number_list)
        assert len(number_list) == 1
        assert not sched.has_fail_message()

    @allure.story("属性设置-分派规则-降序")
    # @pytest.mark.run(order=1)
    def test_sched_rule1(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击对话框
        sched.click_button(
            '//div[text()="分派规则"]/following-sibling::div//i[@class="ivu-icon ivu-icon-md-albums"]'
        )

        ele = driver.find_elements(
            By.XPATH,
            '(//div[text()="分派规则"])[3]/ancestor::div[1]/following-sibling::div[1]//input[@class="ivu-select-input"]',
        )
        ele[0].click()
        sched.click_button('//li[text()="OLD合批日期"]')
        sele_text1 = ele[0].get_attribute("value")
        ele[1].click()
        sched.click_button('//li[text()="降序"]')
        sele_text2 = ele[1].get_attribute("value")
        sched.click_ok_button()
        sleep(2)
        # 获取输入框数据
        befort_input = sched.get_find_element_xpath(
            '//div[text()="分派规则"]/following-sibling::div//p'
        ).text
        sched.get_after_value(name)
        after_input = sched.get_find_element_xpath(
            '//div[text()="分派规则"]/following-sibling::div//p'
        ).text
        assert (
            befort_input == after_input == 'ME.Order.UserDate1,d'
            and sele_text1 == "OLD合批日期"
            and sele_text2 == "降序"
        )
        assert not sched.has_fail_message()


