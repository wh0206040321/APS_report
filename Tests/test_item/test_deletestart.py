import random
from time import sleep

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.item_page import ItemPage
from Pages.login_page import LoginPage
from Pages.master_page import MasterPage
from Pages.operationPlan_page import operationPlanPage
from Pages.order_page import OrderPage
from Pages.plan_page import PlanPage
from Pages.previewPlan_page import PreviewPlanPage
from Pages.resource_page import ResourcePage
from Utils.data_driven import DateDriver
from Utils.shared_data_util import SharedDataUtil
from Utils.driver_manager import create_driver, safe_quit, all_driver_instances


@allure.feature("删除添加的物品，添加的工艺产能，添加的制造订单,删除工作指示测试用例")
@pytest.mark.run(order=24)
class TestDeleteStart:
    @allure.story("删除添加的物品，添加的工艺产能，添加的制造订单,删除工作指示")
    # @pytest.mark.run(order=1)
    def test_delete_start(self):
        """初始化并返回 driver"""
        driver_path = DateDriver().driver_path
        driver = create_driver(driver_path)
        driver.implicitly_wait(3)
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage


        # 初始化登录页面
        page = LoginPage(driver)  # 初始化登录页面
        page.navigate_to(DateDriver().url)  # 导航到登录页面
        page.login(DateDriver().username, DateDriver().password, DateDriver().planning)
        item.go_item()

        # 待删除的物品名称列表
        ITEMS_TO_DELETE = ["1测试A", "1测试B", "1测试C"]

        # 批量删除物品并等待
        for item_name in ITEMS_TO_DELETE:
            try:
                # 先判断是否存在该物品
                elements = driver.find_elements(
                    By.XPATH, f'//span[text()="{item_name}"]'
                )
                if not elements:
                    print(f"物品 {item_name} 不存在，跳过删除。")
                    continue

                item.delete_item(item_name)  # 确认存在后再调用删除方法
                sleep(1)
            except Exception as e:
                print(f"删除物品 {item_name} 时发生异常: {e}")

        page.click_button('(//span[text()="工艺产能"])[1]')  # 点击工艺产能
        master = MasterPage(driver)  # 用 driver 初始化 MasterPage
        sleep(1)
        master.delete_material("1测试C")

        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        page.click_button('(//span[text()="计划业务数据"])[1]')  # 点击计划业务数据
        page.click_button('(//span[text()="制造订单"])[1]')  # 点击制造订单
        code = "1测试C"
        order.delete_order(code)
        order.click_ref_button()
        sleep(1)
        ele = driver.find_elements(
            By.XPATH, f'(//span[text()="{code}"])[1]/ancestor::tr[1]/td[2]'
        )
        page.click_button('(//span[text()="计划业务数据"])[1]')  # 点击计划业务数据
        page.click_button('(//span[text()="工作指示一览"])[1]')

        previewPlan = PreviewPlanPage(driver)  # 用 previewPlan 初始化 PreviewPlanPage
        # 加载共享数据
        shared_data = SharedDataUtil.load_data()

        # 从共享数据中获取资源1和资源2
        resource1 = shared_data.get("master_res1")
        resource2 = shared_data.get("master_res2")

        # 等待2秒，以确保数据加载完成
        sleep(2)

        # 输入订单代码
        previewPlan.enter_texts(
            '//div[./p[text()="订单代码"]]/parent::div//input', "1测试C订单"
        )
        elements = driver.find_elements(By.XPATH, '//table[.//td[4]//span[text()="1测试C订单"]]//tr[1]/td[7]')
        if len(elements) == 1:
            # 获取表格中订单代码为"1测试C订单"的第一行和第二行的资源信息
            ele_resource1 = previewPlan.get_find_element_xpath(
                '//table[.//td[4]//span[text()="1测试C订单"]]//tr[1]/td[7]'
            ).text
            ele_resource2 = previewPlan.get_find_element_xpath(
                '//table[.//td[4]//span[text()="1测试C订单"]]//tr[2]/td[7]'
            ).text

            # 检查获取到的资源信息是否与共享数据中的资源信息一致
            if ele_resource1 == resource1 and ele_resource2 == resource2:
                # 如果一致，则选择第二个复选框
                sleep(2)
                previewPlan.click_button(
                    '(//span[@class="vxe-checkbox--icon vxe-icon-checkbox-unchecked"])[2]'
                )
                sleep(1)
                # 点击删除按钮，并确认删除操作
                previewPlan.click_del_button()
                previewPlan.click_button(
                    '//div[@class="ivu-modal-confirm-footer"]/button[2]'
                )

        # 等待1秒后，检查订单代码为"1测试C订单"的行是否已删除
        sleep(1)
        ele_none = driver.find_elements(
            By.XPATH, '//table[.//td[4]//span[text()="1测试C订单"]]/tbody//tr'
        )


        assert len(ele) == 0 and len(ele_none) == 0
        assert not item.has_fail_message()
