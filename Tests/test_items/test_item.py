import random
from time import sleep

import allure
import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.itemsPage.item_page import ItemPage
from Pages.itemsPage.login_page import LoginPage
from Utils.data_driven import DateDriver
from Utils.driver_manager import create_driver, safe_quit


@pytest.fixture  # (scope="class")这个参数表示整个测试类共用同一个浏览器，默认一个用例执行一次
def login_to_item():
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
    page.click_button('(//span[text()="物品"])[1]')  # 点击物品
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("物料表测试用例")
@pytest.mark.run(order=4)
class TestItemPage:
    @allure.story("添加物料信息 不填写数据点击确认 不允许提交")
    # @pytest.mark.run(order=1)
    def test_item_addfail(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage
        item.click_add_button()
        # 物料代码xpath
        input_box = item.get_find_element_xpath(
            '(//label[text()="物料代码"])[1]/parent::div//input'
        )
        # 物料名称xpath
        inputname_box = item.get_find_element_xpath(
            '(//label[text()="物料名称"])[1]/parent::div//input'
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
        assert not item.has_fail_message()

    @allure.story("添加物料信息，只填写物料代码，不填写物料名称，不允许提交")
    # @pytest.mark.run(order=2)
    def test_item_addcodefail(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        item.click_add_button()
        item.enter_texts(
            '(//label[text()="物料代码"])[1]/parent::div//input', "text1231"
        )
        item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        input_box = item.get_find_element_xpath(
            '(//label[text()="物料名称"])[1]/parent::div//input'
        )
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        border_color = input_box.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert (
            border_color == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{border_color}"
        assert not item.has_fail_message()

    @allure.story("添加物料信息，只填写物料名称，不填写物料代码，不允许提交")
    # @pytest.mark.run(order=3)
    def test_item_addnamefail(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        item.click_add_button()
        item.enter_texts(
            '(//label[text()="物料名称"])[1]/parent::div//input', "text1231"
        )

        # 点击确定
        item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        input_box = item.get_find_element_xpath(
            '(//label[text()="物料代码"])[1]/parent::div//input'
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
    def test_item_addnum(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage
        item.click_add_button()  # 检查点击添加
        # 数值特征数字框输入文字字母符号数字
        item.enter_texts(
            '(//label[text()="数值特征1"])[1]/parent::div//input', "1文字abc。？~1_2+3"
        )
        sleep(1)
        # 获取数值特征数字框
        itemnum = item.get_find_element_xpath(
            '(//label[text()="数值特征1"])[1]/parent::div//input'
        ).get_attribute("value")
        assert itemnum == "1123", f"预期{itemnum}"
        assert not item.has_fail_message()

    @allure.story("下拉框选择成功")
    # @pytest.mark.run(order=1)
    def test_item_addsel(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
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
    def test_item_addcodebox(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
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
    def test_item_addsuccess(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        item.click_add_button()  # 检查点击添加
        # 输入物料代码
        item.enter_texts('(//label[text()="物料代码"])[1]/parent::div//input', "111")
        item.enter_texts('(//label[text()="物料名称"])[1]/parent::div//input', "111")
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
    def test_item_addrepeat(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        item.click_add_button()  # 检查点击添加
        # 输入物料代码
        item.enter_texts('(//label[text()="物料代码"])[1]/parent::div//input', "111")
        item.enter_texts('(//label[text()="物料名称"])[1]/parent::div//input', "111")
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
    def test_item_delcancel(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
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
    def test_item_addsuccess1(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        item.click_add_button()  # 检查点击添加
        # 输入物料代码
        item.enter_texts('(//label[text()="物料代码"])[1]/parent::div//input', "1测试A")
        item.enter_texts('(//label[text()="物料名称"])[1]/parent::div//input', "1测试A")
        # 点击确定
        item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        adddata = item.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="1测试A"]]]/td[2]'
        ).text
        assert adddata == "1测试A", f"预期数据是1测试A，实际得到{adddata}"
        assert not item.has_fail_message()

    @allure.story("修改物料代码重复")
    # @pytest.mark.run(order=1)
    def test_item_editrepeat(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        # 选中1测试A物料代码
        item.click_button('//tr[./td[2][.//span[text()="1测试A"]]]/td[2]')
        # 点击修改按钮
        item.click_edi_button()
        # 物料代码输入111
        item.enter_texts('(//label[text()="物料代码"])[1]/parent::div//input', "111")
        # 点击确定
        item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 获取重复弹窗文字
        error_popup = item.get_find_element_xpath(
            '//div[text()=" 记录已存在,请检查！ "]'
        ).text
        assert error_popup == "记录已存在,请检查！", f"预期数据{error_popup}"
        assert not item.has_fail_message()

    @allure.story("修改物料代码成功")
    # @pytest.mark.run(order=1)
    def test_item_editcodesuccess(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage
        # 选中1测试A物料代码
        item.click_button('//tr[./td[2][.//span[text()="1测试A"]]]/td[2]')
        # 点击修改按钮
        item.click_edi_button()
        sleep(1)
        # 生成随机数
        random_int = random.randint(1, 10)
        text = "1测试A" + f"{random_int}"
        # 物料代码输入
        item.enter_texts(
            '(//label[text()="物料代码"])[1]/parent::div//input', f"{text}"
        )
        # 点击确定
        item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(3)
        # 定位表格内容
        itemdata = item.get_find_element_xpath(
            '//tr[./td[2][.//span[contains(text(),"1测试A")]]]/td[2]'
        ).text
        assert itemdata == text, f"预期{itemdata}"
        assert not item.has_fail_message()

    @allure.story("把修改后的物料代码改回来")
    # @pytest.mark.run(order=1)
    def test_item_editcodesuccess2(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        # 选中1测试A物料代码
        item.click_button('//tr[./td[2][.//span[contains(text(),"1测试A")]]]/td[2]')
        # 点击修改按钮
        item.click_edi_button()
        # 物料代码输入
        item.enter_texts('(//label[text()="物料代码"])[1]/parent::div//input', "1测试A")
        # 点击确定
        item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 定位表格内容
        itemdata = item.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="1测试A"]]]/td[2]'
        ).text
        assert itemdata == "1测试A", f"预期{itemdata}"
        assert not item.has_fail_message()

    @allure.story("修改物料名称，自动补充标识，关联条件成功")
    # @pytest.mark.run(order=1)
    def test_item_editnamesuccess(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        # 选中物料代码
        item.click_button('//tr[./td[2][.//span[text()="1测试A"]]]/td[2]')
        # 点击修改按钮
        item.click_edi_button()
        sleep(1)
        # 生成随机数
        random_int = random.randint(1, 10)
        text = "1测试A" + f"{random_int}"
        # 输入修改的物料名称
        item.enter_texts(
            '(//label[text()="物料名称"])[1]/parent::div//input', f"{text}"
        )
        # 获取修改好的值
        editname = item.get_find_element_xpath(
            '(//label[text()="物料名称"])[1]/parent::div//input'
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
    def test_item_refreshsuccess(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

        # 物料代码筛选框输入123
        item.enter_texts(
            '//p[text()="物料代码"]/ancestor::div[2]//input', "123"
        )
        item.click_ref_button()
        itemtext = item.get_find_element_xpath(
            '//p[text()="物料代码"]/ancestor::div[2]//input'
        ).text
        assert itemtext == "", f"预期{itemtext}"
        assert not item.has_fail_message()

    @allure.story("查询物料代码成功")
    # @pytest.mark.run(order=1)
    def test_item_selectcodesuccess(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
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
        item.click_button('//div[text()="物料代码" and contains(@optid,"opt_")]')
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
            "产品A",
        )
        sleep(1)

        # 点击确认
        item.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行是否为产品A
        itemcode = item.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]'
        ).text
        # 定位第二行没有数据
        itemcode2 = driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][2]/td[2]',
        )
        assert itemcode == "产品A" and len(itemcode2) == 0
        assert not item.has_fail_message()

    @allure.story("没有数据时显示正常")
    # @pytest.mark.run(order=1)
    def test_item_selectnodatasuccess(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
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
        item.click_button('//div[text()="物料代码" and contains(@optid,"opt_")]')
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

    @allure.story("查询物料名字成功")
    # @pytest.mark.run(order=1)
    def test_item_selectnamesuccess(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
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
        item.click_button('//div[text()="物料名称" and contains(@optid,"opt_")]')
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
            "M1",
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
        # 定位第二行没有数据
        itemcode2 = driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][2]/td[3]',
        )
        assert itemcode == "M1" and len(itemcode2) == 0
        assert not item.has_fail_message()

    @allure.story("查询物料优先度>60")
    # @pytest.mark.run(order=1)
    def test_item_selectsuccess1(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
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
            "60",
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
        assert int(itemcode) > 60 and int(itemcode2) > 60
        assert not item.has_fail_message()

    @allure.story("查询物料名称包含材料并且物料优先度>70")
    # @pytest.mark.run(order=1)
    def test_item_selectsuccess2(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
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
        item.click_button('//div[text()="物料名称" and contains(@optid,"opt_")]')
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
            "材料",
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
            "70",
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
        # 定位第二行没有数据
        itemcode2 = driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][2]/td[10]',
        )
        # 判断第一行物料优先度>70 并且 物料名称为材料B 并且第二行没有数据
        assert int(itemcode) > 70 and itemname == "材料B" and len(itemcode2) == 0
        assert not item.has_fail_message()

    @allure.story("查询物料名称包含材料或物料优先度>70")
    # @pytest.mark.run(order=1)
    def test_item_selectsuccess3(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
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
        item.click_button('//div[text()="物料名称" and contains(@optid,"opt_")]')
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
            "材料",
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
        # 点击输入数值70
        item.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[6]//input',
            "70",
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
        # 定位第二行数据
        itemcode2 = item.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][2]/td[3]'
        ).text
        assert "材料" in itemname and int(itemcode) < 70 and "材料" in itemcode2
        assert not item.has_fail_message()

    @allure.story("删除数据成功")
    # @pytest.mark.run(order=1)
    def test_item_delsuccess(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
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

    @allure.story("删除测试数据成功")
    # @pytest.mark.run(order=1)
    def test_item_delsuccess1(self, login_to_item):
        driver = login_to_item  # WebDriver 实例
        item = ItemPage(driver)  # 用 driver 初始化 ItemPage

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
        assert len(itemdata) == 0
        assert not item.has_fail_message()
