import random
from time import sleep

import allure
import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.itemsPage.login_page import LoginPage
from Pages.itemsPage.order_page import OrderPage
from Utils.data_driven import DateDriver
from Utils.driver_manager import create_driver, safe_quit


@pytest.fixture  # (scope="class")这个参数表示整个测试类共用同一个浏览器，默认一个用例执行一次
def login_to_order():
    """初始化并返回 driver"""
    driver_path = DateDriver().driver_path
    driver = create_driver(driver_path)
    driver.implicitly_wait(3)

    # 初始化登录页面
    page = LoginPage(driver)  # 初始化登录页面
    page.navigate_to(DateDriver().url)  # 导航到登录页面
    page.login(DateDriver().username, DateDriver().password, DateDriver().planning)
    page.click_button('(//span[text()="计划管理"])[1]')  # 点击计划管理
    page.click_button('(//span[text()="计划业务数据"])[1]')  # 点击计划业务数据
    page.click_button('(//span[text()="制造订单"])[1]')  # 点击制造订单
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("制造订单表测试用例")
@pytest.mark.run(order=15)
class TestOrderPage:
    @allure.story("添加制造订单信息 不填写数据点击确认 不允许提交 并且添加了一新布局设置成默认启动布局")
    # @pytest.mark.run(order=1)
    def test_order_addfail(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        layout = "测试布局A"
        order.add_layout(layout)
        # 获取布局名称的文本元素
        name = order.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        ).text

        sleep(2)
        order.click_add_button()
        # 制造订单代码xpath
        input_box = order.get_find_element_xpath(
            '(//label[text()="订单代码"])[1]/parent::div//input'
        )
        # 物品代码输入框
        inputitem_box = order.get_find_element_xpath(
            '(//label[text()="物料"])[1]/parent::div//input'
        )
        # 交货期输入框
        inputdate_box = order.get_find_element_xpath(
            '(//label[text()="交货期"])[1]/parent::div//input'
        )

        order.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(1)
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        border_color = input_box.value_of_css_property("border-color")
        borderitem_color = inputitem_box.value_of_css_property("border-color")
        inputdate_box = inputdate_box.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert border_color == expected_color and borderitem_color == expected_color and inputdate_box == expected_color and name == layout
        assert not order.has_fail_message()

    @allure.story("添加制造订单信息，填写制造订单和物料，不填写交货期，不允许提交，并且增加一个判断上一个用例默认启动布局是否成功")
    # @pytest.mark.run(order=2)
    def test_order_addcodefail(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        layout = "测试布局A"
        div = order.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        ).get_attribute("class")
        order.click_add_button()
        # 填写订单代码
        order.enter_texts(
            '(//label[text()="订单代码"])[1]/parent::div//input', "text1231"
        )

        # 物料
        random_int = random.randint(1, 7)
        order.click_button('//label[text()="物料"]/parent::div/div//i')
        order.click_button(
            f'//table[@style="margin-top: 0px; width: 780px; margin-left: 0px;"]/tbody/tr[{random_int}]/td[2]'
        )
        order.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        order.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )

        # 交货期输入框
        inputdate_box = order.get_find_element_xpath(
            '(//label[text()="交货期"])[1]/parent::div//input'
        )
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        border_color = inputdate_box.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        # 判断上一步默认启动该布局成功
        assert (
            border_color == expected_color and div == "tabsDivItem tabsDivActive"
        ), f"预期边框颜色为{expected_color}, 但得到{border_color}"
        assert not order.has_fail_message()

    @allure.story(
        "添加制造订单信息，只填写制造订单名称和交货期，不填写物料，不允许提交"
    )
    # @pytest.mark.run(order=3)
    def test_order_addnamefail(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        order.click_add_button()
        # 填写订单代码
        order.enter_texts(
            '(//label[text()="订单代码"])[1]/parent::div//input', "text1231"
        )

        # 填写交货期
        order.click_button('(//label[text()="交货期"])[1]/parent::div//input')
        order.click_button('(//div[@class="ivu-date-picker-cells"])[3]/span[19]')
        order.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary ivu-btn-small"])[3]'
        )

        # 点击确定
        order.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        input_box = order.get_find_element_xpath(
            '(//label[text()="物料"])[1]/parent::div//input'
        )
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        border_color = input_box.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert (
            border_color == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{border_color}"
        assert not order.has_fail_message()

    @allure.story(
        "添加制造订单信息，只填写制造订单名称和交货期和物料，不填写计划数量，不允许提交"
    )
    # @pytest.mark.run(order=3)
    def test_order_addnumfail(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        order.click_add_button()
        # 填写订单代码
        order.enter_texts(
            '(//label[text()="订单代码"])[1]/parent::div//input', "text1231"
        )

        # 物料
        random_int = random.randint(1, 7)
        order.click_button('//label[text()="物料"]/parent::div/div//i')
        order.click_button(
            f'//table[@style="margin-top: 0px; width: 780px; margin-left: 0px;"]/tbody/tr[{random_int}]/td[2]'
        )
        order.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 填写交货期
        order.click_button('(//label[text()="交货期"])[1]/parent::div//input')
        order.click_button('(//div[@class="ivu-date-picker-cells"])[3]/span[19]')
        order.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary ivu-btn-small"])[3]'
        )

        # 清除计划数量
        num = order.get_find_element_xpath(
            '(//label[text()="计划数量"])[1]/parent::div//input'
        )
        num.send_keys(Keys.CONTROL, "a")
        num.send_keys(Keys.BACK_SPACE)

        # 点击确定
        order.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(1)
        input_box = order.get_find_element_xpath(
            '(//label[text()="计划数量"])[1]/parent::div/div[1]/div'
        )
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        border_color = input_box.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert (
            border_color == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{border_color}"
        assert not order.has_fail_message()

    @allure.story("数字文本框 只允许填写数字")
    # @pytest.mark.run(order=1)
    def test_order_addnum(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        order.click_add_button()  # 检查点击添加

        # 计划数量数字框输入文字字母符号数字
        num = order.get_find_element_xpath(
            '(//label[text()="计划数量"])[1]/parent::div//input'
        )
        num.send_keys(Keys.CONTROL, "a")
        num.send_keys(Keys.BACK_SPACE)
        order.enter_texts(
            '(//label[text()="计划数量"])[1]/parent::div//input', "1文字abc。？~1_2+=3"
        )

        # 获取计划数量数字框
        ordernum = order.get_find_element_xpath(
            '(//label[text()="计划数量"])[1]/parent::div//input'
        ).get_attribute("value")
        assert ordernum == "1123", f"预期{ordernum}"
        assert not order.has_fail_message()

    @allure.story("下拉框选择成功")
    # @pytest.mark.run(order=1)
    def test_order_addsel(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        order.click_add_button()  # 检查点击添加

        # 订单区分下拉框
        order.click_button(
            '(//label[text()="订单区分"])[1]/parent::div//input[@class="ivu-select-input"]'
        )
        # 订单区分选择 补充
        order.click_button('//li[text()="补充"]')
        # 获取下拉框
        ordersel = order.get_find_element_xpath(
            '(//label[text()="订单区分"])[1]/parent::div//input['
            '@class="ivu-select-input"]'
        ).get_attribute("value")
        assert ordersel == "补充", f"预期{ordersel}"
        assert not order.has_fail_message()

    @allure.story("添加数据成功")
    # @pytest.mark.run(order=1)
    def test_order_addsuccess(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        order.click_add_button()  # 检查点击添加
        # 填写订单代码
        order.enter_texts('(//label[text()="订单代码"])[1]/parent::div//input', "1A")

        # 物料
        random_int = random.randint(1, 10)
        order.click_button('//label[text()="物料"]/parent::div/div//i')
        order.click_button(
            f'//table[@style="margin-top: 0px; width: 780px; margin-left: 0px;"]/tbody/tr[{random_int}]/td[2]'
        )
        order.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 填写交货期
        order.click_button('(//label[text()="交货期"])[1]/parent::div//input')
        order.click_button('(//div[@class="ivu-date-picker-cells"])[3]/span[19]')
        order.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary ivu-btn-small"])[3]'
        )

        # 计划数量
        num = order.get_find_element_xpath(
            '(//label[text()="计划数量"])[1]/parent::div//input'
        )
        num.send_keys(Keys.CONTROL, "a")
        num.send_keys(Keys.BACK_SPACE)
        order.enter_texts('(//label[text()="计划数量"])[1]/parent::div//input', "200")

        # 点击确定
        order.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        adddata = order.get_find_element_xpath(
            '(//span[text()="1A"])[1]/ancestor::tr[1]/td[2]'
        ).text
        assert adddata == "1A"
        assert not order.has_fail_message()

    @allure.story("添加数据重复")
    # @pytest.mark.run(order=1)
    def test_order_addrepeat(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        order.click_add_button()  # 检查点击添加

        # 填写订单代码
        order.enter_texts('(//label[text()="订单代码"])[1]/parent::div//input', "1A")

        # 物料
        random_int = random.randint(1, 10)
        order.click_button('//label[text()="物料"]/parent::div/div//i')
        order.click_button(
            f'//table[@style="margin-top: 0px; width: 780px; margin-left: 0px;"]/tbody/tr[{random_int}]/td[2]'
        )
        order.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 填写交货期
        order.click_button('(//label[text()="交货期"])[1]/parent::div//input')
        order.click_button('(//div[@class="ivu-date-picker-cells"])[3]/span[19]')
        order.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary ivu-btn-small"])[3]'
        )

        # 点击确定
        order.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )

        # 获取重复弹窗文字
        error_popup = order.get_find_element_xpath(
            '//div[text()=" 记录已存在,请检查！ "]'
        ).text
        assert (
            error_popup == "记录已存在,请检查！"
        ), f"预期数据是记录已存在,请检查，实际得到{error_popup}"
        assert not order.has_fail_message()

    @allure.story("取消删除数据")
    # @pytest.mark.run(order=1)
    def test_order_delcancel(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage

        # 定位内容为‘1A’的行
        order.click_button('(//span[text()="1A"])[1]/ancestor::tr[1]/td[2]')
        order.click_del_button()  # 点击删除
        sleep(1)
        # 点击取消
        order.get_find_element_class("ivu-btn-text").click()
        sleep(1)
        # 定位内容为‘1A’的行
        orderdata = order.get_find_element_xpath(
            '(//span[text()="1A"])[1]/ancestor::tr[1]/td[2]'
        ).text
        assert orderdata == "1A", f"预期{orderdata}"
        assert not order.has_fail_message()

    @allure.story("添加测试数据成功")
    # @pytest.mark.run(order=1)
    def test_order_addsuccess1(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        order.click_add_button()  # 检查点击添加
        # 填写订单代码
        order.enter_texts('(//label[text()="订单代码"])[1]/parent::div//input', "1B")

        # 物料
        random_int = random.randint(1, 10)
        order.click_button('//label[text()="物料"]/parent::div/div//i')
        order.click_button(
            f'//table[@style="margin-top: 0px; width: 780px; margin-left: 0px;"]/tbody/tr[{random_int}]/td[2]'
        )
        order.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 填写交货期
        order.click_button('(//label[text()="交货期"])[1]/parent::div//input')
        order.click_button('(//div[@class="ivu-date-picker-cells"])[3]/span[19]')
        order.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary ivu-btn-small"])[3]'
        )

        # 点击确定
        order.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        adddata = order.get_find_element_xpath(
            '(//span[text()="1B"])[1]/ancestor::tr[1]/td[2]'
        ).text
        assert adddata == "1B"
        assert not order.has_fail_message()

    @allure.story("修改制造订单代码重复")
    # @pytest.mark.run(order=1)
    def test_order_editrepeat(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        # 选中1B制造订单代码
        order.click_button('(//span[text()="1B"])[1]/ancestor::tr[1]/td[2]')
        # 点击修改按钮
        order.click_edi_button()

        # 制造订单代码输入1A
        order.enter_texts('(//label[text()="订单代码"])[1]/parent::div//input', "1A")
        # 点击确定
        order.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        # 获取重复弹窗文字
        error_popup = order.get_find_element_xpath(
            '//div[text()=" 记录已存在,请检查！ "]'
        ).text
        assert error_popup == "记录已存在,请检查！", f"预期数据{error_popup}"
        assert not order.has_fail_message()

    @allure.story("修改制造订单代码成功")
    # @pytest.mark.run(order=1)
    def test_order_editcodesuccess(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        # 选中1A制造订单代码
        order.click_button('(//span[text()="1B"])[1]')
        # 点击修改按钮
        order.click_edi_button()

        # 生成随机数
        random_int = random.randint(1, 10)
        text = "1B" + f"{random_int}"
        sleep(1)
        # 制造订单代码输入
        order.enter_texts(
            '(//label[text()="订单代码"])[1]/parent::div//input', f"{text}"
        )
        # 点击确定
        order.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(3)
        # 定位表格内容
        orderdata = order.get_find_element_xpath(
            '(//span[contains(text(),"1B")])[1]'
        ).text
        assert orderdata == text, f"预期{orderdata}"
        assert not order.has_fail_message()

    @allure.story("把修改后的制造订单代码改回来")
    # @pytest.mark.run(order=1)
    def test_order_editcodesuccess2(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        # 选中1B制造订单代码
        order.click_button('(//span[contains(text(),"1B")])[1]')
        # 点击修改按钮
        order.click_edi_button()
        # 制造订单代码输入
        order.enter_texts('(//label[text()="订单代码"])[1]/parent::div//input', "1B")
        # 点击确定
        order.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(1)
        # 定位表格内容
        orderdata = order.get_find_element_xpath('(//span[text()="1B"])[1]').text
        assert orderdata == "1B", f"预期{orderdata}"
        assert not order.has_fail_message()

    @allure.story("修改物料名称，计划数量成功")
    # @pytest.mark.run(order=1)
    def test_order_editnamesuccess(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        # 选中制造订单代码
        order.click_button('(//span[text()="1B"])[1]')
        # 点击修改按钮
        order.click_edi_button()

        # 物料
        randomitem_int = random.randint(1, 10)
        order.click_button('//label[text()="物料"]/parent::div/div//i')
        order.click_button(
            f'//table[@style="margin-top: 0px; width: 780px; margin-left: 0px;"]/tbody/tr[{randomitem_int}]/td[2]'
        )
        order.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )
        sleep(1)
        edititem = order.get_find_element_xpath(
            '(//label[text()="物料"])[1]/parent::div//input'
        ).get_attribute("value")

        # 计划数量数字框输入文字字母符号数字
        random_int = random.randint(1, 99)
        num = order.get_find_element_xpath(
            '(//label[text()="计划数量"])[1]/parent::div//input'
        )
        num.send_keys(Keys.CONTROL, "a")
        num.send_keys(Keys.BACK_SPACE)
        order.enter_texts(
            '(//label[text()="计划数量"])[1]/parent::div//input', f"{random_int}"
        )
        editnum = order.get_find_element_xpath(
            '(//label[text()="计划数量"])[1]/parent::div//input'
        ).get_attribute("value")

        # 点击确定
        order.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(1)
        # 定位表格内容
        orderitem = order.get_find_element_xpath(
            '(//span[text()="1B"])[1]/ancestor::tr/td[5]/div'
        ).text
        ordernum = order.get_find_element_xpath(
            '(//span[text()="1B"])[1]/ancestor::tr/td[10]/div'
        ).text
        assert orderitem == edititem and ordernum == editnum
        assert not order.has_fail_message()

    @allure.story("刷新成功")
    # @pytest.mark.run(order=1)
    def test_order_refreshsuccess(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        # 制造订单代码筛选框输入123
        order.enter_texts(
            '//p[text()="订单代码"]/ancestor::div[2]//input', "123"
        )
        order.click_ref_button()
        ordertext = order.get_find_element_xpath(
            '//p[text()="订单代码"]/ancestor::div[2]//input'
        ).text
        assert ordertext == "", f"预期{ordertext}"
        assert not order.has_fail_message()

    @allure.story("查询制造订单代码成功")
    # @pytest.mark.run(order=1)
    def test_order_selectcodesuccess(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage

        # 点击查询
        order.click_sel_button()
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
        # 点击制造订单代码
        order.click_button('//div[text()="订单代码" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        order.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        order.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        order.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "1A",
        )
        sleep(1)

        # 点击确认
        order.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行是否为1A
        ordercode = order.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]'
        ).text
        # 定位第二行没有数据
        ordercode2 = driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][2]/td[2]',
        )
        assert ordercode == "1A" and len(ordercode2) == 0
        assert not order.has_fail_message()

    @allure.story("查询物料名字成功")
    # @pytest.mark.run(order=1)
    def test_order_selectnamesuccess(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        # 点击查询
        order.click_sel_button()
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
        # 点击制造订单名称
        order.click_button('//div[text()="物料" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        order.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        order.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        order.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "A",
        )
        sleep(1)

        # 点击确认
        order.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行是否为A
        orderitem = order.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[5]'
        ).text
        assert orderitem == "A"
        assert not order.has_fail_message()

    @allure.story("查询计划数量>100")
    # @pytest.mark.run(order=1)
    def test_order_selectsuccess1(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        # 点击查询
        order.click_sel_button()
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
        # 点击制造订单优先度
        order.click_button('//div[text()="计划数量" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        order.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        order.click_button('//div[text()=">" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        order.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "100",
        )
        sleep(1)

        # 点击确认
        order.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行制造订单优先度
        ordercode = order.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][1]/td[10]'
        ).text
        # 定位第二行数据
        ordercode2 = order.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][2]/td[10]'
        ).text
        assert int(ordercode) > 100 and int(ordercode2) > 100
        assert not order.has_fail_message()

    @allure.story("查询订单代码包含1A并且计划数量>100")
    # @pytest.mark.run(order=1)
    def test_order_selectsuccess2(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        # 点击查询
        order.click_sel_button()
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
        # 点击制造订单名称
        order.click_button('//div[text()="订单代码" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击（
        order.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[3]'
        )
        order.click_button('//div[text()="(" and contains(@optid,"opt_")]')
        # 点击比较关系框
        order.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击包含
        order.click_button('//div[text()="包含" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        order.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "1A",
        )

        # 点击（
        order.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[7]'
        )
        order.click_button('//div[text()=")" and contains(@optid,"opt_")]')
        sleep(1)

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
        order.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[3]'
        )
        order.click_button('//div[text()="(" and contains(@optid,"opt_")]')
        # 点击这种数量
        order.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[4]'
        )
        order.click_button('//div[text()="计划数量" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        order.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[5]//input'
        )
        # 点击>
        order.click_button('//div[text()=">" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        order.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[6]//input',
            "100",
        )
        # 点击（
        order.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[7]'
        )
        order.click_button('//div[text()=")" and contains(@optid,"opt_")]')

        sleep(1)

        # 点击确认
        order.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行计划数量
        ordercode = order.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][1]/td[10]'
        ).text
        ordername = order.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][1]/td[2]'
        ).text
        # 判断第一行计划数量>100 并且 制造订单代码为S1-产品A 并且第二行没有数据
        assert int(ordercode) > 100 and "1A" in ordername
        assert not order.has_fail_message()

    @allure.story("删除数据成功")
    # @pytest.mark.run(order=1)
    def test_order_delsuccess(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        # 定位内容为‘1A’的行
        order.click_button('(//span[text()="1A"])[1]/ancestor::tr[1]/td[2]')
        order.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        parent = order.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        sleep(1)
        # 定位内容为‘1A’的行
        orderdata = driver.find_elements(
            By.XPATH, '(//span[text()="1A"])[1]/ancestor::tr[1]/td[2]'
        )
        assert len(orderdata) == 0
        assert not order.has_fail_message()

    @allure.story("删除测试数据成功")
    # @pytest.mark.run(order=1)
    def test_order_delsuccess1(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        # 定位内容为‘1B’的行
        order.click_button('(//span[text()="1B"])[1]/ancestor::tr[1]/td[2]')
        order.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        parent = order.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        sleep(1)
        # 定位内容为‘1B’的行
        orderdata = driver.find_elements(
            By.XPATH, '(//span[text()="1B"])[1]/ancestor::tr[1]/td[2]'
        )
        assert len(orderdata) == 0
        assert not order.has_fail_message()

    @allure.story("删除布局")
    # @pytest.mark.run(order=1)
    def test_order_dellayout(self, login_to_order):
        driver = login_to_order  # WebDriver 实例
        order = OrderPage(driver)  # 用 driver 初始化 OrderPage
        layout = "测试布局A"
        # 获取目标 div 元素，这里的目标是具有特定文本的 div
        target_div = order.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        )

        # 获取父容器下所有 div
        # 这一步是为了确定目标 div 在其父容器中的位置
        parent_div = order.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon" and ./div[text()=" {layout} "]]'
        )
        all_children = parent_div.find_elements(By.XPATH, "./div")

        # 获取目标 div 的位置索引（从0开始）
        # 这里是为了后续操作，比如点击目标 div 相关的按钮
        index = all_children.index(target_div)
        print(f"目标 div 是第 {index + 1} 个 div")  # 输出 3（如果从0开始则是2）

        order.click_button(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]//i'
        )
        # 根据目标 div 的位置，点击对应的“删除布局”按钮
        order.click_button(f'(//li[text()="删除布局"])[{index + 1}]')
        # 点击确认删除的按钮
        order.click_button('//button[@class="ivu-btn ivu-btn-primary ivu-btn-large"]')
        # 等待一段时间，确保删除操作完成
        sleep(1)

        # 再次查找页面上是否有目标 div，以验证是否删除成功
        after_layout = driver.find_elements(
            By.XPATH, f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        )
        assert len(after_layout) == 0
        assert not order.has_fail_message()
