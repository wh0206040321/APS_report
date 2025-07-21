import random
from time import sleep

import allure
import pytest
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.itemsPage.login_page import LoginPage
from Pages.itemsPage.shift_page import ShiftPage
from Utils.data_driven import DateDriver
from Utils.driver_manager import create_driver, safe_quit


@pytest.fixture  # (scope="class")这个参数表示整个测试类共用同一个浏览器，默认一个用例执行一次
def login_to_shift():
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
    page.click_button('(//span[text()="班次"])[1]')  # 点击班次
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("班次表测试用例")
@pytest.mark.run(order=9)
class TestShiftPage:
    @allure.story("添加班次信息 不填写数据点击确认 不允许提交")
    # @pytest.mark.run(order=1)
    def test_shift_addfail(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage
        layout = "测试布局A"
        shift.add_layout()
        sleep(1)
        shift.enter_texts(
            '//div[text()="当前布局:"]/following-sibling::div//input', f"{layout}"
        )
        checkbox1 = shift.get_find_element_xpath(
            '//div[text()="是否默认启动:"]/following-sibling::label/span'
        )

        # 检查复选框是否未被选中
        if checkbox1.get_attribute("class") == "ivu-checkbox":
            # 如果未选中，则点击复选框进行选中
            shift.click_button(
                '//div[text()="是否默认启动:"]/following-sibling::label/span'
            )
        sleep(1)

        shift.click_button('(//div[text()=" 显示设置 "])[1]')
        # 获取是否可见选项的复选框元素
        checkbox2 = shift.get_find_element_xpath(
            '(//div[./div[text()="是否可见:"]])[1]/label/span'
        )
        # 检查复选框是否未被选中
        if checkbox2.get_attribute("class") == "ivu-checkbox":
            # 如果未选中，则点击复选框进行选中
            shift.click_button('(//div[./div[text()="是否可见:"]])[1]/label/span')
            # 点击确定按钮保存设置
            shift.click_button('(//div[@class="demo-drawer-footer"])[3]/button[2]')
        else:
            # 如果已选中，直接点击确定按钮保存设置
            shift.click_button('(//div[@class="demo-drawer-footer"])[3]/button[2]')

        shift.click_add_button()
        # 班次代码xpath
        input_box = shift.get_find_element_xpath(
            '(//label[text()="代码"])[1]/parent::div//input'
        )
        # 获取布局名称的文本元素
        name = shift.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        ).text

        shift.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        border_color = input_box.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert (
            border_color == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{border_color}"
        assert name == layout
        assert not shift.has_fail_message()

    @allure.story("数字文本框 只允许填写数字")
    # @pytest.mark.run(order=1)
    def test_shift_addnum(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage

        shift.click_add_button()  # 检查点击添加
        # 填写数字的第一个数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//input[1]', "1文字abc。？~1"
        )
        sleep(1)
        # 获取表示顺序数字框
        shiftnum = shift.get_find_element_xpath(
            '//label[text()="时间"]/ancestor::div[1]//input[1]'
        ).get_attribute("value")
        assert shiftnum == "11", f"预期{shiftnum}"
        assert not shift.has_fail_message()

    @allure.story("第一个时间数字框超过23默认为23，第二个时间数字框超过24默认为24")
    # @pytest.mark.run(order=1)
    def test_shift_adddatenum(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage

        shift.click_add_button()  # 检查点击添加
        # 填写第一个日期数字的第一个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[1]//input',
            "345",
        )

        # 填写第二个日期数字的第二个一个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[4]//input',
            "345",
        )
        sleep(1)
        # 获取表示顺序数字框
        shiftnum1 = shift.get_find_element_xpath(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[1]//input'
        ).get_attribute("value")
        shiftnum2 = shift.get_find_element_xpath(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[4]//input'
        ).get_attribute("value")
        assert shiftnum1 == "23" and shiftnum2 == "24", f"预期{shiftnum1},{shiftnum2}"
        assert not shift.has_fail_message()

    @allure.story(
        "第一个时间数字框分钟和秒超过59默认为59，第二个时间数字框分钟和秒超过59默认为59"
    )
    # @pytest.mark.run(order=1)
    def test_shift_addminutesnum(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage

        shift.click_add_button()  # 检查点击添加
        # 填写第一个日期数字的第二个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[2]//input',
            "345",
        )
        # 填写第一个日期数字的第三个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[3]//input',
            "345",
        )

        # 填写第二个日期数字的第二个第二个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[5]//input',
            "345",
        )
        # 填写第二个日期数字的第二个第三个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[6]//input',
            "345",
        )
        shift.click_button(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[5]//input'
        )

        # 获取表示顺序数字框
        shiftnum1 = shift.get_find_element_xpath(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[2]//input'
        ).get_attribute("value")
        shiftnum2 = shift.get_find_element_xpath(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[3]//input'
        ).get_attribute("value")
        shiftnum3 = shift.get_find_element_xpath(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[5]//input'
        ).get_attribute("value")
        shiftnum4 = shift.get_find_element_xpath(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[6]//input'
        ).get_attribute("value")
        assert (
            shiftnum1 == "59"
            and shiftnum2 == "59"
            and shiftnum3 == "59"
            and shiftnum4 == "59"
        )
        assert not shift.has_fail_message()

    @allure.story("第一个时间数字框不允许超过第二个时间数字框 添加失败")
    # @pytest.mark.run(order=1)
    def test_shift_adddateminnum_comparison(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage

        shift.click_add_button()  # 检查点击添加
        # 填写第一个日期数字的第一个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[1]//input',
            "23",
        )
        # 填写第一个日期数字的第二个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[2]//input',
            "30",
        )
        # 填写第一个日期数字的第三个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[3]//input',
            "30",
        )

        # 填写第二个日期数字的第二个一个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[4]//input',
            "8",
        )
        # 填写第二个日期数字的第二个第二个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[5]//input',
            "0",
        )
        # 填写第二个日期数字的第二个第三个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[6]//input',
            "0",
        )
        shift.click_button(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/parent::div/div[2]/button'
        )
        data = driver.find_elements(
            By.XPATH,
            '(//span[text()="时间"])[2]/ancestor::table/parent::div/parent::div/div[2]/table//tr[1]',
        )
        assert len(data) == 0
        assert not shift.has_fail_message()

    @allure.story("第一个时间数字框不允许超过第二个时间数字框  添加成功")
    # @pytest.mark.run(order=1)
    def test_shift_adddateminnum_successes(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage

        shift.click_add_button()  # 检查点击添加
        # 填写第一个日期数字的第一个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[1]//input',
            "6",
        )
        # 填写第一个日期数字的第二个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[2]//input',
            "30",
        )
        # 填写第一个日期数字的第三个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[3]//input',
            "30",
        )

        # 填写第二个日期数字的第二个一个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[4]//input',
            "12",
        )
        # 填写第二个日期数字的第二个第二个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[5]//input',
            "0",
        )
        # 填写第二个日期数字的第二个第三个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[6]//input',
            "0",
        )
        shift.click_button(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/parent::div/div[2]/button'
        )

        data = shift.get_find_element_xpath(
            '(//span[text()="时间"])[1]/ancestor::table/parent::div/parent::div/div[2]/table//tr[1]//td[1]'
        )
        assert data.text == "1"
        assert not shift.has_fail_message()

    @allure.story("下拉框选择成功")
    # @pytest.mark.run(order=1)
    def test_shift_addsel(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage

        shift.click_add_button()  # 检查点击添加
        # 显示颜色下拉框
        shift.click_button('(//label[text()="显示颜色"])[1]/parent::div//i')
        # 显示颜色
        shift.click_button('//span[text()="RGB(100,255,178)"]')
        # 获取下拉框数据
        shiftsel = shift.get_find_element_xpath(
            '(//label[text()="显示颜色"])[1]/parent::div//input['
            '@class="ivu-select-input"]'
        ).get_attribute("value")
        assert shiftsel == "RGB(100,255,178)", f"预期{shiftsel}"
        assert not shift.has_fail_message()

    @allure.story("添加数据成功")
    # @pytest.mark.run(order=1)
    def test_shift_addsuccess(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage

        shift.click_add_button()  # 检查点击添加
        # 输入班次代码
        shift.enter_texts('(//label[text()="代码"])[1]/parent::div//input', "111")
        # 点击确定
        shift.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        adddata = shift.get_find_element_xpath(
            '(//span[text()="111"])[1]/ancestor::tr[1]/td[2]'
        )
        assert adddata.text == "111", f"预期数据是111，实际得到{adddata}"
        assert not shift.has_fail_message()

    @allure.story("添加数据重复")
    # @pytest.mark.run(order=1)
    def test_shift_addrepeat(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage

        shift.click_add_button()  # 检查点击添加
        # 输入班次代码
        shift.enter_texts('(//label[text()="代码"])[1]/parent::div//input', "111")
        # 点击确定
        shift.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        # 等待弹窗出现（最多等10秒）
        error_popup = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                ("xpath", '//div[text()=" 记录已存在,请检查！ "]')
            )
        )
        assert (
            error_popup.text == "记录已存在,请检查！"
        ), f"预期数据是记录已存在,请检查，实际得到{error_popup}"
        assert not shift.has_fail_message()

    @allure.story("取消删除数据")
    # @pytest.mark.run(order=1)
    def test_shift_delcancel(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage

        # 定位内容为‘111’的行
        shift.click_button('(//span[text()="111"])[1]/ancestor::tr[1]/td[2]')
        shift.click_del_button()  # 点击删除
        # 点击取消
        shift.get_find_element_class("ivu-btn-text").click()
        # 定位内容为‘111’的行
        shiftdata = shift.get_find_element_xpath(
            '(//span[text()="111"])[1]/ancestor::tr[1]/td[2]'
        )
        assert shiftdata.text == "111", f"预期{shiftdata}"
        assert not shift.has_fail_message()

    @allure.story("添加测试数据成功")
    # @pytest.mark.run(order=1)
    def test_shift_addsuccess1(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage

        shift.click_add_button()  # 检查点击添加
        # 输入班次代码
        shift.enter_texts('(//label[text()="代码"])[1]/parent::div//input', "1修改代码")

        # 填写第一个日期数字的第一个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[1]//input',
            "6",
        )
        # 填写第一个日期数字的第二个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[2]//input',
            "30",
        )
        # 填写第一个日期数字的第三个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[3]//input',
            "30",
        )

        # 填写第二个日期数字的第二个一个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[4]//input',
            "12",
        )
        # 填写第二个日期数字的第二个第二个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[5]//input',
            "0",
        )
        # 填写第二个日期数字的第二个第三个时间数字框
        shift.enter_texts(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/div[6]//input',
            "0",
        )
        shift.click_button(
            '//label[text()="时间"]/ancestor::div[1]//div[@class="left"]/parent::div/div[2]/button'
        )

        timedata = shift.get_find_element_xpath(
            '(//span[text()="时间"])[1]/ancestor::table/parent::div/parent::div/div[2]/table//tr[1]//td[2]//span'
        ).text

        # 点击确定
        shift.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        adddata = shift.get_find_element_xpath(
            '(//span[text()="1修改代码"])[1]/ancestor::tr[1]/td[3]'
        ).text
        assert adddata == timedata
        assert not shift.has_fail_message()

    @allure.story("修改班次代码重复")
    # @pytest.mark.run(order=1)
    def test_shift_editrepeat(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage

        # 选中晚班班次代码
        shift.click_button('(//span[text()="1修改代码"])[1]')
        # 点击修改按钮
        shift.click_edi_button()
        # 班次代码输入白班
        sleep(1)
        shift.enter_texts('(//label[text()="代码"])[1]/parent::div//input', "111")
        # 点击确定
        shift.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        # 等待弹窗出现（最多等10秒）
        error_popup = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                ("xpath", '//div[text()=" 记录已存在,请检查！ "]')
            )
        )
        assert error_popup.text == "记录已存在,请检查！", f"预期数据{error_popup}"
        assert not shift.has_fail_message()

    @allure.story("修改班次代码成功")
    # @pytest.mark.run(order=1)
    def test_shift_editcodesuccess(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage

        # 选中产包装班次代码
        shift.click_button('(//span[text()="1修改代码"])[1]')
        # 点击修改按钮
        shift.click_edi_button()
        sleep(1)
        # 生成随机数
        random_int = random.randint(1, 10)
        text = "1修改代码" + f"{random_int}"
        # 班次代码输入
        shift.enter_texts('(//label[text()="代码"])[1]/parent::div//input', f"{text}")
        # 点击确定
        shift.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 定位表格内容
        shiftdata = shift.get_find_element_xpath(
            '(//span[contains(text(),"1修改代码")])[1]'
        ).text
        assert shiftdata == text, f"预期{shiftdata}"
        assert not shift.has_fail_message()

    @allure.story("把修改后的班次代码改回来")
    # @pytest.mark.run(order=1)
    def test_shift_editcodesuccess2(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage

        # 选中修改代码班次代码
        shift.click_button('(//span[contains(text(),"1修改代码")])[1]')
        # 点击修改按钮
        shift.click_edi_button()
        # 班次代码输入
        shift.enter_texts('(//label[text()="代码"])[1]/parent::div//input', "1修改代码")
        # 点击确定
        shift.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 定位表格内容
        shiftdata = shift.get_find_element_xpath('(//span[text()="1修改代码"])[1]').text
        assert shiftdata == "1修改代码", f"预期{shiftdata}"
        assert not shift.has_fail_message()

    @allure.story("修改时间成功")
    # @pytest.mark.run(order=1)
    def test_shift_edittimesuccess(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage

        # 选中修改代码班次代码
        shift.click_button('(//span[contains(text(),"1修改代码")])[1]')
        # 点击修改按钮
        shift.click_edi_button()
        # 点击编辑按钮
        shift.click_button('//span[text()="编辑"]')
        time1 = shift.get_find_element_xpath(
            '//div[@class="shift-time p-b-10 flex-j-c-between"]/div[1]//input'
        )
        time1.send_keys(Keys.CONTROL, "a")
        time1.send_keys(Keys.BACK_SPACE)
        shift.enter_texts(
            '//div[@class="shift-time p-b-10 flex-j-c-between"]/div[1]//input', "5"
        )

        time2 = shift.get_find_element_xpath(
            '//div[@class="shift-time p-b-10 flex-j-c-between"]/div[2]//input'
        )
        time2.send_keys(Keys.CONTROL, "a")
        time2.send_keys(Keys.BACK_SPACE)
        shift.enter_texts(
            '//div[@class="shift-time p-b-10 flex-j-c-between"]/div[2]//input', "5"
        )

        time3 = shift.get_find_element_xpath(
            '//div[@class="shift-time p-b-10 flex-j-c-between"]/div[3]//input'
        )
        time3.send_keys(Keys.CONTROL, "a")
        time3.send_keys(Keys.BACK_SPACE)
        shift.enter_texts(
            '//div[@class="shift-time p-b-10 flex-j-c-between"]/div[3]//input', "5"
        )

        time4 = shift.get_find_element_xpath(
            '//div[@class="shift-time p-b-10 flex-j-c-between"]/div[4]//input'
        )
        time4.send_keys(Keys.CONTROL, "a")
        time4.send_keys(Keys.BACK_SPACE)
        shift.enter_texts(
            '//div[@class="shift-time p-b-10 flex-j-c-between"]/div[4]//input', "8"
        )

        time5 = shift.get_find_element_xpath(
            '//div[@class="shift-time p-b-10 flex-j-c-between"]/div[5]//input'
        )
        time5.send_keys(Keys.CONTROL, "a")
        time5.send_keys(Keys.BACK_SPACE)
        shift.enter_texts(
            '//div[@class="shift-time p-b-10 flex-j-c-between"]/div[5]//input', "5"
        )

        time6 = shift.get_find_element_xpath(
            '//div[@class="shift-time p-b-10 flex-j-c-between"]/div[6]//input'
        )
        time6.send_keys(Keys.CONTROL, "a")
        time6.send_keys(Keys.BACK_SPACE)
        shift.enter_texts(
            '//div[@class="shift-time p-b-10 flex-j-c-between"]/div[6]//input', "5"
        )

        shift.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )
        sleep(1)

        timedata = shift.get_find_element_xpath(
            '(//span[text()="时间"])[1]/ancestor::table/parent::div/parent::div/div[2]/table//tr[1]//td[2]//span'
        ).text

        # 点击确定
        shift.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        adddata = shift.get_find_element_xpath(
            '(//span[text()="1修改代码"])[1]/ancestor::tr[1]/td[3]'
        ).text
        assert adddata == timedata and adddata == "05:05:05-08:05:05"
        assert not shift.has_fail_message()

    @allure.story("修改显示颜色成功")
    # @pytest.mark.run(order=1)
    def test_shift_editcolorsuccess(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage

        # 选中班次代码
        shift.click_button('(//span[text()="1修改代码"])[1]')
        # 点击修改按钮
        shift.click_edi_button()
        sleep(1)
        # 生成随机数
        random_int = random.randint(1, 10)

        # 显示颜色下拉框
        shift.click_button('(//label[text()="显示颜色"])[1]/parent::div//i')
        # 显示颜色
        shift.click_button(f'//span[text()="{random_int}"]')
        # 获取下拉框数据
        shiftsel = shift.get_find_element_xpath(
            '(//label[text()="显示颜色"])[1]/parent::div//input[@class="ivu-select-input"]'
        ).get_attribute("value")
        # 点击确定
        shift.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        shiftautoGenerateFlag = shift.get_find_element_xpath(
            '(//span[text()="1修改代码"])[1]/ancestor::tr/td[4]/div'
        ).text
        assert shiftautoGenerateFlag == shiftsel
        assert not shift.has_fail_message()

    @allure.story("删除测试数据成功")
    # @pytest.mark.run(order=1)
    def test_shift_delsuccess1(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage

        # 定位内容为‘1修改代码’的行
        shift.click_button('(//span[text()="1修改代码"])[1]/ancestor::tr[1]/td[2]')
        shift.click_del_button()  # 点击删除
        # 点击确定
        # 找到共同的父元素
        parent = shift.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        sleep(1)
        # 定位内容为‘1修改代码’的行
        shiftdata = driver.find_elements(
            By.XPATH, '(//span[text()="1修改代码"])[1]/ancestor::tr[1]/td[2]'
        )
        assert len(shiftdata) == 0
        assert not shift.has_fail_message()

    @allure.story("刷新成功")
    # @pytest.mark.run(order=1)
    def test_shift_refreshsuccess(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage
        sleep(1)  # 等待页面加载
        # 班次代码筛选框输入123
        shift.enter_texts(
            '//p[text()="代码"]/ancestor::div[2]//input', "123"
        )
        shift.click_ref_button()
        shifttext = shift.get_find_element_xpath(
            '//p[text()="代码"]/ancestor::div[2]//input'
        ).text
        assert shifttext == "", f"预期{shifttext}"
        assert not shift.has_fail_message()

    @allure.story("查询代码成功")
    # @pytest.mark.run(order=1)
    def test_shift_selectcodesuccess(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage

        # 点击查询
        shift.click_sel_button()
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
        # 点击班次代码
        shift.click_button('//div[text()="代码" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        shift.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        shift.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        shift.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "111",
        )
        sleep(1)

        # 点击确认
        shift.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行是否为白班
        shiftcode = shift.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]'
        ).text
        # 定位第二行没有数据
        shiftcode2 = driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][2]/td[2]',
        )
        assert shiftcode == "111" and len(shiftcode2) == 0
        assert not shift.has_fail_message()

    @allure.story("输入全部数据，添加保存成功")
    # @pytest.mark.run(order=1)
    def test_shift_addall(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage
        data_list = ["全部数据", "20"]
        shift.click_add_button()  # 检查点击添加
        shift.add_input_all(data_list[0], data_list[1])
        sleep(1)
        shift.enter_texts(
            '//p[text()="代码"]/ancestor::div[2]//input', data_list[0]
        )
        # 缩放到最小（例如 60%）
        driver.execute_script("document.body.style.zoom='0.6'")
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
        bef_text = ['全部数据', '20:20:20-21:20:20', 'RGB(100,255,178)', '全部数据', f'{DateDriver.username}', '2025']
        assert len(columns_text) == len(bef_text), f"长度不一致：actual={len(columns_text)}, expected={len(bef_text)}"
        for i, (a, e) in enumerate(zip(columns_text, bef_text), start=1):
            if i == 6:
                assert str(e) in str(a), f"第7项包含断言失败：'{e}' not in '{a}'"
            else:
                assert a == e, f"第{i + 1}项不一致：actual='{a}', expected='{e}'"
        assert not shift.has_fail_message()

    @allure.story("重新打开浏览器，数据还存在")
    # @pytest.mark.run(order=1)
    def test_shift_restart(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage
        code = '全部数据'
        shift.enter_texts(
            '//p[text()="代码"]/ancestor::div[2]//input', code
        )
        # 缩放到最小（例如 60%）
        driver.execute_script("document.body.style.zoom='0.6'")
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
        bef_text = ['全部数据', '20:20:20-21:20:20', 'RGB(100,255,178)', '全部数据', f'{DateDriver.username}', '2025']
        assert len(columns_text) == len(bef_text), f"长度不一致：actual={len(columns_text)}, expected={len(bef_text)}"
        for i, (a, e) in enumerate(zip(columns_text, bef_text), start=1):
            if i == 6:
                assert str(e) in str(a), f"第7项包含断言失败：'{e}' not in '{a}'"
            else:
                assert a == e, f"第{i + 1}项不一致：actual='{a}', expected='{e}'"
        assert not shift.has_fail_message()

    @allure.story("删除全部input数据成功")
    # @pytest.mark.run(order=1)
    def test_shift_delall(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage
        code = '全部数据'
        shift.enter_texts(
            '//p[text()="代码"]/ancestor::div[2]//input', code
        )
        sleep(2)

        # 定位内容为‘全部数据’的行
        shift.click_button('//tr[./td[2][.//span[text()="全部数据"]]]/td[2]')
        shift.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        parent = shift.get_find_element_class("ivu-modal-confirm-footer")

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
        assert not shift.has_fail_message()

    @allure.story("删除数据成功,删除数据删除布局成功")
    # @pytest.mark.run(order=1)
    def test_shift_delsuccess2(self, login_to_shift):
        driver = login_to_shift  # WebDriver 实例
        shift = ShiftPage(driver)  # 用 driver 初始化 ShiftPage
        layout = "测试布局A"

        # 定位内容为‘111’的行
        shift.click_button('(//span[text()="111"])[1]/ancestor::tr[1]/td[2]')
        shift.click_del_button()  # 点击删除
        # 点击确定
        # 找到共同的父元素
        parent = shift.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        sleep(1)
        # 定位内容为‘111’的行
        shiftdata = driver.find_elements(
            By.XPATH, '(//span[text()="111"])[1]/ancestor::tr[1]/td[2]'
        )

        # 获取目标 div 元素，这里的目标是具有特定文本的 div
        target_div = shift.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        )

        # 获取父容器下所有 div
        # 这一步是为了确定目标 div 在其父容器中的位置
        parent_div = shift.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon" and ./div[text()=" {layout} "]]'
        )
        all_children = parent_div.find_elements(By.XPATH, "./div")

        # 获取目标 div 的位置索引（从0开始）
        # 这里是为了后续操作，比如点击目标 div 相关的按钮
        index = all_children.index(target_div)
        print(f"目标 div 是第 {index + 1} 个 div")  # 输出 3（如果从0开始则是2）
        sleep(2)
        shift.click_button(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]//i'
        )
        # 根据目标 div 的位置，点击对应的“删除布局”按钮
        shift.click_button(f'(//li[text()="删除布局"])[{index + 1}]')
        sleep(2)
        # 点击确认删除的按钮
        shift.click_button('//button[@class="ivu-btn ivu-btn-primary ivu-btn-large"]')
        # 等待一段时间，确保删除操作完成
        sleep(1)

        # 再次查找页面上是否有目标 div，以验证是否删除成功
        after_layout = driver.find_elements(
            By.XPATH, f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        )
        assert len(shiftdata) == 0 == len(after_layout)
        assert not shift.has_fail_message()
