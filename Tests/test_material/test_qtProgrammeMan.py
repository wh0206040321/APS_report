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

from Pages.itemsPage.login_page import LoginPage
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
@pytest.mark.run(order=106)
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
            '//div[contains(text(),"是否考虑最小替代量 ")]/following-sibling::div',
            '//div[contains(text(),"物料欠料计算方式 ")]/following-sibling::div',
        ]
        select_value_list = [
            '是',
            '分批齐套',
            '否',
            '按下阶齐套标识物料',
            '否',
            '否',
            '否',
            '考虑替代,产生分配明细',
        ]
        sched.batch_selection_dropdown(select_xpath_list, select_value_list)
        input()
        assert True
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

    @allure.story("属性设置-分派规则-升序")
    # @pytest.mark.run(order=1)
    def test_sched_rule2(self, login_to_sched):
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
        sched.click_button('//li[text()="OLD订单类别"]')
        sele_text1 = ele[0].get_attribute("value")
        ele[1].click()
        sched.click_button('//li[text()="升序"]')
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
            befort_input == after_input == 'ME.Order.UserStr2,a'
            and sele_text1 == "OLD订单类别"
            and sele_text2 == "升序"
        )
        assert not sched.has_fail_message()

    @allure.story("属性设置-不填写数据不允许提交")
    # @pytest.mark.run(order=1)
    def test_sched_rule3(self, login_to_sched):
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

        # 点击添加
        sched.click_button('(//i[@class="ivu-icon ivu-icon-md-add"])[2]')

        sched.click_ok_button()
        message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="ivu-message"]//span')
            )
        )
        # 检查元素是否包含子节点
        sleep(1)
        assert message.text == "请把信息填写完整"
        assert not sched.has_fail_message()

    @allure.story("属性设置-分派失败时(资源锁定制约)")
    # @pytest.mark.run(order=1)
    def test_sched_dispatchfailed1(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击下拉框
        sched.click_button(
            '//div[text()="分派失败时(资源锁定制约)"]/following-sibling::div'
        )
        sched.click_button(
            '//div[text()="分派失败时(资源锁定制约)"]/following-sibling::div//ul[2]/li[2]'
        )
        sleep(1)
        befort_input = sched.get_find_element_xpath(
            '//div[text()="分派失败时(资源锁定制约)"]/following-sibling::div//input/following-sibling::div/input'
        ).get_attribute("value")
        sched.get_after_value(name)
        after_input = sched.get_find_element_xpath(
            '//div[text()="分派失败时(资源锁定制约)"]/following-sibling::div//input/following-sibling::div/input'
        ).get_attribute("value")
        assert befort_input == after_input == '忽视制约'
        assert not sched.has_fail_message()

    @allure.story("属性设置-分派失败时(最大移动时间制约)")
    # @pytest.mark.run(order=1)
    def test_sched_dispatchfailed2(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击下拉框
        sched.click_button(
            '//div[text()="分派失败时(最大移动时间制约)"]/following-sibling::div'
        )
        sched.click_button(
            '//div[text()="分派失败时(最大移动时间制约)"]/following-sibling::div//ul[2]/li[2]'
        )
        sleep(1)
        befort_input = sched.get_find_element_xpath(
            '//div[text()="分派失败时(最大移动时间制约)"]/following-sibling::div//input/following-sibling::div/input'
        ).get_attribute("value")
        sched.get_after_value(name)
        after_input = sched.get_find_element_xpath(
            '//div[text()="分派失败时(最大移动时间制约)"]/following-sibling::div//input/following-sibling::div/input'
        ).get_attribute("value")
        assert befort_input == after_input == '忽视制约'
        assert not sched.has_fail_message()

    @allure.story("属性设置-分派停止条件式")
    # @pytest.mark.run(order=1)
    def test_sched_dispatchstopped(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击对话框
        sched.click_button(
            '//div[text()="分派停止条件式"]/following-sibling::div//i[@class="ivu-icon ivu-icon-md-albums"]'
        )

        # 点击添加
        sched.click_button('//div[text()=" 标准登录 "]')
        element = sched.get_find_element_xpath(
            '//span[text()="大前个工序分派的主资源为A"]'
        )
        actions = ActionChains(driver)
        # 双击命令
        actions.double_click(element).perform()

        sched.click_ok_button()
        sleep(2)
        # 获取输入框数据
        befort_input = sched.get_find_element_xpath(
            '//div[text()="分派停止条件式"]/following-sibling::div//p'
        ).text
        sched.get_after_value(name)
        after_input = sched.get_find_element_xpath(
            '//div[text()="分派停止条件式"]/following-sibling::div//p'
        ).text
        assert "ME.PrevOperation[1].PrevOperation[1].IsAssigned!='0'&&ME.PrevOperation[1].PrevOperation[1].OperationMainRes=='A'" in befort_input == after_input
        assert not sched.has_fail_message()

    @allure.story("属性设置-分派资源")
    # @pytest.mark.run(order=1)
    def test_sched_allocateresources(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击下拉框
        sched.click_button('//div[text()="分派资源"]/following-sibling::div')
        sched.click_button(
            '//div[text()="分派资源"]/following-sibling::div//ul[2]/li[2]'
        )
        sleep(1)
        befort_input = sched.get_find_element_xpath(
            '//div[text()="分派资源"]/following-sibling::div//input/following-sibling::div/input'
        ).get_attribute("value")
        sched.get_after_value(name)
        after_input = sched.get_find_element_xpath(
            '//div[text()="分派资源"]/following-sibling::div//input/following-sibling::div/input'
        ).get_attribute("value")
        assert befort_input == after_input == '优先资源'
        assert not sched.has_fail_message()

    @allure.story("属性设置-更新关联/补充订单")
    # @pytest.mark.run(order=1)
    def test_sched_order(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击下拉框
        sched.click_button('//div[text()="更新关联/补充订单"]/following-sibling::div')
        sched.click_button(
            '//div[text()="更新关联/补充订单"]/following-sibling::div//ul[2]/li[2]'
        )
        sleep(1)
        befort_input = sched.get_find_element_xpath(
            '//div[text()="更新关联/补充订单"]/following-sibling::div//input/following-sibling::div/input'
        ).get_attribute("value")
        sched.get_after_value(name)
        after_input = sched.get_find_element_xpath(
            '//div[text()="更新关联/补充订单"]/following-sibling::div//input/following-sibling::div/input'
        ).get_attribute("value")
        assert befort_input == after_input == '是'
        assert not sched.has_fail_message()

    @allure.story("属性设置-工作临时固定")
    # @pytest.mark.run(order=1)
    def test_sched_work(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击下拉框
        sched.click_button('//div[text()="工作临时固定"]/following-sibling::div')
        sched.click_button(
            '//div[text()="工作临时固定"]/following-sibling::div//ul[2]/li[2]'
        )
        sleep(1)
        befort_input = sched.get_find_element_xpath(
            '//div[text()="工作临时固定"]/following-sibling::div//input/following-sibling::div/input'
        ).get_attribute("value")
        sched.get_after_value(name)
        after_input = sched.get_find_element_xpath(
            '//div[text()="工作临时固定"]/following-sibling::div//input/following-sibling::div/input'
        ).get_attribute("value")
        assert befort_input == after_input == '分派结束工作'
        assert not sched.has_fail_message()

    @allure.story("属性设置-忽视未分派的前后工序的工作")
    # @pytest.mark.run(order=1)
    def test_sched_neglectingwork(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击下拉框
        sched.click_button(
            '//div[text()="忽视未分派的前后工序的工作"]/following-sibling::div'
        )
        sched.click_button(
            '//div[text()="忽视未分派的前后工序的工作"]/following-sibling::div//ul[2]/li[2]'
        )
        sleep(1)
        befort_input = sched.get_find_element_xpath(
            '//div[text()="忽视未分派的前后工序的工作"]/following-sibling::div//input/following-sibling::div/input'
        ).get_attribute("value")
        sched.get_after_value(name)
        after_input = sched.get_find_element_xpath(
            '//div[text()="忽视未分派的前后工序的工作"]/following-sibling::div//input/following-sibling::div/input'
        ).get_attribute("value")
        assert befort_input == after_input == '是'
        assert not sched.has_fail_message()

    @allure.story("属性设置-启用原料库存制约")
    # @pytest.mark.run(order=1)
    def test_sched_restrict(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击下拉框
        sched.click_button('//div[text()="启用原料库存制约"]/following-sibling::div')
        sched.click_button(
            '//div[text()="启用原料库存制约"]/following-sibling::div//ul[2]/li[2]'
        )
        sleep(1)
        befort_input = sched.get_find_element_xpath(
            '//div[text()="启用原料库存制约"]/following-sibling::div//input/following-sibling::div/input'
        ).get_attribute("value")
        sched.get_after_value(name)
        after_input = sched.get_find_element_xpath(
            '//div[text()="启用原料库存制约"]/following-sibling::div//input/following-sibling::div/input'
        ).get_attribute("value")
        assert befort_input == after_input == '是'
        assert not sched.has_fail_message()

    @allure.story("属性设置-筛选工作")
    # @pytest.mark.run(order=1)
    def test_sched_screeningwork(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击对话框
        sched.click_button(
            '//div[text()="筛选工作"]/following-sibling::div//i[@class="ivu-icon ivu-icon-md-albums"]'
        )

        # 点击添加
        sched.click_button('//div[text()=" 标准登录 "]')

        element = sched.get_find_element_xpath('//span[text()="订单规格1等于‘A’"]')
        actions = ActionChains(driver)
        # 双击命令
        actions.double_click(element).perform()

        sched.click_ok_button()
        sleep(2)
        # 获取输入框数据
        befort_input = sched.get_find_element_xpath(
            '//div[text()="筛选工作"]/following-sibling::div//p'
        ).text
        sched.get_after_value(name)
        after_input = sched.get_find_element_xpath(
            '//div[text()="筛选工作"]/following-sibling::div//p'
        ).text
        assert befort_input == after_input
        assert "ME.Order.Spec1=='A'" in befort_input
        assert not sched.has_fail_message()

    @allure.story("属性设置-筛选订单")
    # @pytest.mark.run(order=1)
    def test_sched_filterorders(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击对话框
        sched.click_button(
            '//div[text()="筛选订单"]/following-sibling::div//i[@class="ivu-icon ivu-icon-md-albums"]'
        )

        # 点击添加
        sched.click_button('//div[text()=" 标准登录 "]')

        element = sched.get_find_element_xpath('//span[text()="采购订单"]')
        actions = ActionChains(driver)
        # 双击命令
        actions.double_click(element).perform()

        sched.click_ok_button()
        sleep(2)
        # 获取输入框数据
        befort_input = sched.get_find_element_xpath(
            '//div[text()="筛选订单"]/following-sibling::div//p'
        ).text
        sched.get_after_value(name)
        after_input = sched.get_find_element_xpath(
            '//div[text()="筛选订单"]/following-sibling::div//p'
        ).text
        assert befort_input == after_input
        assert "ME.Order_Type=='P'" in befort_input
        assert not sched.has_fail_message()

    @allure.story("属性设置-严格遵守后资源制约-开关开启")
    # @pytest.mark.run(order=1)
    def test_sched_resourceconstraints1(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击开关
        ele = sched.get_find_element_xpath(
            '//div[text()="严格遵守后资源制约"]/following-sibling::div//span[1]'
        )
        if ele.get_attribute("class") == "ivu-switch ivu-switch-default":
            sched.click_button(
                '//div[text()="严格遵守后资源制约"]/following-sibling::div//span[1]'
            )
        sleep(1)
        # 获取输入框数据
        befort_class = sched.get_find_element_xpath(
            '//div[text()="严格遵守后资源制约"]/following-sibling::div//span[1]'
        ).get_attribute("class")
        sched.get_after_value(name)
        after_class = sched.get_find_element_xpath(
            '//div[text()="严格遵守后资源制约"]/following-sibling::div//span[1]'
        ).get_attribute("class")
        assert befort_class == after_class
        assert (
            befort_class
            == "ivu-switch ivu-switch-checked ivu-switch-default"
        )
        assert not sched.has_fail_message()

    @allure.story("属性设置-严格遵守后资源制约-开关关闭")
    # @pytest.mark.run(order=1)
    def test_sched_resourceconstraints2(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击开关
        ele = sched.get_find_element_xpath(
            '//div[text()="严格遵守后资源制约"]/following-sibling::div//span[1]'
        )
        if (
            ele.get_attribute("class")
            == "ivu-switch ivu-switch-checked ivu-switch-default"
        ):
            sched.click_button(
                '//div[text()="严格遵守后资源制约"]/following-sibling::div//span[1]'
            )

        # 获取输入框数据
        befort_class = sched.get_find_element_xpath(
            '//div[text()="严格遵守后资源制约"]/following-sibling::div//span[1]'
        ).get_attribute("class")
        sched.get_after_value(name)
        after_class = sched.get_find_element_xpath(
            '//div[text()="严格遵守后资源制约"]/following-sibling::div//span[1]'
        ).get_attribute("class")
        assert befort_class == after_class
        assert befort_class == "ivu-switch ivu-switch-default"
        assert not sched.has_fail_message()

    @allure.story("属性设置-制造效率")
    # @pytest.mark.run(order=1)
    def test_sched_restrictnum(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击数字框
        ele = sched.get_find_element_xpath(
            '//div[text()="制造效率"]/following-sibling::div//input'
        )
        ele.send_keys(Keys.CONTROL, "a")
        ele.send_keys(Keys.BACK_SPACE)
        sched.enter_texts(
            '//div[text()="制造效率"]/following-sibling::div//input', "1aQ!~_-1+=0.8"
        )
        sleep(1)
        befort_input = sched.get_find_element_xpath(
            '//div[text()="制造效率"]/following-sibling::div//input'
        ).get_attribute("value")
        sched.get_after_value(name)
        after_input = sched.get_find_element_xpath(
            '//div[text()="制造效率"]/following-sibling::div//input'
        ).get_attribute("value")
        assert befort_input == after_input
        assert befort_input == "110.8"
        assert not sched.has_fail_message()

    @allure.story("属性设置-新增资源选择策略")
    # @pytest.mark.run(order=1)
    def test_sched_add_resourcefailed(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击对话框
        sched.click_button(
            '//div[text()="资源选择策略"]/following-sibling::div//i[@class="ivu-icon ivu-icon-md-albums"]'
        )

        # 点击策略
        sched.click_button('(//i[@class="ivu-icon ivu-icon-md-add"])[2]')
        # 点击确认
        sched.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[3]/button[1]'
        )

        message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="el-message el-message--error"]//p')
            )
        )
        # 检查元素是否包含子节点
        sleep(1)
        assert message.text == "请填写策略名称"
        assert not sched.has_fail_message()

    @allure.story("属性设置-新增资源选择策略")
    # @pytest.mark.run(order=1)
    def test_sched_add_resourcesuccess(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击对话框
        sched.click_button(
            '//div[text()="资源选择策略"]/following-sibling::div//i[@class="ivu-icon ivu-icon-md-albums"]'
        )

        # 点击策略
        sched.click_button('(//i[@class="ivu-icon ivu-icon-md-add"])[2]')
        # 填写策略名称
        sleep(1)
        sched.enter_texts(
            '(//p[text()=" 策略名称 "])[2]/following-sibling::div//input', "策略名称111"
        )
        # 点击确认
        sched.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[3]/button[1]'
        )
        sleep(1)
        before_text = sched.get_find_element_xpath(
            '//div[@class="flex-1 p-r-10 overflow-auto"]/div[contains(text(), "策略名称111")]'
        ).text
        sched.click_button('(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]//span[text()="确定"]')
        sched.get_after_value(name)
        sleep(1)
        # 点击对话框
        sched.click_button(
            '(//div[text()="资源选择策略"]/following-sibling::div)[2]//i'
        )

        after_text = sched.get_find_element_xpath(
            '//div[@class="flex-1 p-r-10 overflow-auto"]//div[contains(text(), "策略名称111")]'
        ).text
        assert before_text == after_text == "策略名称111"
        assert not sched.has_fail_message()

    @allure.story("属性设置-新增资源选择策略-评估方案")
    # @pytest.mark.run(order=1)
    def test_sched_add_resourcesuccess1(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击对话框
        sched.click_button(
            '//div[text()="资源选择策略"]/following-sibling::div//i[@class="ivu-icon ivu-icon-md-albums"]'
        )

        # 点击策略
        sched.click_button('(//i[@class="ivu-icon ivu-icon-md-add"])[2]')
        # 填写策略名称
        sleep(1)
        sched.enter_texts(
            '(//p[text()=" 策略名称 "])[2]/following-sibling::div//input', "策略名称222"
        )
        # 点击确认
        sched.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[3]/button[1]'
        )

        sched.click_button('//div[text()=" 策略名称222 "]')

        sched.click_button(
            '(//input[@class="ivu-select-input" and @placeholder="请选择"])[1]'
        )
        sched.click_button('//li[text()="AS相同物料优先"]')
        sched.click_button('(//input[@placeholder="请输入数字"])[2]')
        sched.enter_texts('(//input[@placeholder="请输入数字"])[2]', "1aQ!~_-1+=0.8")

        before_input_text = sched.get_find_element_xpath(
            '//div[@class="flex-1"]//input[@class="ivu-select-input"]'
        ).get_attribute("value")
        before_input_num = sched.get_find_element_xpath(
            '(//input[@placeholder="请输入数字"])[2]'
        ).get_attribute("value")

        sched.click_button('(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]//span[text()="确定"]')

        input_after = sched.get_find_element_xpath(
            '//div[text()="资源选择策略"]/following-sibling::div//p'
        )
        sched.click_ok_button()
        # 点击对话框
        sched.click_button(
            '(//div[text()="资源选择策略"]/following-sibling::div)[2]//i'
        )

        after_input_text = sched.get_find_element_xpath(
            '//div[@class="flex-1"]//input[@class="ivu-select-input"]'
        ).get_attribute("value")
        after_input_num = sched.get_find_element_xpath(
            '(//input[@placeholder="请输入数字"])[2]'
        ).get_attribute("value")
        assert (
            before_input_text == after_input_text == "AS相同物料优先"
            and before_input_num == after_input_num == "110.8"
            and input_after.text == "(集合)"
        )
        assert not sched.has_fail_message()

    @allure.story("属性设置-新增资源选择策略-不允许命名一致")
    # @pytest.mark.run(order=1)
    def test_sched_add_resourcefail(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        # 点击对话框
        sched.click_button(
            '//div[text()="资源选择策略"]/following-sibling::div//i[@class="ivu-icon ivu-icon-md-albums"]'
        )

        # 点击策略
        sched.click_button('(//i[@class="ivu-icon ivu-icon-md-add"])[2]')
        # 填写策略名称
        sleep(1)
        sched.enter_texts(
            '(//p[text()=" 策略名称 "])[2]/following-sibling::div//input', "策略名称111"
        )
        # 点击确认
        sched.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[3]/button[1]'
        )
        message = sched.get_find_message().text
        assert message == "记录已存在,请检查！"
        assert not sched.has_fail_message()

    @allure.story("属性设置-时间属性-分派开始时间")
    # @pytest.mark.run(order=1)
    def test_sched_starttime(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        sched.click_time_sched()
        # 点击分派开始时间对话框
        sched.click_button(
            '//div[text()="分派开始时间"]/following-sibling::div//div[@class="w-b-100 h-100 flex-alignItems-center cursor-pointer"]'
        )
        sched.click_button('//div[text()=" 标准登录 "]')
        ele = sched.get_find_element_xpath(
            '//span[text()="收集的工作中最早的开始时刻"]'
        )
        action = ActionChains(driver)
        action.double_click(ele).perform()
        sleep(1)
        sched.click_ok_button()
        sleep(2)
        before_div_text = sched.get_find_element_xpath(
            '//div[text()="分派开始时间"]/following-sibling::div//div[@class="w-b-100 h-100 flex-alignItems-center cursor-pointer"]'
        ).text
        sched.get_after_value(name)
        sched.click_time_sched()
        after_div_text = sched.get_find_element_xpath(
            '//div[text()="分派开始时间"]/following-sibling::div//div[@class="w-b-100 h-100 flex-alignItems-center cursor-pointer"]'
        ).text
        assert "Min(ME.Command_OperationList,TARGET.Work_StartTime)" in before_div_text == after_div_text
        assert not sched.has_fail_message()

    @allure.story("属性设置-时间属性-分派结束时间")
    # @pytest.mark.run(order=1)
    def test_sched_endtime(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        sched.click_time_sched()
        # 点击分派开始时间对话框
        sched.click_button(
            '//div[text()="分派结束时间"]/following-sibling::div//div[@class="w-b-100 h-100 flex-alignItems-center cursor-pointer"]'
        )
        sched.click_button('//div[text()=" 标准登录 "]')
        ele = sched.get_find_element_xpath(
            '//span[text()="收集的工作中最迟的结束时刻的次日"]'
        )
        action = ActionChains(driver)
        action.double_click(ele).perform()

        sched.click_ok_button()
        sleep(2)
        before_div_text = sched.get_find_element_xpath(
            '//div[text()="分派结束时间"]/following-sibling::div//div[@class="w-b-100 h-100 flex-alignItems-center cursor-pointer"]'
        ).text
        sched.get_after_value(name)
        sched.click_time_sched()
        after_div_text = sched.get_find_element_xpath(
            '//div[text()="分派结束时间"]/following-sibling::div//div[@class="w-b-100 h-100 flex-alignItems-center cursor-pointer"]'
        ).text
        assert "Max(ME.Command_OperationList,TARGET.Work_EndTime)+1d" in before_div_text == after_div_text
        assert not sched.has_fail_message()

    @allure.story("属性设置-时间属性-用户指定最早开始时刻")
    # @pytest.mark.run(order=1)
    def test_sched_moststarttime(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        sched.click_time_sched()
        # 点击分派开始时间对话框
        sched.click_button(
            '//div[text()="用户指定最早开始时刻"]/following-sibling::div//div[@class="w-b-100 h-100 flex-alignItems-center cursor-pointer"]'
        )
        sched.click_button('//div[text()=" 标准登录 "]')
        ele = sched.get_find_element_xpath(
            '//span[text()="从第1个子工作的开始时间起5个小时后"]'
        )
        action = ActionChains(driver)
        action.double_click(ele).perform()

        sched.click_ok_button()
        sleep(2)
        before_div_text = sched.get_find_element_xpath(
            '//div[text()="用户指定最早开始时刻"]/following-sibling::div//div[@class="w-b-100 h-100 flex-alignItems-center cursor-pointer"]'
        ).text
        sched.get_after_value(name)
        sched.click_time_sched()
        after_div_text = sched.get_find_element_xpath(
            '//div[text()="用户指定最早开始时刻"]/following-sibling::div//div[@class="w-b-100 h-100 flex-alignItems-center cursor-pointer"]'
        ).text
        assert "ME.Parent.Work_StartTime+5h" in before_div_text == after_div_text
        assert not sched.has_fail_message()

    @allure.story("属性设置-时间属性-用户指定最迟结束时刻")
    # @pytest.mark.run(order=1)
    def test_sched_mostendtime(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        # 选择排产方案(订单级)复制方案
        sched.click_button(f'//ul[@visible="visible"]//ul//span[text()="{name}"]')
        sched.click_attribute_button()
        sched.click_time_sched()
        # 点击分派开始时间对话框
        sched.click_button(
            '//div[text()="用户指定最迟结束时刻"]/following-sibling::div//div[@class="w-b-100 h-100 flex-alignItems-center cursor-pointer"]'
        )
        sched.click_button('//div[text()=" 标准登录 "]')
        ele = sched.get_find_element_xpath(
            '//span[text()="从第1个子工作的开始时间起5个小时后"]'
        )
        action = ActionChains(driver)
        action.double_click(ele).perform()

        sched.click_ok_button()
        sleep(2)
        before_div_text = sched.get_find_element_xpath(
            '//div[text()="用户指定最迟结束时刻"]/following-sibling::div//div[@class="w-b-100 h-100 flex-alignItems-center cursor-pointer"]'
        ).text
        sched.get_after_value(name)
        sched.click_time_sched()
        after_div_text = sched.get_find_element_xpath(
            '//div[text()="用户指定最迟结束时刻"]/following-sibling::div//div[@class="w-b-100 h-100 flex-alignItems-center cursor-pointer"]'
        ).text
        assert "ME.Parent.Work_StartTime+5h" in before_div_text == after_div_text
        assert not sched.has_fail_message()

    @allure.story("删除测试方案")
    # @pytest.mark.run(order=1)
    def test_sched_delsched3(self, login_to_sched):
        driver = login_to_sched  # WebDriver 实例
        sched = SchedPage(driver)  # 用 driver 初始化 SchedPage
        name = "排产方案(订单级)复制"
        sched.click_button(
            f'(//div[@class="ivu-radio-group ivu-radio-group-small ivu-radio-small ivu-radio-group-button"])[2]/label[text()="{name}"]'
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
