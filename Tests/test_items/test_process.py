import random
from time import sleep

import allure
import pytest
from selenium.common import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.itemsPage.login_page import LoginPage
from Pages.itemsPage.process_page import ProcessPage
from Utils.data_driven import DateDriver
from Utils.driver_manager import create_driver, safe_quit


@pytest.fixture  # (scope="class")这个参数表示整个测试类共用同一个浏览器，默认一个用例执行一次
def login_to_process():
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
    page.click_button('(//span[text()="工序"])[1]')  # 点击工序
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("工序表测试用例")
@pytest.mark.run(order=8)
class TestProcessPage:
    @allure.story("添加工序信息 不填写数据点击确认 不允许提交，添加新布局")
    # @pytest.mark.run(order=1)
    def test_process_addfail(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage
        layout = "测试布局A"
        process.add_layout(layout)
        # 获取布局名称的文本元素
        name = process.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        ).text
        process.click_add_button()
        # 工序代码xpath
        input_box = process.get_find_element_xpath(
            '(//label[text()="工序代码"])[1]/parent::div//input'
        )
        # 工序名xpath
        inputname_box = process.get_find_element_xpath(
            '(//label[text()="工序名"])[1]/parent::div//input'
        )
        process.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
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
        assert name == layout
        assert not process.has_fail_message()

    @allure.story("添加工序信息，只填写工序代码，不填写工序名，不允许提交")
    # @pytest.mark.run(order=2)
    def test_process_addcodefail(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        process.click_add_button()
        process.enter_texts(
            '(//label[text()="工序代码"])[1]/parent::div//input', "text1231"
        )
        process.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        input_box = process.get_find_element_xpath(
            '(//label[text()="工序名"])[1]/parent::div//input'
        )
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        border_color = input_box.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert (
            border_color == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{border_color}"
        assert not process.has_fail_message()

    @allure.story("添加工序信息，只填写工序名，不填写工序代码，不允许提交")
    # @pytest.mark.run(order=3)
    def test_process_addnamefail(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        process.click_add_button()
        process.enter_texts(
            '(//label[text()="工序名"])[1]/parent::div//input', "text1231"
        )
        sleep(1)
        # 点击确定
        process.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        input_box = process.get_find_element_xpath(
            '(//label[text()="工序代码"])[1]/parent::div//input'
        )
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        border_color = input_box.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert (
            border_color == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{border_color}"
        assert not process.has_fail_message()

    @allure.story("数字文本框 只允许填写数字")
    # @pytest.mark.run(order=1)
    def test_process_addnum(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        process.click_add_button()  # 检查点击添加
        # 表示顺序数字框输入文字字母符号数字
        element = process.get_find_element_xpath(
            '(//label[text()="表示顺序"])[1]/parent::div//input'
        )
        # 全选后删除
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        sleep(1)
        process.enter_texts(
            '(//label[text()="表示顺序"])[1]/parent::div//input', "1文字abc。？~1_2+3"
        )
        sleep(1)
        # 获取表示顺序数字框
        processnum = process.get_find_element_xpath(
            '(//label[text()="表示顺序"])[1]/parent::div//input'
        ).get_attribute("value")
        assert processnum == "1123", f"预期{processnum}"
        assert not process.has_fail_message()

    @allure.story("下拉框选择成功")
    # @pytest.mark.run(order=1)
    def test_process_addsel(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        process.click_add_button()  # 检查点击添加
        # 显示颜色下拉框
        process.click_button('(//label[text()="显示颜色"])[1]/parent::div//i')
        # 显示颜色
        process.click_button('//span[text()="2"]')
        # 获取下拉框数据
        processsel = process.get_find_element_xpath(
            '(//label[text()="显示颜色"])[1]/parent::div//input['
            '@class="ivu-select-input"]'
        ).get_attribute("value")
        assert processsel == "2", f"预期{processsel}"
        assert not process.has_fail_message()

    # @allure.story('复选框勾选成功')
    # # @pytest.mark.run(order=1)
    # def test_process_checkbox(self, login_to_process):
    #     driver = login_to_process  # WebDriver 实例
    #     process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage
    #
    #     process.click_button('(//span[(text()="勾选复选框")])[1]')
    #     process.click_edi_button()  # 检查点击修改
    #     checkbox = process.get_find_element_xpath('//label[text()="无效标志"]/parent::div//span[1]')
    #     # 勾选复选框
    #     if checkbox.get_attribute('class') == 'ivu-checkbox ivu-checkbox-checked':
    #         # 点击确定
    #         process.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
    #     else:
    #         element = process.get_find_element_xpath('//label[text()="无效标志"]/parent::div//input')
    #         driver.execute_script("arguments[0].click();", element)
    #         process.click_button('//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"]/button[1]')
    #     checkboxlist = process.get_find_element_xpath('//span[text()="勾选复选框"]/ancestor::tr/td[6]//label')
    #     assert checkboxlist.get_attribute('class') == 'notClick vxe-checkbox size--small is--checked'

    # @allure.story('取消复选框勾选成功')
    # # @pytest.mark.run(order=1)
    # def test_process_nocheckbox(self, login_to_process):
    #     driver = login_to_process  # WebDriver 实例
    #     process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage
    #     sleep(1)  # 等待页面加载
    #     process.click_button('(//span[(text()="勾选复选框")])[1]')
    #     process.click_edi_button()  # 检查点击修改
    #     checkbox = process.get_find_element_xpath('//label[text()="无效标志"]/parent::div//input')
    #     # 勾选复选框
    #     if checkbox.is_selected():
    #         sleep(1)
    #         process.click_button('//label[text()="无效标志"]/parent::div//input')
    #         # 点击确定
    #         process.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
    #     else:
    #         process.click_button('//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"]/button[1]')
    #     checkboxlist = process.get_find_element_xpath('//span[text()="勾选复选框"]/ancestor::tr[1]/td[6]//input')
    #     sleep(3)
    #     assert checkbox.is_selected() == checkboxlist.is_selected()

    @allure.story("添加数据成功")
    # @pytest.mark.run(order=1)
    def test_process_addsuccess(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        process.click_add_button()  # 检查点击添加
        # 输入工序代码
        process.enter_texts('(//label[text()="工序代码"])[1]/parent::div//input', "111")
        process.enter_texts('(//label[text()="工序名"])[1]/parent::div//input', "111")
        # 点击确定
        process.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        adddata = process.get_find_element_xpath(
            '(//span[text()="111"])[1]/ancestor::tr[1]/td[2]'
        ).text
        assert adddata == "111", f"预期数据是111，实际得到{adddata}"
        assert not process.has_fail_message()

    @allure.story("添加数据重复")
    # @pytest.mark.run(order=1)
    def test_process_addrepeat(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        process.click_add_button()  # 检查点击添加
        # 输入工序代码
        process.enter_texts('(//label[text()="工序代码"])[1]/parent::div//input', "111")
        process.enter_texts('(//label[text()="工序名"])[1]/parent::div//input', "检查")
        # 点击确定
        process.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 获取重复弹窗文字
        error_popup = process.get_find_element_xpath(
            '//div[text()=" 记录已存在,请检查！ "]'
        ).text
        assert (
            error_popup == "记录已存在,请检查！"
        ), f"预期数据是记录已存在,请检查，实际得到{error_popup}"
        assert not process.has_fail_message()

    @allure.story("取消删除数据")
    # @pytest.mark.run(order=1)
    def test_process_delcancel(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        # 定位内容为‘111’的行
        process.click_button('(//span[text()="111"])[1]/ancestor::tr[1]/td[2]')
        process.click_del_button()  # 点击删除
        sleep(1)
        # 点击取消
        process.click_button('//button[@class="ivu-btn ivu-btn-text"]')
        sleep(1)
        # 定位内容为‘111’的行
        processdata = process.get_find_element_xpath(
            '(//span[text()="111"])[1]/ancestor::tr[1]/td[2]'
        ).text
        assert processdata == "111", f"预期{processdata}"
        assert not process.has_fail_message()

    @allure.story("添加测试数据成功")
    # @pytest.mark.run(order=1)
    def test_process_addsuccess1(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        process.click_add_button()  # 检查点击添加
        # 输入工序代码
        process.enter_texts(
            '(//label[text()="工序代码"])[1]/parent::div//input', "1测试A"
        )
        process.enter_texts(
            '(//label[text()="工序名"])[1]/parent::div//input', "1测试A"
        )
        # 点击确定
        process.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        adddata = process.get_find_element_xpath(
            '(//span[text()="1测试A"])[1]/ancestor::tr[1]/td[2]'
        ).text
        assert adddata == "1测试A", f"预期数据是1测试A，实际得到{adddata}"
        assert not process.has_fail_message()

    @allure.story("修改工序代码重复")
    # @pytest.mark.run(order=1)
    def test_process_editrepeat(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        # 选中切割工序代码
        process.click_button('(//span[text()="1测试A"])[1]')
        # 点击修改按钮
        process.click_edi_button()
        # 工序代码输入检查
        sleep(1)
        process.enter_texts('(//label[text()="工序代码"])[1]/parent::div//input', "111")
        # 点击确定
        process.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 获取重复弹窗文字
        error_popup = process.get_find_element_xpath(
            '//div[text()=" 记录已存在,请检查！ "]'
        ).text
        assert error_popup == "记录已存在,请检查！", f"预期数据{error_popup}"
        assert not process.has_fail_message()

    @allure.story("修改工序代码成功")
    # @pytest.mark.run(order=1)
    def test_process_editcodesuccess(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        # 选中产包装工序代码
        process.click_button('(//span[text()="1测试A"])[1]')
        # 点击修改按钮
        process.click_edi_button()
        sleep(1)
        # 生成随机数
        random_int = random.randint(1, 10)
        text = "1测试A" + f"{random_int}"
        # 工序代码输入
        process.enter_texts(
            '(//label[text()="工序代码"])[1]/parent::div//input', f"{text}"
        )
        # 点击确定
        process.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 定位表格内容
        processdata = process.get_find_element_xpath(
            '(//span[contains(text(),"1测试A")])[1]'
        ).text
        assert processdata == text, f"预期{processdata}"
        assert not process.has_fail_message()

    @allure.story("把修改后的工序代码改回来")
    # @pytest.mark.run(order=1)
    def test_process_editcodesuccess2(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        # 选中1测试A工序代码
        process.click_button('(//span[contains(text(),"1测试A")])[1]')
        # 点击修改按钮
        process.click_edi_button()
        # 工序代码输入
        process.enter_texts(
            '(//label[text()="工序代码"])[1]/parent::div//input', "1测试A"
        )
        # 点击确定
        process.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 定位表格内容
        processdata = process.get_find_element_xpath(
            '(//span[text()="1测试A"])[1]'
        ).text
        assert processdata == "1测试A", f"预期{processdata}"
        assert not process.has_fail_message()

    @allure.story("修改工序名，显示颜色成功")
    # @pytest.mark.run(order=1)
    def test_process_editnamesuccess(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        # 选中工序代码
        process.click_button('//tr[.//span[text()="1测试A"]]/td[2]')
        # 点击修改按钮
        process.click_edi_button()
        sleep(1)
        # 生成随机数
        random_int = random.randint(1, 8)
        text = "1测试A" + f"{random_int}"
        # 输入修改的工序名
        process.enter_texts(
            '(//label[text()="工序名"])[1]/parent::div//input', f"{text}"
        )
        # 获取修改好的值
        editname = process.get_find_element_xpath(
            '(//label[text()="工序名"])[1]/parent::div//input'
        ).get_attribute("value")

        # 显示颜色下拉框
        process.click_button('(//label[text()="显示颜色"])[1]/parent::div//i')
        sleep(2)
        # 显示颜色
        process.click_button(f'//span[text()="{random_int}"]')
        # 获取下拉框数据
        processsel = process.get_find_element_xpath(
            '(//label[text()="显示颜色"])[1]/parent::div//input['
            '@class="ivu-select-input"]'
        ).get_attribute("value")
        # 点击确定
        process.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 定位表格内容
        processname = process.get_find_element_xpath(
            '(//span[text()="1测试A"])[1]/ancestor::tr/td[3]/div'
        ).text
        processautoGenerateFlag = process.get_find_element_xpath(
            '(//span[text()="1测试A"])[1]/ancestor::tr/td[4]/div'
        ).text
        assert processname == editname and processautoGenerateFlag == processsel
        assert not process.has_fail_message()

    @allure.story("刷新成功")
    # @pytest.mark.run(order=1)
    def test_process_refreshsuccess(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        # 工序代码筛选框输入123
        process.enter_texts(
            '//p[text()="工序代码"]/ancestor::div[2]//input', "123"
        )
        process.click_ref_button()
        processtext = process.get_find_element_xpath(
            '//p[text()="工序代码"]/ancestor::div[2]//input'
        ).text
        assert processtext == "", f"预期{processtext}"
        assert not process.has_fail_message()

    @allure.story("查询工序代码成功")
    # @pytest.mark.run(order=1)
    def test_process_selectcodesuccess(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        # 点击查询
        process.click_sel_button()
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
        # 点击工序代码
        process.click_button('//div[text()="工序代码" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        process.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        process.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "111",
        )
        sleep(1)

        # 点击确认
        process.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行是否为111
        processcode = process.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]'
        ).text
        # 定位第二行没有数据
        processcode2 = driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][2]/td[2]',
        )
        assert processcode == "111" and len(processcode2) == 0
        assert not process.has_fail_message()

    @allure.story("没有数据时显示正常")
    # @pytest.mark.run(order=1)
    def test_process_selectnodatasuccess(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        # 点击查询
        process.click_sel_button()
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
        # 点击工序代码
        process.click_button('//div[text()="工序代码" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        process.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        process.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "没有数据",
        )
        sleep(1)

        # 点击确认
        process.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行是否为
        processcode = driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]',
        )
        assert len(processcode) == 0
        assert not process.has_fail_message()

    @allure.story("查询工序名字成功")
    # @pytest.mark.run(order=1)
    def test_process_selectnamesuccess(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        # 点击查询
        process.click_sel_button()
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
        # 点击工序名
        process.click_button('//div[text()="工序名" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        process.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        process.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "打包",
        )
        sleep(1)

        # 点击确认
        process.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行
        processcode = process.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[3]'
        ).text
        # 定位第二行没有数据
        processcode2 = driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][2]/td[3]',
        )
        assert processcode == "打包" and len(processcode2) == 0
        assert not process.has_fail_message()

    @allure.story("表示顺序>60")
    # @pytest.mark.run(order=1)
    def test_process_selectsuccess1(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        # 点击查询
        process.click_sel_button()
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
        # 点击表示顺序
        process.click_button('//div[text()="表示顺序" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        process.click_button('//div[text()=">" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        process.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "60",
        )
        sleep(1)

        # 点击确认
        process.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行
        processcode = process.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][1]/td[5]'
        ).text
        # 定位第二行数据
        processcode2 = process.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][2]/td[5]'
        ).text
        assert int(processcode) > 60 and int(processcode2) > 60
        assert not process.has_fail_message()

    @allure.story("查询工序名包含裁剪并且表示顺序>70")
    # @pytest.mark.run(order=1)
    def test_process_selectsuccess2(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        # 点击查询
        process.click_sel_button()
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
        # 点击工序名
        process.click_button('//div[text()="工序名" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击（
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[3]'
        )
        process.click_button('//div[text()="(" and contains(@optid,"opt_")]')
        # 点击比较关系框
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击包含
        process.click_button('//div[text()="包含" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        process.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "裁剪",
        )

        # 点击（
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[7]'
        )
        process.click_button('//div[text()=")" and contains(@optid,"opt_")]')

        double_click = driver.find_element(
            By.XPATH,
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[2]',
        )
        sleep(1)
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
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[3]'
        )
        process.click_button('//div[text()="(" and contains(@optid,"opt_")]')
        # 点击物料优先度
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[4]'
        )
        process.click_button('//div[text()="表示顺序" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[5]//input'
        )
        # 点击>
        process.click_button('//div[text()=">" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        process.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[6]//input',
            "70",
        )
        # 点击（
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[7]'
        )
        process.click_button('//div[text()=")" and contains(@optid,"opt_")]')

        sleep(1)
        # 点击确认
        process.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行表示顺序
        processcode = process.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][1]/td[5]'
        ).text
        processname = process.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][1]/td[3]'
        ).text
        assert "裁剪" in processname and int(processcode) > 70
        assert not process.has_fail_message()

    @allure.story("查询工序名包含检查或表示顺序>70")
    # @pytest.mark.run(order=1)
    def test_process_selectsuccess3(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        # 点击查询
        process.click_sel_button()
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
        # 点击工序名
        process.click_button('//div[text()="工序名" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击（
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[3]'
        )
        process.click_button('//div[text()="(" and contains(@optid,"opt_")]')
        # 点击比较关系框
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击包含
        process.click_button('//div[text()="包含" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        process.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "检查",
        )

        # 点击（
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[7]'
        )
        process.click_button('//div[text()=")" and contains(@optid,"opt_")]')

        sleep(1)
        double_click = driver.find_element(
            By.XPATH,
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[2]',
        )
        # 双击命令
        actions.double_click(double_click).perform()

        # 定义or元素的XPath
        or_xpath = '//div[text()="or" and contains(@optid,"opt_")]'

        try:
            # 首先尝试直接查找并点击and元素
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
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[3]'
        )
        process.click_button('//div[text()="(" and contains(@optid,"opt_")]')
        # 点击物料优先度
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[4]'
        )
        process.click_button('//div[text()="表示顺序" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[5]//input'
        )
        # 点击>
        sleep(1)
        process.click_button('//div[text()=">" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值70
        process.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[6]//input',
            "70",
        )
        # 点击（
        process.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[2]/td[7]'
        )
        process.click_button('//div[text()=")" and contains(@optid,"opt_")]')

        sleep(1)

        # 点击确认
        process.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行物料优先度
        processname = process.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][1]/td[3]'
        ).text
        processcode = process.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][1]/td[5]'
        ).text
        # 定位第二行数据
        processname2 = process.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][2]/td[3]'
        ).text
        processcode2 = process.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[contains(@class,"vxe-body--row")][2]/td[5]'
        ).text

        sleep(1)
        assert ("开料" in processname or int(processcode) > 70) and (
            "开料" in processname2 or int(processcode2) > 70
        )
        assert not process.has_fail_message()

    @allure.story("输入全部数据，添加保存成功")
    # @pytest.mark.run(order=1)
    def test_process_addall(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage
        data_list = ["全部数据", "20"]
        process.click_add_button()  # 检查点击添加
        process.add_input_all(data_list[0], data_list[1])
        sleep(1)
        process.enter_texts(
            '//p[text()="工序代码"]/ancestor::div[2]//input', data_list[0]
        )
        # 缩放到最小（例如 70%）
        driver.execute_script("document.body.style.zoom='0.7'")
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
            except StaleElementReferenceException:
                print(f"⚠️ 第 {i} 个单元格引用失效，尝试重新查找")
                sleep(0.2)
                td = driver.find_element(By.XPATH, td_xpath)

            if i == 6:
                try:
                    label = td.find_element(By.TAG_NAME, "label")
                    label_class = label.get_attribute("class")
                    print(f"第 {i} 个单元格中 <label> 的 class 属性：{label_class}")
                    columns_text.append(label_class)
                except NoSuchElementException:
                    print(f"⚠️ 第 {i} 个单元格中未找到 <label> 元素")
                    columns_text.append("")
            else:
                text = td.text.strip()
                print(f"第 {i} 个单元格内容：{text}")
                columns_text.append(text)

        print(columns_text)
        bef_text = ['全部数据', '全部数据', '2', '20', 'is--checked', '全部数据', f'{DateDriver.username}', '2025']
        assert len(columns_text) == len(bef_text), f"长度不一致：actual={len(columns_text)}, expected={len(bef_text)}"
        for i, (a, e) in enumerate(zip(columns_text, bef_text)):
            if i == 4:
                assert str(e) in str(a), f"第5项包含断言失败：'{e}' not in '{a}'"
            elif i == 7:
                assert str(e) in str(a), f"第6项包含断言失败：'{e}' not in '{a}'"
            else:
                assert a == e, f"第{i + 1}项不一致：actual='{a}', expected='{e}'"
        assert not process.has_fail_message()

    @allure.story("重新打开浏览器，数据还存在")
    # @pytest.mark.run(order=1)
    def test_process_restart(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage
        code = '全部数据'
        process.enter_texts(
            '//p[text()="工序代码"]/ancestor::div[2]//input', code
        )
        # 缩放到最小（例如 70%）
        driver.execute_script("document.body.style.zoom='0.7'")
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
            except StaleElementReferenceException:
                print(f"⚠️ 第 {i} 个单元格引用失效，尝试重新查找")
                sleep(0.2)
                td = driver.find_element(By.XPATH, td_xpath)

            if i == 6:
                try:
                    label = td.find_element(By.TAG_NAME, "label")
                    label_class = label.get_attribute("class")
                    print(f"第 {i} 个单元格中 <label> 的 class 属性：{label_class}")
                    columns_text.append(label_class)
                except NoSuchElementException:
                    print(f"⚠️ 第 {i} 个单元格中未找到 <label> 元素")
                    columns_text.append("")
            else:
                text = td.text.strip()
                print(f"第 {i} 个单元格内容：{text}")
                columns_text.append(text)

        print(columns_text)
        bef_text = ['全部数据', '全部数据', '2', '20', 'is--checked', '全部数据', f'{DateDriver.username}', '2025']
        assert len(columns_text) == len(bef_text), f"长度不一致：actual={len(columns_text)}, expected={len(bef_text)}"
        for i, (a, e) in enumerate(zip(columns_text, bef_text)):
            if i == 4:
                assert str(e) in str(a), f"第5项包含断言失败：'{e}' not in '{a}'"
            elif i == 7:
                assert str(e) in str(a), f"第6项包含断言失败：'{e}' not in '{a}'"
            else:
                assert a == e, f"第{i + 1}项不一致：actual='{a}', expected='{e}'"
        assert not process.has_fail_message()

    @allure.story("删除全部input数据成功")
    # @pytest.mark.run(order=1)
    def test_processr_delall(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage
        code = '全部数据'
        process.enter_texts(
            '//p[text()="工序代码"]/ancestor::div[2]//input', code
        )
        sleep(2)
        # 定位内容为‘全部数据’的行
        process.click_button('//tr[./td[2][.//span[text()="全部数据"]]]/td[2]')
        process.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        parent = process.get_find_element_class("ivu-modal-confirm-footer")

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
        assert not process.has_fail_message()

    @allure.story("删除数据成功")
    # @pytest.mark.run(order=1)
    def test_process_delsuccess(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage

        # 定位内容为‘111’的行
        process.click_button('(//span[text()="111"])[1]/ancestor::tr[1]/td[2]')
        process.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        parent = process.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        sleep(1)
        # 定位内容为‘111’的行
        processdata = driver.find_elements(
            By.XPATH, '(//span[text()="111"])[1]/ancestor::tr[1]/td[2]'
        )
        assert len(processdata) == 0
        assert not process.has_fail_message()

    @allure.story("删除测试数据成功，删除布局")
    # @pytest.mark.run(order=1)
    def test_process_delsuccess1(self, login_to_process):
        driver = login_to_process  # WebDriver 实例
        process = ProcessPage(driver)  # 用 driver 初始化 ProcessPage
        layout = "测试布局A"

        # 定位内容为‘1测试A’的行
        process.click_button('(//span[text()="1测试A"])[1]/ancestor::tr[1]/td[2]')
        process.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        parent = process.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        sleep(1)
        # 定位内容为‘1测试A’的行
        processdata = driver.find_elements(
            By.XPATH, '(//span[text()="1测试A"])[1]/ancestor::tr[1]/td[2]'
        )

        # 获取目标 div 元素，这里的目标是具有特定文本的 div
        target_div = process.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        )

        # 获取父容器下所有 div
        # 这一步是为了确定目标 div 在其父容器中的位置
        parent_div = process.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon" and ./div[text()=" {layout} "]]'
        )
        all_children = parent_div.find_elements(By.XPATH, "./div")

        # 获取目标 div 的位置索引（从0开始）
        # 这里是为了后续操作，比如点击目标 div 相关的按钮
        index = all_children.index(target_div)
        print(f"目标 div 是第 {index + 1} 个 div")  # 输出 3（如果从0开始则是2）
        sleep(2)
        process.click_button(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]//i'
        )
        # 根据目标 div 的位置，点击对应的“删除布局”按钮
        process.click_button(f'(//li[text()="删除布局"])[{index + 1}]')
        sleep(2)
        # 点击确认删除的按钮
        process.click_button('//button[@class="ivu-btn ivu-btn-primary ivu-btn-large"]')
        # 等待一段时间，确保删除操作完成
        sleep(1)

        # 再次查找页面上是否有目标 div，以验证是否删除成功
        after_layout = driver.find_elements(
            By.XPATH, f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        )
        assert len(processdata) == 0 == len(after_layout)
        assert not process.has_fail_message()
