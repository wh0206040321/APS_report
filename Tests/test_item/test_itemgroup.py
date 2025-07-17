import random
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

from Pages.item_page import ItemPage
from Pages.login_page import LoginPage
from Utils.data_driven import DateDriver
from Utils.driver_manager import create_driver, safe_quit, all_driver_instances


@pytest.fixture  # (scope="class")这个参数表示整个测试类共用同一个浏览器，默认一个用例执行一次
def login_to_itemgroup():
    """初始化并返回 driver"""
    driver_path = DateDriver().driver_path
    driver = create_driver(driver_path)
    driver.implicitly_wait(3)

    # 初始化登录页面
    page = LoginPage(driver)  # 初始化登录页面
    page.navigate_to(DateDriver().url)  # 导航到登录页面
    page.login(DateDriver().username, DateDriver().password, DateDriver().planning)
    page.click_button('(//span[text()="计划管理"])[1]')  # 点击计划管理
    page.click_button('(//span[text()="计划基础数据"])[1]')  # 点击计划基础数据
    page.click_button('(//span[text()="物品组"])[1]')  # 点击物品组
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("物料组表测试用例")
@pytest.mark.run(order=5)
class TestItemGroupPage:
    @allure.story("添加物料组信息 不填写数据点击确认 不允许提交，添加测试布局")
    # @pytest.mark.run(order=1)
    def test_itemgroup_addfail(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        layout = "测试布局A"
        item.add_layout()
        item.enter_texts(
            '//div[text()="当前布局:"]/following-sibling::div//input', f"{layout}"
        )
        checkbox1 = item.get_find_element_xpath(
            '//div[text()="是否默认启动:"]/following-sibling::label/span'
        )

        # 检查复选框是否未被选中
        if checkbox1.get_attribute("class") == "ivu-checkbox":
            # 如果未选中，则点击复选框进行选中
            item.click_button(
                '//div[text()="是否默认启动:"]/following-sibling::label/span'
            )
        sleep(1)

        item.click_button('(//div[text()=" 显示设置 "])[1]')
        # 获取是否可见选项的复选框元素
        checkbox2 = item.get_find_element_xpath(
            '(//div[./div[text()="是否可见:"]])[1]/label/span'
        )
        # 检查复选框是否未被选中
        if checkbox2.get_attribute("class") == "ivu-checkbox":
            # 如果未选中，则点击复选框进行选中
            item.click_button('(//div[./div[text()="是否可见:"]])[1]/label/span')
            # 点击确定按钮保存设置
            item.click_button('(//div[@class="demo-drawer-footer"])[3]/button[2]')
        else:
            # 如果已选中，直接点击确定按钮保存设置
            item.click_button('(//div[@class="demo-drawer-footer"])[3]/button[2]')
        # 获取布局名称的文本元素
        name = item.get_find_element_xpath(
                f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
            ).text
        item.click_add_button()
        # 物料组代码xpath
        input_box = item.get_find_element_xpath(
            '(//label[text()="物料组代码"])[1]/parent::div//input'
        )
        # 物料组名称xpath
        inputname_box = item.get_find_element_xpath(
            '(//label[text()="物料组名称"])[1]/parent::div//input'
        )
        item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        border_color = input_box.value_of_css_property("border-color")
        bordername_color = inputname_box.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert (
            border_color == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{border_color}"
        assert (
            bordername_color == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{border_color}"
        assert layout == name
        assert not item.has_fail_message()

    @allure.story("添加物料组信息，只填写物料代码，不填写物料名称，不允许提交")
    # @pytest.mark.run(order=2)
    def test_itemgroup_addcodefail(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        item.click_add_button()
        item.enter_texts(
            '(//label[text()="物料组代码"])[1]/parent::div//input', "text1231"
        )
        item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        input_box = item.get_find_element_xpath(
            '(//label[text()="物料组名称"])[1]/parent::div//input'
        )
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        border_color = input_box.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert (
            border_color == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{border_color}"
        assert not item.has_fail_message()

    @allure.story("添加物料组信息，只填写物料名称，不填写物料代码，不允许提交")
    # @pytest.mark.run(order=3)
    def test_itemgroup_addnamefail(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        item.click_add_button()
        item.enter_texts(
            '(//label[text()="物料组名称"])[1]/parent::div//input', "text1231"
        )

        # 点击确定
        item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        input_box = item.get_find_element_xpath(
            '(//label[text()="物料组代码"])[1]/parent::div//input'
        )
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        border_color = input_box.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert (
            border_color == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{border_color}"
        assert not item.has_fail_message()

    @allure.story("数字文本框 只允许填写数字")
    # @pytest.mark.run(order=1)
    def test_itemgroup_addnum(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage
        item.click_add_button()  # 检查点击添加
        ele = item.get_find_element_xpath(
            '(//label[text()="物料优先度"])[1]/parent::div//input'
        )
        ele.send_keys(Keys.CONTROL, "a")
        ele.send_keys(Keys.DELETE)
        # 物料优先度框输入文字字母符号数字
        item.enter_texts(
            '(//label[text()="物料优先度"])[1]/parent::div//input', "1文字abc。+=？~1_2+3"
        )
        sleep(1)
        # 获取物料优先度
        itemnum = item.get_find_element_xpath(
            '(//label[text()="物料优先度"])[1]/parent::div//input'
        ).get_attribute("value")
        assert itemnum == "1123", f"预期{itemnum}"
        assert not item.has_fail_message()

    @allure.story("下拉框选择成功")
    # @pytest.mark.run(order=1)
    def test_itemgroup_addsel(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage
        item.click_add_button()  # 检查点击添加
        # 自动补充标志下拉框
        item.click_button(
            '(//label[text()="自动补充标志"])[1]/parent::div//input[@class="ivu-select-input"]'
        )
        # 自动补充标志选择是(是库存+1对1制造)
        item.click_button('//li[text()="是(库存+1对1制造)"]')
        # 获取自动补充标志下拉框
        itemsel = item.get_find_element_xpath(
            '(//label[text()="自动补充标志"])[1]/parent::div//input['
            '@class="ivu-select-input"]'
        ).get_attribute("value")
        assert itemsel == "是(库存+1对1制造)", f"预期{itemsel}"
        assert not item.has_fail_message()

    @allure.story("代码设计器选择成功，并且没有乱码")
    # @pytest.mark.run(order=1)
    def test_itemgroup_addcodebox(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        item.click_add_button()  # 检查点击添加
        # 点击代码设计器
        item.click_button('(//label[text()="关联条件"])[1]/parent::div//i')
        # 点击标准登录
        item.click_button('(//div[text()=" 标准登录 "])[1]')
        # 首先，定位到你想要双击的元素
        element_to_double_click = driver.find_element(
            By.XPATH, '(//span[text()="订单规格1相等"])[1]'
        )
        # 创建一个 ActionChains 对象
        actions = ActionChains(driver)
        # 双击命令
        actions.double_click(element_to_double_click).perform()
        # 点击确认
        item.click_button('(//button[@class="ivu-btn ivu-btn-primary"])[5]')
        # 获取代码设计器文本框
        sleep(1)
        itemcode = item.get_find_element_xpath(
            '(//label[text()="关联条件"])[1]/parent::div//input'
        ).get_attribute("value")
        assert itemcode == "ME.Order.Spec1==OTHER.Order.Spec1", f"预期{itemcode}"
        assert not item.has_fail_message()

    @allure.story("添加数据成功")
    # @pytest.mark.run(order=1)
    def test_itemgroup_addsuccess(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        item.click_add_button()  # 检查点击添加
        # 输入物料组代码
        item.enter_texts('(//label[text()="物料组代码"])[1]/parent::div//input', "111")
        item.enter_texts('(//label[text()="物料组名称"])[1]/parent::div//input', "111")
        ele = item.get_find_element_xpath(
            '(//label[text()="物料优先度"])[1]/parent::div//input'
        )
        ele.send_keys(Keys.CONTROL, "a")
        ele.send_keys(Keys.DELETE)
        # 点击确定
        item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        adddata = item.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="111"]]]/td[2]'
        ).text
        assert adddata == "111", f"预期数据是111，实际得到{adddata}"
        assert not item.has_fail_message()

    @allure.story("添加数据重复")
    # @pytest.mark.run(order=1)
    def test_itemgroup_addrepeat(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        item.click_add_button()  # 检查点击添加
        # 输入物料组代码
        item.enter_texts('(//label[text()="物料组代码"])[1]/parent::div//input', "111")
        item.enter_texts('(//label[text()="物料组名称"])[1]/parent::div//input', "111")
        # 点击确定
        item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 获取重复弹窗文字
        error_popup = item.get_find_element_xpath(
            '//div[text()=" 记录已存在,请检查！ "]'
        ).text
        assert (
            error_popup == "记录已存在,请检查！"
        ), f"预期数据是记录已存在,请检查，实际得到{error_popup}"
        assert not item.has_fail_message()

    @allure.story("取消删除数据")
    # @pytest.mark.run(order=1)
    def test_itemgroup_delcancel(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        # 定位内容为‘111’的行
        item.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
        item.click_del_button()  # 点击删除
        sleep(1)
        # 点击取消
        item.click_button('//button[@class="ivu-btn ivu-btn-text"]')
        sleep(1)
        # 定位内容为‘111’的行
        itemdata = item.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="111"]]]/td[2]'
        ).text
        assert itemdata == "111", f"预期{itemdata}"
        assert not item.has_fail_message()

    @allure.story("添加测试数据")
    # @pytest.mark.run(order=1)
    def test_itemgroup_addsuccess1(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        item.click_add_button()  # 检查点击添加
        # 输入物料组代码
        item.enter_texts('(//label[text()="物料组代码"])[1]/parent::div//input', "1测试A")
        item.enter_texts('(//label[text()="物料组名称"])[1]/parent::div//input', "1测试A")
        # 点击确定
        item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        adddata = item.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="1测试A"]]]/td[2]'
        ).text
        assert adddata == "1测试A", f"预期数据是1测试A，实际得到{adddata}"
        assert not item.has_fail_message()

    @allure.story("修改物料组代码重复")
    # @pytest.mark.run(order=1)
    def test_itemgroup_editrepeat(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        # 选中1测试A物料组代码
        item.click_button('//tr[./td[2][.//span[text()="1测试A"]]]/td[2]')
        # 点击修改按钮
        item.click_edi_button()
        # 物料组代码输入111
        item.enter_texts('(//label[text()="物料组代码"])[1]/parent::div//input', "111")
        # 点击确定
        item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 获取重复弹窗文字
        error_popup = item.get_find_element_xpath(
            '//div[text()=" 记录已存在,请检查！ "]'
        ).text
        assert error_popup == "记录已存在,请检查！", f"预期数据{error_popup}"
        assert not item.has_fail_message()

    @allure.story("修改物料组代码成功")
    # @pytest.mark.run(order=1)
    def test_itemgroup_editcodesuccess(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        # 选中1测试A物料组代码
        item.click_button('//tr[./td[2][.//span[text()="1测试A"]]]/td[2]')
        # 点击修改按钮
        item.click_edi_button()
        sleep(1)
        # 生成随机数
        random_int = random.randint(1, 10)
        text = "1测试A" + f"{random_int}"
        # 物料组代码输入
        item.enter_texts(
            '(//label[text()="物料组代码"])[1]/parent::div//input', f"{text}"
        )
        # 点击确定
        item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 定位表格内容
        itemdata = item.get_find_element_xpath(
            '//tr[./td[2][.//span[contains(text(),"1测试A")]]]/td[2]'
        ).text
        assert itemdata == text, f"预期{itemdata}"
        assert not item.has_fail_message()

    @allure.story("把修改后的物料组代码改回来")
    # @pytest.mark.run(order=1)
    def test_itemgroup_editcodesuccess2(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        # 选中1测试A物料组代码
        item.click_button('//tr[./td[2][.//span[contains(text(),"1测试A")]]]/td[2]')
        # 点击修改按钮
        item.click_edi_button()
        # 物料组代码输入
        item.enter_texts('(//label[text()="物料组代码"])[1]/parent::div//input', "1测试A")
        # 点击确定
        item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 定位表格内容
        itemdata = item.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="1测试A"]]]/td[2]'
        ).text
        assert itemdata == "1测试A", f"预期{itemdata}"
        assert not item.has_fail_message()

    @allure.story("修改物料组名称，自动补充标识，关联条件成功")
    # @pytest.mark.run(order=1)
    def test_itemgroup_editnamesuccess(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        # 选中物料组代码
        item.click_button('//tr[./td[2][.//span[text()="1测试A"]]]/td[2]')
        # 点击修改按钮
        item.click_edi_button()
        sleep(1)
        # 生成随机数
        random_int = random.randint(1, 10)
        text = "1测试A" + f"{random_int}"
        # 输入修改的物料组名称
        item.enter_texts(
            '(//label[text()="物料组名称"])[1]/parent::div//input', f"{text}"
        )
        # 获取修改好的值
        editname = item.get_find_element_xpath(
            '(//label[text()="物料组名称"])[1]/parent::div//input'
        ).get_attribute("value")

        # 修改自动补充标识 自动补充标志下拉框
        item.click_button(
            '(//label[text()="自动补充标志"])[1]/parent::div//input[@class="ivu-select-input"]'
        )
        # 自动补充标志选择是(是库存+1对1制造)
        item.click_button('//li[text()="是(库存+1对1制造)"]')
        # 获取自动补充标志下拉框的值
        itemsel = item.get_find_element_xpath(
            '(//label[text()="自动补充标志"])[1]/parent::div//input[@class="ivu-select-input"]'
        ).get_attribute("value")

        # 修改关联条件 点击代码设计器
        item.click_button('(//label[text()="关联条件"])[1]/parent::div//i')
        # 点击标准登录
        item.click_button('(//div[text()=" 标准登录 "])[1]')
        # 首先，定位到你想要双击的元素
        element_to_double_click = driver.find_element(
            By.XPATH, '(//span[text()="订单规格1相等"])[1]'
        )
        # 创建一个 ActionChains 对象
        actions = ActionChains(driver)
        # 双击命令
        actions.double_click(element_to_double_click).perform()
        # 点击确认
        item.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )
        # 获取代码设计器文本框
        sleep(1)
        itemcode = item.get_find_element_xpath(
            '(//label[text()="关联条件"])[1]/parent::div//input'
        ).get_attribute("value")
        # 点击确定
        item.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(1)
        # 定位表格内容
        itemname = item.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="1测试A"]]]/td[3]/div'
        ).text
        itemautoGenerateFlag = item.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="1测试A"]]]/td[8]/div'
        ).text
        sleep(1)
        itempeggingConditionExpr = item.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="1测试A"]]]/td[10]/div'
        ).text
        assert (
            itemname == editname
            and itemautoGenerateFlag == itemsel
            and itempeggingConditionExpr == itemcode
        )
        assert not item.has_fail_message()

    @allure.story("刷新成功")
    # @pytest.mark.run(order=1)
    def test_itemgroup_refreshsuccess(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        # 物料代码筛选框输入123
        item.enter_texts(
            '//p[text()="物料组代码"]/ancestor::div[2]//input', "123"
        )
        item.click_ref_button()
        itemtext = item.get_find_element_xpath(
            '//p[text()="物料组代码"]/ancestor::div[2]//input'
        ).text
        assert itemtext == "", f"预期{itemtext}"
        assert not item.has_fail_message()

    @allure.story("查询物料组代码成功")
    # @pytest.mark.run(order=1)
    def test_itemgroup_selectcodesuccess(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        # 点击查询
        item.click_sel_button()
        sleep(1)
        # 定位名称输入框
        element_to_double_click = driver.find_element(
            By.XPATH,
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[4]',
        )
        # 创建一个 ActionChains 对象
        actions = ActionChains(driver)
        # 双击命令
        actions.double_click(element_to_double_click).perform()
        sleep(1)
        # 点击物料代码
        item.click_button('//div[text()="物料组代码" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        item.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        item.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "1测试A",
        )
        sleep(1)

        # 点击确认
        item.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行是否为1测试A
        itemcode = item.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]'
        ).text
        # 定位第二行没有数据
        itemcode2 = driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][2]/td[2]',
        )
        assert itemcode == "1测试A" and len(itemcode2) == 0
        assert not item.has_fail_message()

    @allure.story("没有数据时显示正常")
    # @pytest.mark.run(order=1)
    def test_itemgroup_selectnodatasuccess(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        # 点击查询
        item.click_sel_button()
        sleep(1)
        # 定位名称输入框
        element_to_double_click = driver.find_element(
            By.XPATH,
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[4]',
        )
        # 创建一个 ActionChains 对象
        actions = ActionChains(driver)
        # 双击命令
        actions.double_click(element_to_double_click).perform()
        sleep(1)
        # 点击物料代码
        item.click_button('//div[text()="物料组代码" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        item.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        item.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "没有数据",
        )
        sleep(1)

        # 点击确认
        item.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        itemcode = driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]',
        )
        assert len(itemcode) == 0
        assert not item.has_fail_message()

    @allure.story("查询物料组名字成功")
    # @pytest.mark.run(order=1)
    def test_itemgroup_selectnamesuccess(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        # 点击查询
        item.click_sel_button()
        sleep(1)
        # 定位名称输入框
        element_to_double_click = driver.find_element(
            By.XPATH,
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[4]',
        )
        # 创建一个 ActionChains 对象
        actions = ActionChains(driver)
        # 双击命令
        actions.double_click(element_to_double_click).perform()
        sleep(1)
        # 点击物料名称
        item.click_button('//div[text()="物料组名称" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        item.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        item.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "A类",
        )
        sleep(1)

        # 点击确认
        item.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行是否为M1
        itemcode = item.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[3]'
        ).text
        assert "A类" == itemcode
        assert not item.has_fail_message()

    @allure.story("查询物料优先度>0")
    # @pytest.mark.run(order=1)
    def test_itemgroupselectsuccess1(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        # 点击查询
        item.click_sel_button()
        sleep(1)
        # 定位名称输入框
        element_to_double_click = driver.find_element(
            By.XPATH,
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[4]',
        )
        # 创建一个 ActionChains 对象
        actions = ActionChains(driver)
        # 双击命令
        actions.double_click(element_to_double_click).perform()
        sleep(1)
        # 点击物料优先度
        item.click_button('//div[text()="物料优先度" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        item.click_button('//div[text()=">" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        item.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "0",
        )
        sleep(1)

        # 点击确认
        item.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行物料优先度
        itemcode = item.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][1]/td[6]'
        ).text
        # 定位第二行数据
        itemcode2 = item.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][2]/td[6]'
        ).text
        assert int(itemcode) > 0 and int(itemcode2) > 0
        assert not item.has_fail_message()

    @allure.story("查询物料组名称包含A并且物料优先度>0")
    # @pytest.mark.run(order=1)
    def test_itemgroup_selectsuccess2(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        # 点击查询
        item.click_sel_button()
        sleep(1)

        # 定位名称输入框
        element_to_double_click = driver.find_element(
            By.XPATH,
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[4]',
        )
        # 创建一个 ActionChains 对象
        actions = ActionChains(driver)
        # 双击命令
        actions.double_click(element_to_double_click).perform()
        sleep(1)
        # 点击物料名称
        item.click_button('//div[text()="物料组名称" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击（
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[3]'
        )
        item.click_button('//div[text()="(" and contains(@optid,"opt_")]')
        # 点击比较关系框
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击包含
        item.click_button('//div[text()="包含" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        item.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "A",
        )

        # 点击（
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[7]'
        )
        item.click_button('//div[text()=")" and contains(@optid,"opt_")]')

        double_click = driver.find_element(
            By.XPATH,
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[2]',
        )
        # 双击命令
        actions.double_click(double_click).perform()
        # 定义and元素的XPath
        and_xpath = '//div[text()="and" and contains(@optid,"opt_")]'

        try:
            # 首先尝试直接查找并点击and元素
            and_element = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, and_xpath))
            )
            and_element.click()
        except:
            # 如果直接查找失败，进入循环双击操作
            max_attempts = 5
            attempt = 0
            and_found = False

            while attempt < max_attempts and not and_found:
                try:
                    # 执行双击操作
                    actions.double_click(double_click).perform()
                    sleep(1)

                    # 再次尝试查找and元素
                    and_element = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, and_xpath))
                    )
                    and_element.click()
                    and_found = True
                except:
                    attempt += 1
                    sleep(1)

            if not and_found:
                raise Exception(f"在{max_attempts}次尝试后仍未找到并点击到'and'元素")

        # 点击（
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[3]'
        )
        item.click_button('//div[text()="(" and contains(@optid,"opt_")]')
        # 点击物料优先度
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[4]'
        )
        item.click_button('//div[text()="物料优先度" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[5]//input'
        )
        # 点击>
        item.click_button('//div[text()=">" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        item.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[6]//input',
            "0",
        )
        # 点击（
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[7]'
        )
        item.click_button('//div[text()=")" and contains(@optid,"opt_")]')

        sleep(1)

        # 点击确认
        item.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行物料优先度
        itemcode = item.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][1]/td[6]'
        ).text
        itemname = item.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][1]/td[3]'
        ).text

        itemcode2 = item.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][2]/td[6]'
        ).text
        itemname2 = item.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][2]/td[3]'
        ).text

        # 定位第三行没有数据
        itemcode3 = driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][3]/td[3]',
        )
        assert int(itemcode) > 0 and "A" in itemname and int(itemcode2) > 0 and "A" in itemname2 and len(itemcode3) == 0
        assert not item.has_fail_message()

    @allure.story("查询物料组代码包含产品A或物料优先度>0")
    # @pytest.mark.run(order=1)
    def test_itemgroup_selectsuccess3(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        # 点击查询
        item.click_sel_button()
        sleep(1)

        # 定位名称输入框
        element_to_double_click = driver.find_element(
            By.XPATH,
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[4]',
        )
        # 创建一个 ActionChains 对象
        actions = ActionChains(driver)
        # 双击命令
        actions.double_click(element_to_double_click).perform()
        sleep(1)
        # 点击物料名称
        item.click_button('//div[text()="物料组代码" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击（
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[3]'
        )
        item.click_button('//div[text()="(" and contains(@optid,"opt_")]')
        # 点击比较关系框
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击包含
        item.click_button('//div[text()="包含" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        item.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "产品A",
        )

        # 点击（
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[7]'
        )
        item.click_button('//div[text()=")" and contains(@optid,"opt_")]')

        sleep(1)
        double_click = driver.find_element(
            By.XPATH,
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[2]',
        )
        # 双击命令
        sleep(1)
        actions.double_click(double_click).perform()
        # 定义or元素的XPath
        or_xpath = '//div[text()="or" and contains(@optid,"opt_")]'

        try:
            # 首先尝试直接查找并点击or元素
            and_element = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, or_xpath))
            )
            and_element.click()
        except:
            # 如果直接查找失败，进入循环双击操作
            max_attempts = 5
            attempt = 0
            or_found = False

            while attempt < max_attempts and not or_found:
                try:
                    # 执行双击操作
                    actions.double_click(double_click).perform()
                    sleep(1)

                    # 再次尝试查找or元素
                    or_element = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, or_xpath))
                    )
                    or_element.click()
                    or_found = True
                except:
                    attempt += 1
                    sleep(1)

            if not or_found:
                raise Exception(f"在{max_attempts}次尝试后仍未找到并点击到'or'元素")

        # 点击（
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[3]'
        )
        item.click_button('//div[text()="(" and contains(@optid,"opt_")]')
        # 点击物料优先度
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[4]'
        )
        item.click_button('//div[text()="物料优先度" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[5]//input'
        )
        # 点击>
        item.click_button('//div[text()=">" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值0
        item.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[6]//input',
            "0",
        )
        # 点击（
        item.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[7]'
        )
        item.click_button('//div[text()=")" and contains(@optid,"opt_")]')

        sleep(1)

        # 点击确认
        item.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行物料优先度
        itemcode = item.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][1]/td[6]'
        ).text
        itemname = item.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][1]/td[2]'
        ).text
        code = item.get_find_element_xpath(
            '//tr[./td[2]//span[text()="产品A"]]//td[6]'
        ).text
        assert int(code) <= 0 and int(itemcode) > 0 and itemname == "1测试A"
        assert not item.has_fail_message()

    @allure.story("删除数据成功")
    # @pytest.mark.run(order=1)
    def test_itemgroup_delsuccess(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        # 定位内容为‘111’的行
        item.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
        item.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        parent = item.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        item.click_ref_button()
        sleep(1)
        # 定位内容为‘111’的行
        itemdata = driver.find_elements(
            By.XPATH, '//tr[./td[2][.//span[text()="111"]]]/td[2]'
        )
        assert len(itemdata) == 0
        assert not item.has_fail_message()

    @allure.story("删除测试数据成功，删除布局成功")
    # @pytest.mark.run(order=1)
    def test_itemgroup_delsuccess1(self, login_to_itemgroup):
        driver = login_to_itemgroup  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage
        layout = "测试布局A"

        # 定位内容为‘1测试A’的行
        item.click_button('//tr[./td[2][.//span[text()="1测试A"]]]/td[2]')
        item.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        parent = item.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        item.click_ref_button()
        sleep(1)
        # 定位内容为‘1测试A’的行
        itemdata = driver.find_elements(
            By.XPATH, '//tr[./td[2][.//span[text()="1测试A"]]]/td[2]'
        )

        # 获取目标 div 元素，这里的目标是具有特定文本的 div
        target_div = item.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        )

        # 获取父容器下所有 div
        # 这一步是为了确定目标 div 在其父容器中的位置
        parent_div = item.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon" and ./div[text()=" {layout} "]]'
        )
        all_children = parent_div.find_elements(By.XPATH, "./div")

        # 获取目标 div 的位置索引（从0开始）
        # 这里是为了后续操作，比如点击目标 div 相关的按钮
        index = all_children.index(target_div)
        print(f"目标 div 是第 {index + 1} 个 div")  # 输出 3（如果从0开始则是2）

        item.click_button(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]//i'
        )
        # 根据目标 div 的位置，点击对应的“删除布局”按钮
        item.click_button(f'(//li[text()="删除布局"])[{index + 1}]')
        sleep(2)
        # 点击确认删除的按钮
        item.click_button('//button[@class="ivu-btn ivu-btn-primary ivu-btn-large"]')
        # 等待一段时间，确保删除操作完成
        sleep(1)

        # 再次查找页面上是否有目标 div，以验证是否删除成功
        after_layout = driver.find_elements(
            By.XPATH, f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        )
        assert len(itemdata) == 0 == len(after_layout)
        assert not item.has_fail_message()
