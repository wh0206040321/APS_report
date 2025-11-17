import logging
import os
from datetime import datetime
from time import sleep
import re
import allure
import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException

from Pages.itemsPage.adds_page import AddsPages
from Pages.itemsPage.login_page import LoginPage
from Pages.materialPage.materialData_page import MaterialDataPage
from Utils.data_driven import DateDriver
from Utils.driver_manager import create_driver, safe_quit, capture_screenshot


@pytest.fixture  # (scope="class")这个参数表示整个测试类共用同一个浏览器，默认一个用例执行一次
def login_to_materialsubstitution():
    driver = None
    try:
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
        list_ = ["物控管理", "物控基础数据", "物料替代"]
        for v in list_:
            page.click_button(f'(//span[text()="{v}"])[1]')
        yield driver  # 提供给测试用例使用
    finally:
        if driver:
            safe_quit(driver)


@allure.feature("物料替代页用例")
@pytest.mark.run(order=103)
class TestSMaterialSubstitutionPage:

    @allure.story("新增直接点击保存不允许添加")
    # @pytest.mark.run(order=1)
    def test_materialsubstitution_addfail1(self, login_to_materialsubstitution):
        driver = login_to_materialsubstitution  # WebDriver 实例
        material = MaterialDataPage(driver)  # 用 driver 初始化 MaterialDataPage
        layout = "测试布局A"
        material.add_layout(layout)
        # 获取布局名称的文本元素
        name = material.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        ).text

        material.click_all_button("新增")
        sleep(1)
        material.click_confirm()
        message = material.get_error_message()
        assert message == "校验不通过，请检查标红的表单字段！"
        assert layout == name
        assert not material.has_fail_message()

    @allure.story("只添加替代场景父料号不允许添加")
    # @pytest.mark.run(order=1)
    def test_materialsubstitution_addfail2(self, login_to_materialsubstitution):
        driver = login_to_materialsubstitution  # WebDriver 实例
        material = MaterialDataPage(driver)  # 用 driver 初始化 MaterialDataPage
        adds = AddsPages(driver)
        material.click_all_button("新增")
        select_list = [{"select": '//div[@id="h0590xfj-jemd"]//input', "value": '//div[@class="el-scrollbar"]//span[text()="常规替代"]'},
                       {"select": '//div[@id="gid148zp-0f98"]//input', "value": '(//div[@class="el-scrollbar"]//span[text()="*"])[last()]'}]
        adds.batch_modify_select_input(select_list)
        material.click_confirm()
        message = material.get_error_message()
        assert message == "校验不通过，请检查标红的表单字段！"
        assert not material.has_fail_message()

    @allure.story("添加单料替代成功")
    # @pytest.mark.run(order=1)
    def test_materialsubstitution_addsingle(self, login_to_materialsubstitution):
        driver = login_to_materialsubstitution  # WebDriver 实例
        material = MaterialDataPage(driver)  # 用 driver 初始化 MaterialDataPage
        material.wait_for_loading_to_disappear()
        before_data = material.get_find_element_xpath('(//span[contains(text(),"条记录")])[1]').text
        before_count = int(re.search(r'\d+', before_data).group())
        material.add_material_substitution(num=1)

        material.click_confirm()
        message = material.get_find_message()
        material.wait_for_loading_to_disappear()
        after_data = material.get_find_element_xpath('(//span[contains(text(),"条记录")])[1]').text
        after_count = int(re.search(r'\d+', after_data).group())
        assert after_count - before_count == 1, f"新增失败: 新增前 {before_count}, 删新增后 {after_count}"
        assert message == "新增成功！"
        assert not material.has_fail_message()

    @allure.story("添加成组替代成功")
    # @pytest.mark.run(order=1)
    def test_materialsubstitution_addgroup(self, login_to_materialsubstitution):
        driver = login_to_materialsubstitution  # WebDriver 实例
        material = MaterialDataPage(driver)  # 用 driver 初始化 MaterialDataPage
        material.wait_for_loading_to_disappear()
        before_data = material.get_find_element_xpath('(//span[contains(text(),"条记录")])[1]').text
        before_count = int(re.search(r'\d+', before_data).group())
        material.add_material_substitution(num=2, name="成组替代")

        material.click_confirm()
        message = material.get_find_message()
        material.wait_for_loading_to_disappear()
        after_data = material.get_find_element_xpath('(//span[contains(text(),"条记录")])[1]').text
        after_count = int(re.search(r'\d+', after_data).group())
        assert after_count - before_count == 1, f"新增失败: 新增前 {before_count}, 删新增后 {after_count}"
        assert message == "新增成功！"
        assert not material.has_fail_message()

    @allure.story("添加测试数据单料替代成功")
    # @pytest.mark.run(order=1)
    def test_materialsubstitution_addsingle1(self, login_to_materialsubstitution):
        driver = login_to_materialsubstitution  # WebDriver 实例
        material = MaterialDataPage(driver)  # 用 driver 初始化 MaterialDataPage
        material.wait_for_loading_to_disappear()
        before_data = material.get_find_element_xpath('(//span[contains(text(),"条记录")])[1]').text
        before_count = int(re.search(r'\d+', before_data).group())
        material.add_material_substitution(num=2)

        material.click_confirm()
        message = material.get_find_message()
        material.wait_for_loading_to_disappear()
        after_data = material.get_find_element_xpath('(//span[contains(text(),"条记录")])[1]').text
        after_count = int(re.search(r'\d+', after_data).group())
        assert after_count - before_count == 1, f"新增失败: 新增前 {before_count}, 删新增后 {after_count}"
        assert message == "新增成功！"
        assert not material.has_fail_message()

    @allure.story("修改单料替代BOM版本，替代后子项料号成功")
    # @pytest.mark.run(order=1)
    def test_materialsubstitution_updatesingle(self, login_to_materialsubstitution):
        driver = login_to_materialsubstitution  # WebDriver 实例
        material = MaterialDataPage(driver)  # 用 driver 初始化 MaterialDataPage
        material.click_update()
        material.click_button('//div[@id="g8b1op6y-vfpx"]/i')
        material.click_button('//div[@id="db2x9abu-154j"]//input')
        material.click_button('(//div[@class="el-scrollbar"])[last()]//div[@class="my-list-item"][1]')
        before_data = material.get_find_element_xpath('//div[@id="db2x9abu-154j"]//input').get_attribute("value")
        sleep(1)
        material.click_button('(//div[@class="vxe-modal--footer"]//span[text()="确定"])[2]')

        material.enter_texts('//div[@id="hji97w60-v76b"]//input', 6)
        material.click_confirm()
        message = material.get_find_message()
        material.wait_for_loading_to_disappear()

        material.click_flagdata()

        after_data = material.get_find_element_xpath('//table[@class="vxe-table--body"]//tr[1]/td[10]').text
        after_num = material.get_find_element_xpath('//table[@class="vxe-table--body"]//tr[1]/td[6]').text
        assert after_data == before_data and after_num == "6"
        assert message == "编辑成功！"
        assert not material.has_fail_message()

    @allure.story("修改成组替代BOM版本，被替代子项料号，替代后子项料号成功")
    # @pytest.mark.run(order=1)
    def test_materialsubstitution_updategroup(self, login_to_materialsubstitution):
        driver = login_to_materialsubstitution  # WebDriver 实例
        material = MaterialDataPage(driver)  # 用 driver 初始化 MaterialDataPage
        material.click_flagdata()
        material.click_button('(//table[@class="vxe-table--body"]//tr[td[4]//span[text()="成组替代"]]/td[2])[1]')
        sleep(1)
        material.click_all_button("编辑")
        material.wait_for_loading_to_disappear()

        material.click_button('//div[@id="g8b1op6y-vfpx"]/i')
        for i in range(2):
            material.click_button(f'(//button[not(@disabled)]//span[text()="删除"])[2]')
            material.click_button('//div[@class="ivu-modal-confirm-footer"]//span[text()="确定"]')
            sleep(1)

        before_data1 = material.get_find_element_xpath('//table[@class="vxe-table--body"]//tr[td[3]//button]/td[2]').text
        before_data2 = material.get_find_element_xpath('//table[@class="vxe-table--body"]//tr[td[6]//button]/td[2]').text
        material.click_button('(//div[@class="vxe-modal--footer"]//span[text()="确定"])[2]')

        material.enter_texts('//div[@id="hji97w60-v76b"]//input', 8)
        material.click_confirm()
        message = material.get_find_message()
        material.wait_for_loading_to_disappear()

        material.click_flagdata()

        after_data1 = material.get_find_element_xpath('//table[@class="vxe-table--body"]//tr[td[4]//span[text()="成组替代"]]/td[7]').text
        after_data2 = material.get_find_element_xpath('//table[@class="vxe-table--body"]//tr[td[4]//span[text()="成组替代"]]/td[10]').text
        after_num = material.get_find_element_xpath('//table[@class="vxe-table--body"]//tr[td[4]//span[text()="成组替代"]]/td[6]').text
        assert after_data1 == before_data1 and after_data2 == before_data2 and after_num == "8"
        assert message == "编辑成功！"
        assert not material.has_fail_message()

    @allure.story("查询替代类别成功")
    # @pytest.mark.run(order=1)
    def test_materialsubstitution_selectAlternativeCategories(self, login_to_materialsubstitution):
        driver = login_to_materialsubstitution  # WebDriver 实例
        material = MaterialDataPage(driver)  # 用 driver 初始化 MaterialDataPage
        material.wait_for_loading_to_disappear()
        material.click_button('//div[@id="ogx8hadg-224s"]//input')
        material.click_button('//div[@class="el-scrollbar"]//span[text()="单料替代"]')
        material.click_select_button()

        eles = material.loop_judgment('//table[@class="vxe-table--body"]//tr/td[4]')
        assert all('单料替代' == ele for ele in eles)
        assert not material.has_fail_message()

    @allure.story("查询父料号成功")
    # @pytest.mark.run(order=1)
    def test_materialsubstitution_selectParentNumber(self, login_to_materialsubstitution):
        driver = login_to_materialsubstitution  # WebDriver 实例
        material = MaterialDataPage(driver)  # 用 driver 初始化 MaterialDataPage
        material.wait_for_loading_to_disappear()
        material.click_button('//div[@id="g7yqlm5y-a4w0"]//input')
        material.click_button('(//div[@class="el-scrollbar"])[last()]//div[@class="my-list-item"]')
        material.click_select_button()
        name = material.get_find_element_xpath('//div[@id="g7yqlm5y-a4w0"]//input').get_attribute("value")

        eles = material.loop_judgment('//table[@class="vxe-table--body"]//tr/td[5]')
        assert all(name == ele for ele in eles)
        assert not material.has_fail_message()

    @allure.story("查询被替代子项料号成功")
    # @pytest.mark.run(order=1)
    def test_materialsubstitution_selectReplacedSub(self, login_to_materialsubstitution):
        driver = login_to_materialsubstitution  # WebDriver 实例
        material = MaterialDataPage(driver)  # 用 driver 初始化 MaterialDataPage
        material.wait_for_loading_to_disappear()
        material.click_button('//div[@id="53txfv56-a74l"]//input')
        material.click_button('(//div[@class="el-scrollbar"])[last()]//div[@class="my-list-item"]')
        material.click_select_button()
        name = material.get_find_element_xpath('//div[@id="53txfv56-a74l"]//input').get_attribute("value")

        eles = material.loop_judgment('//table[@class="vxe-table--body"]//tr/td[7]')
        assert all(name == ele for ele in eles)
        assert not material.has_fail_message()

    @allure.story("查询替代后子项料号成功")
    # @pytest.mark.run(order=1)
    def test_materialsubstitution_selectSubstituteSub(self, login_to_materialsubstitution):
        driver = login_to_materialsubstitution  # WebDriver 实例
        material = MaterialDataPage(driver)  # 用 driver 初始化 MaterialDataPage
        material.wait_for_loading_to_disappear()
        material.click_button('//div[@id="8dsqasad-wy1m"]//input')
        material.click_button('(//div[@class="el-scrollbar"])[last()]//div[@class="my-list-item"]')
        material.click_select_button()
        name = material.get_find_element_xpath('//div[@id="8dsqasad-wy1m"]//input').get_attribute("value")

        eles = material.loop_judgment('//table[@class="vxe-table--body"]//tr/td[10]')
        assert all(name == ele for ele in eles)
        assert not material.has_fail_message()

    @allure.story("查询替代类别和父料号和被替代子项料号成功")
    # @pytest.mark.run(order=1)
    def test_materialsubstitution_selectand(self, login_to_materialsubstitution):
        driver = login_to_materialsubstitution  # WebDriver 实例
        material = MaterialDataPage(driver)  # 用 driver 初始化 MaterialDataPage
        material.wait_for_loading_to_disappear()
        material.click_button('//div[@id="g7yqlm5y-a4w0"]//input')
        material.click_button('(//div[@class="el-scrollbar"])[last()]//div[@class="my-list-item"]')
        material.click_button('//div[@id="53txfv56-a74l"]//input')
        material.click_button('(//div[@class="el-scrollbar"])[last()]//div[@class="my-list-item"]')
        material.click_select_button()
        name1 = material.get_find_element_xpath('//div[@id="g7yqlm5y-a4w0"]//input').get_attribute("value")
        name2 = material.get_find_element_xpath('//div[@id="53txfv56-a74l"]//input').get_attribute("value")

        eles1 = material.loop_judgment('//table[@class="vxe-table--body"]//tr/td[5]')
        eles2 = material.loop_judgment('//table[@class="vxe-table--body"]//tr/td[7]')
        assert all(name1 == ele for ele in eles1) and all(name2 == ele for ele in eles2)
        assert not material.has_fail_message()
