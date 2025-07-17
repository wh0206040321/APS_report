import random
from time import sleep

import allure
import pytest
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.spec1_page import Spec1Page
from Pages.login_page import LoginPage
from Utils.data_driven import DateDriver
from Utils.driver_manager import create_driver, safe_quit, all_driver_instances


@pytest.fixture  # (scope="class")这个参数表示整个测试类共用同一个浏览器，默认一个用例执行一次
def login_to_spec1():
    """初始化并返回 driver"""
    driver_path = DateDriver().driver_path
    driver = create_driver(driver_path)
    driver.implicitly_wait(3)

    # 初始化登录页面
    page = LoginPage(driver)  # 初始化登录页面
    page.navigate_to(DateDriver().url)  # 导航到登录页面
    page.login(DateDriver().username, DateDriver().password, DateDriver().planning)
    page.click_button('(//span[text()="计划管理"])[1]')  # 点击计划管理
    page.click_button('(//span[text()="计划生产特征"])[1]')  # 点击计划生产特征
    page.click_button('(//span[text()="生产特征1"])[1]')  # 点击生产特征1
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("生产特征表测试用例")
@pytest.mark.run(order=2)
class TestSpecPage:
    @allure.story("添加生产特征信息 不填写数据点击确认 不允许提交，添加新布局")
    # @pytest.mark.run(order=1)
    def test_spec_addfail(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page
        layout = "测试布局A"
        spec.add_layout()
        spec.enter_texts(
            '//div[text()="当前布局:"]/following-sibling::div//input', f"{layout}"
        )
        checkbox1 = spec.get_find_element_xpath(
            '//div[text()="是否默认启动:"]/following-sibling::label/span'
        )

        # 检查复选框是否未被选中
        if checkbox1.get_attribute("class") == "ivu-checkbox":
            # 如果未选中，则点击复选框进行选中
            spec.click_button(
                '//div[text()="是否默认启动:"]/following-sibling::label/span'
            )
        sleep(1)

        spec.click_button('(//div[text()=" 显示设置 "])[1]')
        # 获取是否可见选项的复选框元素
        checkbox2 = spec.get_find_element_xpath(
            '(//div[./div[text()="是否可见:"]])[1]/label/span'
        )
        # 检查复选框是否未被选中
        if checkbox2.get_attribute("class") == "ivu-checkbox":
            # 如果未选中，则点击复选框进行选中
            spec.click_button('(//div[./div[text()="是否可见:"]])[1]/label/span')
            # 点击确定按钮保存设置
            spec.click_button('(//div[@class="demo-drawer-footer"])[3]/button[2]')
        else:
            # 如果已选中，直接点击确定按钮保存设置
            spec.click_button('(//div[@class="demo-drawer-footer"])[3]/button[2]')

        spec.click_add_button()
        # 代码xpath
        input_box = spec.get_find_element_xpath(
            '(//label[text()="代码"])[1]/parent::div//input'
        )
        spec.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        border_color = input_box.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert (
            border_color == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{border_color}"
        assert not spec.has_fail_message()

    @allure.story("数字文本框 只允许填写数字")
    # @pytest.mark.run(order=1)
    def test_spec_addnum(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page
        spec.click_add_button()  # 检查点击添加
        ele = spec.get_find_element_xpath(
            '(//label[text()="显示顺序"])[1]/parent::div//input'
        )
        ele.send_keys(Keys.CONTROL, "a")
        ele.send_keys(Keys.DELETE)
        # 数值特征数字框输入文字字母符号数字
        spec.enter_texts(
            '(//label[text()="显示顺序"])[1]/parent::div//input', "1文字abc。？~1_2+=3"
        )
        sleep(1)
        # 获取显示顺序数字框
        specnum = spec.get_find_element_xpath(
            '(//label[text()="显示顺序"])[1]/parent::div//input'
        ).get_attribute("value")
        assert specnum == "1123", f"预期{specnum}"
        assert not spec.has_fail_message()

    @allure.story("下拉框选择成功")
    # @pytest.mark.run(order=1)
    def test_spec_addsel(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page
        spec.click_add_button()  # 检查点击添加
        # 显示颜色下拉框
        spec.click_button('(//label[text()="显示颜色"])[1]/parent::div//i')
        # 显示颜色
        spec.click_button('//span[text()="RGB(100,255,178)"]')
        # 获取下拉框数据
        specsel = spec.get_find_element_xpath(
            '(//label[text()="显示颜色"])[1]/parent::div//input['
            '@class="ivu-select-input"]'
        ).get_attribute("value")
        assert specsel == "2", f"预期{specsel}"
        assert not spec.has_fail_message()

    @allure.story("添加数据成功")
    # @pytest.mark.run(order=1)
    def test_spec_addsuccess(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page

        spec.click_add_button()  # 检查点击添加
        # 输入代码
        spec.enter_texts('(//label[text()="代码"])[1]/parent::div//input', "111")
        spec.enter_texts('(//label[text()="名称"])[1]/parent::div//input', "111")
        # 点击确定
        spec.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        adddata = spec.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="111"]]]/td[2]'
        ).text
        assert adddata == "111", f"预期数据是111，实际得到{adddata}"
        assert not spec.has_fail_message()

    @allure.story("添加数据重复")
    # @pytest.mark.run(order=1)
    def test_spec_addrepeat(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page

        spec.click_add_button()  # 检查点击添加
        # 输入代码
        spec.enter_texts('(//label[text()="代码"])[1]/parent::div//input', "111")
        spec.enter_texts('(//label[text()="名称"])[1]/parent::div//input', "111")
        # 点击确定
        spec.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 获取重复弹窗文字
        error_popup = spec.get_find_element_xpath(
            '//div[text()=" 记录已存在,请检查！ "]'
        ).text
        assert (
            error_popup == "记录已存在,请检查！"
        ), f"预期数据是记录已存在,请检查，实际得到{error_popup}"
        assert not spec.has_fail_message()

    @allure.story("取消删除数据")
    # @pytest.mark.run(order=1)
    def test_spec_delcancel(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page

        # 定位内容为‘111’的行
        spec.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
        spec.click_del_button()  # 点击删除
        sleep(1)
        # 点击取消
        spec.click_button('//button[@class="ivu-btn ivu-btn-text"]')
        sleep(1)
        # 定位内容为‘111’的行
        itemdata = spec.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="111"]]]/td[2]'
        ).text
        assert itemdata == "111", f"预期{itemdata}"
        assert not spec.has_fail_message()

    @allure.story("添加测试数据")
    # @pytest.mark.run(order=1)
    def test_spec_addsuccess1(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page

        spec.click_add_button()  # 检查点击添加
        # 输入代码
        spec.enter_texts('(//label[text()="代码"])[1]/parent::div//input', "1测试A")
        spec.enter_texts('(//label[text()="名称"])[1]/parent::div//input', "1测试A")
        # 显示颜色下拉框
        spec.click_button('(//label[text()="显示颜色"])[1]/parent::div//i')
        # 显示颜色
        spec.click_button('//span[text()="RGB(100,255,178)"]')
        ele = spec.get_find_element_xpath(
            '(//label[text()="显示顺序"])[1]/parent::div//input'
        )
        ele.send_keys(Keys.CONTROL, "a")
        ele.send_keys(Keys.DELETE)
        # 显示顺序框输入文字字母符号数字
        spec.enter_texts(
            '(//label[text()="显示顺序"])[1]/parent::div//input', "20"
        )
        # 点击确定
        spec.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        adddata = spec.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="1测试A"]]]/td[2]'
        ).text
        assert adddata == "1测试A", f"预期数据是1测试A，实际得到{adddata}"
        assert not spec.has_fail_message()

    @allure.story("修改代码重复")
    # @pytest.mark.run(order=1)
    def test_spec_editrepeat(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page

        # 选中1测试A物料代码
        spec.click_button('//tr[./td[2][.//span[text()="1测试A"]]]/td[2]')
        # 点击修改按钮
        spec.click_edi_button()
        # 物料代码输入111
        spec.enter_texts('(//label[text()="代码"])[1]/parent::div//input', "111")
        # 点击确定
        spec.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 获取重复弹窗文字
        error_popup = spec.get_find_element_xpath(
            '//div[text()=" 记录已存在,请检查！ "]'
        ).text
        assert error_popup == "记录已存在,请检查！", f"预期数据{error_popup}"
        assert not spec.has_fail_message()

    @allure.story("修改代码成功")
    # @pytest.mark.run(order=1)
    def test_spec_editcodesuccess(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page
        # 选中1测试A代码
        spec.click_button('//tr[./td[2][.//span[text()="1测试A"]]]/td[2]')
        # 点击修改按钮
        spec.click_edi_button()
        sleep(1)
        # 生成随机数
        random_int = random.randint(1, 10)
        text = "1测试A" + f"{random_int}"
        # 物料代码输入
        spec.enter_texts(
            '(//label[text()="代码"])[1]/parent::div//input', f"{text}"
        )
        # 点击确定
        spec.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(3)
        # 定位表格内容
        specdata = spec.get_find_element_xpath(
            '//tr[./td[2][.//span[contains(text(),"1测试A")]]]/td[2]'
        ).text
        assert specdata == text, f"预期{specdata}"
        assert not spec.has_fail_message()

    @allure.story("把修改后的代码改回来")
    # @pytest.mark.run(order=1)
    def test_spec_editcodesuccess2(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page

        # 选中1测试A代码
        spec.click_button('//tr[./td[2][.//span[contains(text(),"1测试A")]]]/td[2]')
        # 点击修改按钮
        spec.click_edi_button()
        # 代码输入
        spec.enter_texts('(//label[text()="代码"])[1]/parent::div//input', "1测试A")
        # 点击确定
        spec.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 定位表格内容
        specdata = spec.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="1测试A"]]]/td[2]'
        ).text
        assert specdata == "1测试A", f"预期{specdata}"
        assert not spec.has_fail_message()

    @allure.story("修改名称，显示颜色成功")
    # @pytest.mark.run(order=1)
    def test_spec_editnamesuccess(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page

        # 选中代码
        spec.click_button('//tr[./td[2][.//span[text()="1测试A"]]]/td[2]')
        # 点击修改按钮
        spec.click_edi_button()
        sleep(1)
        # 生成随机数
        random_int = random.randint(1, 10)
        text = "1测试A" + f"{random_int}"
        # 输入修改的物料名称
        spec.enter_texts(
            '(//label[text()="名称"])[1]/parent::div//input', f"{text}"
        )
        # 获取修改好的值
        editname = spec.get_find_element_xpath(
            '(//label[text()="名称"])[1]/parent::div//input'
        ).get_attribute("value")

        # 修改显示颜色下拉框
        spec.click_button('(//label[text()="显示颜色"])[1]/parent::div//i')
        # 显示颜色
        spec.click_button('//span[text()="RGB(242,128,255)"]')
        # 获取下拉框数据
        specsel = spec.get_find_element_xpath(
            '(//label[text()="显示颜色"])[1]/parent::div//input['
            '@class="ivu-select-input"]'
        ).get_attribute("value")
        # 点击确定
        spec.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(1)
        # 定位表格内容
        itemname = spec.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="1测试A"]]]/td[3]/div'
        ).text
        color = spec.get_find_element_xpath(
            '//tr[./td[2][.//span[text()="1测试A"]]]/td[4]/div'
        ).text
        sleep(1)
        assert (
            itemname == editname
            and specsel == color
        )
        assert not spec.has_fail_message()

    @allure.story("刷新成功")
    # @pytest.mark.run(order=1)
    def test_spec_refreshsuccess(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page

        # 代码筛选框输入123
        spec.enter_texts(
            '//p[text()="代码"]/ancestor::div[2]//input', "123"
        )
        spec.click_ref_button()
        spectext = spec.get_find_element_xpath(
            '//p[text()="代码"]/ancestor::div[2]//input'
        ).text
        assert spectext == "", f"预期{spectext}"
        assert not spec.has_fail_message()

    @allure.story("查询代码成功")
    # @pytest.mark.run(order=1)
    def test_spec_selectcodesuccess(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page

        # 点击查询
        spec.click_sel_button()
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
        spec.click_button('//div[text()="代码" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        spec.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        spec.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        spec.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "111",
        )
        sleep(1)

        # 点击确认
        spec.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行是否为111
        speccode = spec.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]'
        ).text
        # 定位第二行没有数据
        speccode2 = driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][2]/td[2]',
        )
        assert speccode == "111" and len(speccode2) == 0
        assert not spec.has_fail_message()

    @allure.story("没有数据时显示正常")
    # @pytest.mark.run(order=1)
    def test_spec_selectnodatasuccess(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page

        # 点击查询
        spec.click_sel_button()
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
        # 点击代码
        spec.click_button('//div[text()="代码" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        spec.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        spec.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        spec.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "没有数据",
        )
        sleep(1)

        # 点击确认
        spec.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        itemcode = driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]',
        )
        assert len(itemcode) == 0
        assert not spec.has_fail_message()

    @allure.story("查询显示顺序>10")
    # @pytest.mark.run(order=1)
    def test_spec_selectsuccess1(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page

        # 点击查询
        spec.click_sel_button()
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
        # 点击显示顺序
        spec.click_button('//div[text()="显示顺序" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        spec.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        spec.click_button('//div[text()=">" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        spec.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "10",
        )
        sleep(1)

        # 点击确认
        spec.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行显示顺序
        speccode = spec.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][1]/td[5]'
        ).text
        assert int(speccode) > 10
        assert not spec.has_fail_message()

    @allure.story("查询名称包含1并且显示顺序>10")
    # @pytest.mark.run(order=1)
    def test_spec_selectsuccess2(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page

        # 点击查询
        spec.click_sel_button()
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
        spec.click_button('//div[text()="名称" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击（
        spec.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[3]'
        )
        spec.click_button('//div[text()="(" and contains(@optid,"opt_")]')
        # 点击比较关系框
        spec.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击包含
        spec.click_button('//div[text()="包含" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        spec.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "1",
        )

        # 点击（
        spec.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[7]'
        )
        spec.click_button('//div[text()=")" and contains(@optid,"opt_")]')

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
        spec.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[3]'
        )
        spec.click_button('//div[text()="(" and contains(@optid,"opt_")]')
        # 点击显示顺序
        spec.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[4]'
        )
        spec.click_button('//div[text()="显示顺序" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        spec.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[5]//input'
        )
        # 点击>
        spec.click_button('//div[text()=">" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        spec.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[6]//input',
            "10",
        )
        # 点击（
        spec.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[7]'
        )
        spec.click_button('//div[text()=")" and contains(@optid,"opt_")]')

        sleep(1)

        # 点击确认
        spec.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行
        specname = spec.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][1]/td[3]'
        ).text
        specorder = spec.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][1]/td[5]'
        ).text
        # 判断第一行名称包含1、显示顺序>10
        assert "1" in specname and int(specorder) > 10
        assert not spec.has_fail_message()

    @allure.story("查询名称包含11或显示顺序>10")
    # @pytest.mark.run(order=1)
    def test_spec_selectsuccess3(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page

        # 点击查询
        spec.click_sel_button()
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
        # 点击名称
        spec.click_button('//div[text()="名称" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击（
        spec.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[3]'
        )
        spec.click_button('//div[text()="(" and contains(@optid,"opt_")]')
        # 点击比较关系框
        spec.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击包含
        spec.click_button('//div[text()="包含" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        spec.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "11",
        )

        # 点击（
        spec.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[7]'
        )
        spec.click_button('//div[text()=")" and contains(@optid,"opt_")]')

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
        spec.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[3]'
        )
        spec.click_button('//div[text()="(" and contains(@optid,"opt_")]')
        # 点击显示顺序
        spec.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[4]'
        )
        spec.click_button('//div[text()="显示顺序" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        spec.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[5]//input'
        )
        # 点击>
        spec.click_button('//div[text()=">" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值10
        spec.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[6]//input',
            "10",
        )
        # 点击（
        spec.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[7]'
        )
        spec.click_button('//div[text()=")" and contains(@optid,"opt_")]')

        sleep(1)

        # 点击确认
        spec.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 获取目标表格第2个 vxe 表格中的所有数据行
        xpath_rows = '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")]'

        # 先拿到总行数
        base_rows = driver.find_elements(By.XPATH, xpath_rows)
        total = len(base_rows)

        valid_count = 0
        for idx in range(total):
            try:
                # 每次都按索引重新定位这一行
                row = driver.find_elements(By.XPATH, xpath_rows)[idx]
                tds = row.find_elements(By.TAG_NAME, "td")
                td3 = tds[2].text.strip()
                td5_raw = tds[4].text.strip()
                td5_val = int(td5_raw) if td5_raw else 0

                assert "11" in td3 or td5_val > 10, f"第 {idx + 1} 行不符合：td3={td3}, td5={td5_raw}"
                valid_count += 1

            except StaleElementReferenceException:
                # 如果行元素失效，再重试一次
                row = driver.find_elements(By.XPATH, xpath_rows)[idx]
                tds = row.find_elements(By.TAG_NAME, "td")
                td3 = tds[2].text.strip()
                td5_raw = tds[4].text.strip()
                td5_val = int(td5_raw) if td5_raw else 0
                assert "11" in td3 or td5_val > 10, f"第 {idx + 1} 行不符合：td3={td3}, td5={td5_raw}"
                valid_count += 1
        assert not spec.has_fail_message()
        print(f"符合条件的行数：{valid_count}")

    @allure.story("输入全部数据，添加保存成功")
    # @pytest.mark.run(order=1)
    def test_spec_addall(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page
        data_list = ["全部数据", "20"]
        spec.click_add_button()  # 检查点击添加
        spec.add_input_all(data_list[0], data_list[1])
        sleep(1)
        spec.enter_texts(
            '//p[text()="代码"]/ancestor::div[2]//input', data_list[0]
        )
        # 缩放到最小（例如 25%）
        driver.execute_script("document.body.style.zoom='0.25'")
        sleep(1)

        row_xpath = f'//tr[./td[2][.//span[text()="{data_list[0]}"]]]'
        # 获取目标行
        target_row = driver.find_element(By.XPATH, row_xpath)

        # 获取该行下所有 td 元素
        td_elements = target_row.find_elements(By.XPATH, "./td")
        td_count = len(td_elements)
        print(f"该行共有 {td_count} 个 <td> 元素")
        columns_text = []
        # 遍历每个 td[i]
        # 遍历每个 td[i] 并提取文本
        for i in range(2, td_count + 1):
            td_xpath = f'{row_xpath}/td[{i}]'
            sleep(0.2)
            try:
                td = driver.find_element(By.XPATH, td_xpath)
                text = td.text.strip()
                print(f"第 {i} 个单元格内容：{text}")
                columns_text.append(text)
            except StaleElementReferenceException:
                print(f"⚠️ 第 {i} 个单元格引用失效，尝试重新查找")
                sleep(0.2)
                td = driver.find_element(By.XPATH, td_xpath)
                text = td.text.strip()
                columns_text.append(text)

        print(columns_text)
        bef_text = ['全部数据', '全部数据', '2', '20', '全部数据', f'{DateDriver().username}', '2025', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20']
        assert len(columns_text) == len(bef_text), f"长度不一致：actual={len(columns_text)}, expected={len(bef_text)}"
        for i, (a, e) in enumerate(zip(columns_text, bef_text)):
            if i == 6:
                assert str(e) in str(a), f"第7项包含断言失败：'{e}' not in '{a}'"
            else:
                assert a == e, f"第{i + 1}项不一致：actual='{a}', expected='{e}'"
        assert not spec.has_fail_message()

    @allure.story("重新打开浏览器，数据还存在")
    # @pytest.mark.run(order=1)
    def test_spec_restart(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page
        code = '全部数据'
        spec.enter_texts(
            '//p[text()="代码"]/ancestor::div[2]//input', code
        )
        # 缩放到最小（例如 25%）
        driver.execute_script("document.body.style.zoom='0.25'")
        sleep(1)

        row_xpath = f'//tr[./td[2][.//span[text()="{code}"]]]'
        # 获取目标行
        target_row = driver.find_element(By.XPATH, row_xpath)

        # 获取该行下所有 td 元素
        td_elements = target_row.find_elements(By.XPATH, "./td")
        td_count = len(td_elements)
        print(f"该行共有 {td_count} 个 <td> 元素")
        columns_text = []
        # 遍历每个 td[i]
        # 遍历每个 td[i] 并提取文本
        for i in range(2, td_count + 1):
            td_xpath = f'{row_xpath}/td[{i}]'
            sleep(0.2)
            try:
                td = driver.find_element(By.XPATH, td_xpath)
                text = td.text.strip()
                print(f"第 {i} 个单元格内容：{text}")
                columns_text.append(text)
            except StaleElementReferenceException:
                print(f"⚠️ 第 {i} 个单元格引用失效，尝试重新查找")
                sleep(0.2)
                td = driver.find_element(By.XPATH, td_xpath)
                text = td.text.strip()
                columns_text.append(text)

        print(columns_text)
        bef_text = ['全部数据', '全部数据', '2', '20', '全部数据', f'{DateDriver().username}', '2025', '20', '20', '20',
                    '20', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20', '20',
                    '20', '20']
        assert len(columns_text) == len(bef_text), f"长度不一致：actual={len(columns_text)}, expected={len(bef_text)}"
        for i, (a, e) in enumerate(zip(columns_text, bef_text)):
            if i == 6:
                assert str(e) in str(a), f"第7项包含断言失败：'{e}' not in '{a}'"
            else:
                assert a == e, f"第{i + 1}项不一致：actual='{a}', expected='{e}'"
        assert not spec.has_fail_message()

    @allure.story("删除全部input数据成功")
    # @pytest.mark.run(order=1)
    def test_spec_delall(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page
        spec.enter_texts(
            '//p[text()="代码"]/ancestor::div[2]//input', "全部数据"
        )
        sleep(2)
        # 定位内容为‘全部数据’的行
        spec.click_button('//tr[./td[2][.//span[text()="全部数据"]]]/td[2]')
        spec.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        parent = spec.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        sleep(1)
        # 定位内容为‘全部数据’的行
        itemdata = driver.find_elements(
            By.XPATH, '//tr[./td[2][.//span[text()="全部数据"]]]/td[2]'
        )
        assert len(itemdata) == 0
        assert not spec.has_fail_message()

    @allure.story("删除数据成功")
    # @pytest.mark.run(order=1)
    def test_spec_delsuccess(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page

        # 定位内容为‘111’的行
        spec.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
        spec.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        parent = spec.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        sleep(1)
        # 定位内容为‘111’的行
        itemdata = driver.find_elements(
            By.XPATH, '//tr[./td[2][.//span[text()="111"]]]/td[2]'
        )
        assert len(itemdata) == 0
        assert not spec.has_fail_message()

    @allure.story("删除测试数据成功，删除布局成功")
    # @pytest.mark.run(order=1)
    def test_spec_delsuccess1(self, login_to_spec1):
        driver = login_to_spec1  # WebDriver 实例
        spec = Spec1Page(driver)  # 用 driver 初始化 Spec1Page
        layout = "测试布局A"

        # 定位内容为‘1测试A’的行
        spec.click_button('//tr[./td[2][.//span[text()="1测试A"]]]/td[2]')
        spec.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        parent = spec.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        sleep(1)
        # 定位内容为‘1测试A’的行
        specdata = driver.find_elements(
            By.XPATH, '//tr[./td[2][.//span[text()="1测试A"]]]/td[2]'
        )

        # 获取目标 div 元素，这里的目标是具有特定文本的 div
        target_div = spec.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        )

        # 获取父容器下所有 div
        # 这一步是为了确定目标 div 在其父容器中的位置
        parent_div = spec.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon" and ./div[text()=" {layout} "]]'
        )
        all_children = parent_div.find_elements(By.XPATH, "./div")

        # 获取目标 div 的位置索引（从0开始）
        # 这里是为了后续操作，比如点击目标 div 相关的按钮
        index = all_children.index(target_div)
        print(f"目标 div 是第 {index + 1} 个 div")  # 输出 3（如果从0开始则是2）
        sleep(2)
        spec.click_button(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]//i'
        )
        # 根据目标 div 的位置，点击对应的“删除布局”按钮
        spec.click_button(f'(//li[text()="删除布局"])[{index + 1}]')
        sleep(2)
        # 点击确认删除的按钮
        spec.click_button('//button[@class="ivu-btn ivu-btn-primary ivu-btn-large"]')
        # 等待一段时间，确保删除操作完成
        sleep(1)

        # 再次查找页面上是否有目标 div，以验证是否删除成功
        after_layout = driver.find_elements(
            By.XPATH, f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        )
        assert len(specdata) == 0 == len(after_layout)
        assert not spec.has_fail_message()
