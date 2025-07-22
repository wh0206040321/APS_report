import random
from time import sleep

import allure
import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from Pages.itemsPage.login_page import LoginPage
from Pages.itemsPage.resource_page import ResourcePage
from Utils.data_driven import DateDriver
from Utils.driver_manager import create_driver, safe_quit


@pytest.fixture  # (scope="class")这个参数表示整个测试类共用同一个浏览器，默认一个用例执行一次
def login_to_resourcegroup():
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
    page.click_button('(//span[text()="资源组"])[1]')  # 点击资源组
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("资源组表测试用例")
@pytest.mark.run(order=7)
class TestResourceGroupPage:
    @allure.story("添加资源组信息 不填写数据点击确认 不允许提交，添加测试布局")
    # @pytest.mark.run(order=1)
    def test_resourcegroup_addfail(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        layout = "测试布局A"
        resource.add_layout(layout)

        # 获取布局名称的文本元素
        name = resource.get_find_element_xpath(
                f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
            ).text

        resource.click_add_button()
        # 资源组代码xpath
        input_box = resource.get_find_element_xpath(
            '(//label[text()="资源组代码"])[1]/parent::div//input'
        )
        # 资源组名称xpath
        inputname_box = resource.get_find_element_xpath(
            '(//label[text()="资源组名称"])[1]/parent::div//input'
        )
        resource.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
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
        assert not resource.has_fail_message()

    @allure.story("添加资源组信息，只填写资源代码，不填写资源名称，不允许提交")
    # @pytest.mark.run(order=2)
    def test_resourcegroup_addcodefail(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        resource.click_add_button()
        resource.enter_texts(
            '(//label[text()="资源组代码"])[1]/parent::div//input', "text1231"
        )
        resource.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        input_box = resource.get_find_element_xpath(
            '(//label[text()="资源组名称"])[1]/parent::div//input'
        )
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        border_color = input_box.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert (
            border_color == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{border_color}"
        assert not resource.has_fail_message()

    @allure.story("添加资源组信息，只填写资源名称，不填写资源代码，不允许提交")
    # @pytest.mark.run(order=3)
    def test_resourcegroup_addnamefail(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        resource.click_add_button()
        resource.enter_texts(
            '(//label[text()="资源组名称"])[1]/parent::div//input', "text1231"
        )
        sleep(1)
        # 点击确定
        resource.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        input_box = resource.get_find_element_xpath(
            '(//label[text()="资源组代码"])[1]/parent::div//input'
        )
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        border_color = input_box.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert (
            border_color == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{border_color}"
        assert not resource.has_fail_message()

    @allure.story("数字文本框 只允许填写数字")
    # @pytest.mark.run(order=1)
    def test_resourcegroup_addnum(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        resource.click_add_button()  # 检查点击添加
        # 数值特征数字框输入文字字母符号数字
        resource.enter_texts(
            '(//label[text()="数值特征1MAX"])[1]/parent::div//input',
            "1文字abc。？~1_2+3",
        )
        sleep(1)
        # 获取数值特征数字框
        resourcenum = resource.get_find_element_xpath(
            '(//label[text()="数值特征1MAX"])[1]/parent::div//input'
        ).get_attribute("value")
        assert resourcenum == "1123", f"预期{resourcenum}"
        assert not resource.has_fail_message()

    @allure.story("下拉框选择成功")
    # @pytest.mark.run(order=1)
    def test_resourcegroup_addsel(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        resource.click_add_button()  # 检查点击添加
        # 资源量制约下拉框
        resource.click_button(
            '(//label[text()="资源量制约"])[1]/parent::div//input[@class="ivu-select-input"]'
        )
        # 自动补充标志选择是(是库存+1对1制造)
        resource.click_button('//li[text()="按资源量分派"]')
        # 获取资源量制约下拉框
        resourcesel = resource.get_find_element_xpath(
            '(//label[text()="资源量制约"])[1]/parent::div//input[@class="ivu-select-input"]'
        ).get_attribute("value")
        assert resourcesel == "按资源量分派", f"预期{resourcesel}"
        assert not resource.has_fail_message()

    @allure.story("代码设计器选择成功，并且没有乱码")
    # @pytest.mark.run(order=1)
    def test_resourcegroup_addcodebox(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        resource.click_add_button()  # 检查点击添加
        # 点击代码设计器
        resource.click_button('(//label[text()="分割条件式"])[1]/parent::div//i')
        # 点击标准登录
        resource.click_button('(//div[text()=" 标准登录 "])[1]')
        # 首先，定位到你想要双击的元素
        element_to_double_click = driver.find_element(
            By.XPATH, '(//span[text()="分割数量在10以上，且中断时间超过1小时"])[1]'
        )
        # 创建一个 ActionChains 对象
        actions = ActionChains(driver)
        # 双击命令
        actions.double_click(element_to_double_click).perform()
        # 点击确认
        resource.click_button('(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]//span[text()="确定"]')
        # 获取分割条件式代码设计器文本框
        sleep(1)
        resourcecode = resource.get_find_element_xpath(
            '(//label[text()="分割条件式"])[1]/parent::div//input'
        ).get_attribute("value")
        assert (
            resourcecode
            == "ME.AssignedQty>=10&&1h<ME.SuspendEndTime[0]-ME.SuspendStartTime[0]"
        ), f"预期{resourcecode}"
        assert not resource.has_fail_message()

    @allure.story("添加数据成功")
    # @pytest.mark.run(order=1)
    def test_resourcegroup_addsuccess(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        resource.click_add_button()  # 检查点击添加
        # 输入资源组代码
        resource.enter_texts(
            '(//label[text()="资源组代码"])[1]/parent::div//input', "111"
        )
        resource.enter_texts(
            '(//label[text()="资源组名称"])[1]/parent::div//input', "111"
        )
        # 点击确定
        resource.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        adddata = resource.get_find_element_xpath(
            '(//span[text()="111"])[1]/ancestor::tr[1]/td[2]'
        ).text
        assert adddata == "111", f"预期数据是111，实际得到{adddata}"
        assert not resource.has_fail_message()

    @allure.story("添加数据重复")
    # @pytest.mark.run(order=1)
    def test_resourcegroup_addrepeat(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        resource.click_add_button()  # 检查点击添加
        # 输入资源组代码
        resource.enter_texts(
            '(//label[text()="资源组代码"])[1]/parent::div//input', "111"
        )
        resource.enter_texts(
            '(//label[text()="资源组名称"])[1]/parent::div//input', "切割机"
        )
        # 点击确定
        resource.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 获取重复弹窗文字
        error_popup = resource.get_find_element_xpath(
            '//div[text()=" 记录已存在,请检查！ "]'
        ).text
        assert (
            error_popup == "记录已存在,请检查！"
        ), f"预期数据是记录已存在,请检查，实际得到{error_popup}"
        assert not resource.has_fail_message()

    @allure.story("取消删除数据")
    # @pytest.mark.run(order=1)
    def test_resourcegroup_delcancel(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        # 定位内容为‘111’的行
        resource.click_button('(//span[text()="111"])[1]/ancestor::tr[1]/td[2]')
        resource.click_del_button()  # 点击删除
        sleep(1)
        # 点击取消
        resource.get_find_element_class("ivu-btn-text").click()
        sleep(1)
        # 定位内容为‘111’的行
        resourcedata = resource.get_find_element_xpath(
            '(//span[text()="111"])[1]/ancestor::tr[1]/td[2]'
        ).text
        assert resourcedata == "111", f"预期{resourcedata}"
        assert not resource.has_fail_message()

    @allure.story("添加测试数据成功")
    # @pytest.mark.run(order=1)
    def test_resourcegroup_addsuccess1(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        resource.click_add_button()  # 检查点击添加
        # 输入资源组代码
        resource.enter_texts(
            '(//label[text()="资源组代码"])[1]/parent::div//input', "1测试A"
        )
        resource.enter_texts(
            '(//label[text()="资源组名称"])[1]/parent::div//input', "1测试A"
        )
        # 点击确定
        resource.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        adddata = resource.get_find_element_xpath(
            '(//span[text()="1测试A"])[1]/ancestor::tr[1]/td[2]'
        ).text
        assert adddata == "1测试A", f"预期数据是1测试A，实际得到{adddata}"
        assert not resource.has_fail_message()

    @allure.story("修改资源代码重复")
    # @pytest.mark.run(order=1)
    def test_resourcegroup_editrepeat(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        # 选中1测试A代码
        resource.click_button('(//span[text()="1测试A"])[1]')
        # 点击修改按钮
        resource.click_edi_button()
        # 资源组代码输入111
        resource.enter_texts(
            '(//label[text()="资源组代码"])[1]/parent::div//input', "111"
        )
        # 点击确定
        resource.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 获取重复弹窗文字
        error_popup = resource.get_find_element_xpath(
            '//div[text()=" 记录已存在,请检查！ "]'
        ).text
        assert error_popup == "记录已存在,请检查！", f"预期数据{error_popup}"
        assert not resource.has_fail_message()

    @allure.story("修改资源组代码成功")
    # @pytest.mark.run(order=1)
    def test_resourcegroup_editcodesuccess(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        # 选中产品D资源组代码
        resource.click_button('(//span[text()="1测试A"])[1]')
        # 点击修改按钮
        resource.click_edi_button()
        sleep(1)
        # 生成随机数
        random_int = random.randint(1, 10)
        text = "1测试A" + f"{random_int}"
        # 资源组代码输入
        resource.enter_texts(
            '(//label[text()="资源组代码"])[1]/parent::div//input', f"{text}"
        )
        # 点击确定
        resource.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 定位表格内容
        resourcedata = resource.get_find_element_xpath(
            '(//span[contains(text(),"1测试A")])[1]'
        ).text
        assert resourcedata == text, f"预期{resourcedata}"
        assert not resource.has_fail_message()

    @allure.story("把修改后的资源组代码改回来")
    # @pytest.mark.run(order=1)
    def test_rresourcegroup_editcodesuccess2(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        # 选中资源代码
        resource.click_button('(//span[contains(text(),"1测试A")])[1]')
        # 点击修改按钮
        resource.click_edi_button()
        # 资源组代码输入
        resource.enter_texts(
            '(//label[text()="资源组代码"])[1]/parent::div//input', "1测试A"
        )
        # 点击确定
        resource.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 定位表格内容
        resourcedata = resource.get_find_element_xpath(
            '(//span[text()="1测试A"])[1]'
        ).text
        assert resourcedata == "1测试A", f"预期{resourcedata}"
        assert not resource.has_fail_message()

    @allure.story("修改资源组名称，资源量制约")
    # @pytest.mark.run(order=1)
    def test_resourcegroup_editnamesuccess(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        # 选中资源组代码
        resource.click_button('(//span[text()="1测试A"])[1]')
        # 点击修改按钮
        resource.click_edi_button()
        sleep(1)
        # 生成随机数
        random_int = random.randint(1, 10)
        text = "包装机" + f"{random_int}"
        # 输入修改的资源组名称
        resource.enter_texts(
            '(//label[text()="资源组名称"])[1]/parent::div//input', f"{text}"
        )
        # 获取修改好的值
        editname = resource.get_find_element_xpath(
            '(//label[text()="资源组名称"])[1]/parent::div//input'
        ).get_attribute("value")

        # 资源量制约下拉框
        resource.click_button(
            '(//label[text()="资源量制约"])[1]/parent::div//input[@class="ivu-select-input"]'
        )
        # 资源量制约选择(不制约)
        resource.click_button('//li[text()="不制约"]')
        # 获取资源量制约下拉框的值
        resourcesel = resource.get_find_element_xpath(
            '(//label[text()="资源量制约"])[1]/parent::div//input[@class="ivu-select-input"]'
        ).get_attribute("value")

        # 点击确定
        resource.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
        sleep(1)
        # 定位表格内容
        resourcename = resource.get_find_element_xpath(
            '(//span[text()="1测试A"])[1]/ancestor::tr/td[3]/div'
        ).text
        resourceautoGenerateFlag = resource.get_find_element_xpath(
            '(//span[text()="1测试A"])[1]/ancestor::tr/td[7]/div'
        ).text
        assert resourcename == editname and resourceautoGenerateFlag == resourcesel
        assert not resource.has_fail_message()

    @allure.story("刷新成功")
    # @pytest.mark.run(order=1)
    def test_resourcegroup_refreshsuccess(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        # 资源代码筛选框输入123
        resource.enter_texts(
            '//p[text()="资源组代码"]/ancestor::div[2]//input', "123"
        )
        resource.click_ref_button()
        resourcetext = resource.get_find_element_xpath(
            '//p[text()="资源组代码"]/ancestor::div[2]//input'
        ).text
        assert resourcetext == "", f"预期{resourcetext}"
        assert not resource.has_fail_message()

    @allure.story("查询资源组代码成功")
    # @pytest.mark.run(order=1)
    def test_resourcegroup_selectcodesuccess(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        # 点击查询
        resource.click_sel_button()
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
        # 点击资源组代码
        resource.click_button('//div[text()="资源组代码" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        resource.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        resource.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        resource.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "111",
        )
        sleep(1)

        # 点击确认
        resource.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行是否为111
        resourcecode = resource.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]'
        ).text
        # 定位第二行没有数据
        resourcecode2 = driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][2]/td[2]',
        )
        assert resourcecode == "111" and len(resourcecode2) == 0
        assert not resource.has_fail_message()

    @allure.story("没有数据时显示正常")
    # @pytest.mark.run(order=1)
    def test_resourcegroup_selectnodatasuccess(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        # 点击查询
        resource.click_sel_button()
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
        # 点击资源组代码
        resource.click_button('//div[text()="资源组代码" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        resource.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        resource.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        resource.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "没有数据",
        )
        sleep(1)

        # 点击确认
        resource.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        resourcecode = driver.find_elements(
            By.XPATH,
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]',
        )
        assert len(resourcecode) == 0
        assert not resource.has_fail_message()

    @allure.story("查询资源组名字成功")
    # @pytest.mark.run(order=1)
    def test_resourcegroup_selectnamesuccess(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage

        # 点击查询
        resource.click_sel_button()
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
        # 点击资源组名称
        resource.click_button('//div[text()="资源组名称" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        resource.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        resource.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        resource.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            "111",
        )
        sleep(1)

        # 点击确认
        resource.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行是否为检查
        resourcecode = resource.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[3]'
        ).text
        assert resourcecode == "111"
        assert not resource.has_fail_message()

    @allure.story("删除数据成功")
    # @pytest.mark.run(order=1)
    def test_resourcegroup_delsuccess(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage
        sleep(1)  # 等待页面加载
        # 定位内容为‘111’的行
        resource.click_button('(//span[text()="111"])[1]/ancestor::tr[1]/td[2]')
        resource.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        parent = resource.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        sleep(1)
        # 定位内容为‘111’的行
        resourcedata = driver.find_elements(
            By.XPATH, '(//span[text()="111"])[1]/ancestor::tr[1]/td[2]'
        )
        assert len(resourcedata) == 0
        assert not resource.has_fail_message()

    @allure.story("删除测试数据成功，删除布局成功")
    # @pytest.mark.run(order=1)
    def test_resourcegroup_delsuccess1(self, login_to_resourcegroup):
        driver = login_to_resourcegroup  # WebDriver 实例
        resource = ResourcePage(driver)  # 用 driver 初始化 resourcePage
        layout = "测试布局A"

        # 定位内容为‘1测试A’的行
        resource.click_button('(//span[text()="1测试A"])[1]/ancestor::tr[1]/td[2]')
        resource.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        parent = resource.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        sleep(1)
        # 定位内容为‘1测试A’的行
        resourcedata = driver.find_elements(
            By.XPATH, '(//span[text()="1测试A"])[1]/ancestor::tr[1]/td[2]'
        )

        # 获取目标 div 元素，这里的目标是具有特定文本的 div
        target_div = resource.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        )

        # 获取父容器下所有 div
        # 这一步是为了确定目标 div 在其父容器中的位置
        parent_div = resource.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon" and ./div[text()=" {layout} "]]'
        )
        all_children = parent_div.find_elements(By.XPATH, "./div")

        # 获取目标 div 的位置索引（从0开始）
        # 这里是为了后续操作，比如点击目标 div 相关的按钮
        index = all_children.index(target_div)
        print(f"目标 div 是第 {index + 1} 个 div")  # 输出 3（如果从0开始则是2）

        resource.click_button(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]//i'
        )
        # 根据目标 div 的位置，点击对应的“删除布局”按钮
        resource.click_button(f'(//li[text()="删除布局"])[{index + 1}]')
        sleep(2)
        # 点击确认删除的按钮
        resource.click_button('//button[@class="ivu-btn ivu-btn-primary ivu-btn-large"]')
        # 等待一段时间，确保删除操作完成
        sleep(1)

        # 再次查找页面上是否有目标 div，以验证是否删除成功
        after_layout = driver.find_elements(
            By.XPATH, f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        )
        assert len(resourcedata) == 0 and len(after_layout) == 0
        assert not resource.has_fail_message()
