import logging
import random
from datetime import date
from time import sleep

import allure
import pytest
from selenium.common.exceptions import WebDriverException
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from Pages.itemsPage.adds_page import AddsPages
from Pages.itemsPage.changeR_page import ChangeR
from Pages.itemsPage.login_page import LoginPage
from Utils.data_driven import DateDriver
from Utils.driver_manager import create_driver, safe_quit, capture_screenshot


@pytest.fixture  # (scope="class")这个参数表示整个测试类共用同一个浏览器，默认一个用例执行一次
def login_to_changespec():
    """初始化并返回 driver"""
    date_driver = DateDriver()
    # 初始化 driver
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
    page.click_button('(//span[text()="计划管理"])[1]')  # 点击计划管理
    page.click_button('(//span[text()="计划切换定义"])[1]')  # 点击计划切换定义
    page.click_button('(//span[text()="生产特征1切换"])[1]')  # 点击生产特征1切换
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("生产特征切换表测试用例")
@pytest.mark.run(order=14)
class TestChangeSpecPage:
    @allure.story("添加生产特征切换信息 不填写数据点击确认 不允许提交，添加新布局，")
    # @pytest.mark.run(order=1)
    def test_changespec_addfail(self, login_to_changespec):
        driver = login_to_changespec  # WebDriver 实例
        change = ChangeR(driver)  # 用 driver 初始化 ChangeR

        layout = "测试布局A"
        change.add_layout(layout)
        # 获取布局名称的文本元素
        name = change.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        ).text

        change.click_add_button()
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        # 资源
        inputresource_box = change.get_find_element_xpath(
            '(//label[text()="资源"])[1]/parent::div//input'
        )
        # 前生产特征
        inputitem_box1 = change.get_find_element_xpath(
            '(//label[text()="前生产特征"])[1]/parent::div//input'
        )
        # 后资源
        inputitem_box2 = change.get_find_element_xpath(
            '(//label[text()="后生产特征"])[1]/parent::div//input'
        )

        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        borderresource_color = inputresource_box.value_of_css_property("border-color")
        borderitem_color1 = inputitem_box1.value_of_css_property("border-color")
        borderitem_color2 = inputitem_box2.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert (
            borderresource_color == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{borderresource_color}"
        assert (
            borderitem_color1 == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{borderitem_color1}"
        assert (
            borderitem_color2 == expected_color
        ), f"预期边框颜色为{expected_color}, 但得到{borderitem_color2}"
        assert name == layout
        assert not change.has_fail_message()

    @allure.story("添加生产特征切换信息 填写资源不填写前生产特征和后生产特征 不允许提交")
    # @pytest.mark.run(order=1)
    def test_changespec_addresourcefail(self, login_to_changespec):
        driver = login_to_changespec  # WebDriver 实例
        change = ChangeR(driver)  # 用 driver 初始化 ChangeR

        change.click_add_button()
        # 点击资源
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[1]'
        )
        # 勾选框
        random_int = random.randint(3, 8)
        sleep(1)
        change.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int}]')
        sleep(1)
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 前生产特征
        inputitem_box1 = change.get_find_element_xpath(
            '(//label[text()="前生产特征"])[1]/parent::div//input'
        )
        # 后生产特征
        inputitem_box2 = change.get_find_element_xpath(
            '(//label[text()="后生产特征"])[1]/parent::div//input'
        )

        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        borderitem_color1 = inputitem_box1.value_of_css_property("border-color")
        borderitem_color2 = inputitem_box2.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert borderitem_color1 == expected_color, f"预期边框颜色为{borderitem_color1}"
        assert borderitem_color2 == expected_color, f"预期边框颜色为{borderitem_color1}"
        assert not change.has_fail_message()

    @allure.story("添加生产特征切换信息 填写前生产特征和后生产特征不填写资源 不允许提交")
    # @pytest.mark.run(order=1)
    def test_changespec_additemfail(self, login_to_changespec):
        driver = login_to_changespec  # WebDriver 实例
        change = ChangeR(driver)  # 用 driver 初始化 ChangeR

        change.click_add_button()
        # 资源
        input_box = change.get_find_element_xpath(
            '(//label[text()="资源"])[1]/parent::div//input'
        )

        # 点击前生产特征
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[2]'
        )
        # 勾选框
        random_int = random.randint(3, 8)
        sleep(1)
        change.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int}]')
        sleep(1)
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 点击后生产特征
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[3]'
        )
        # 勾选框
        random_int1 = random.randint(3, 8)
        sleep(1)
        change.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int1}]')
        sleep(1)
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 点击确定
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        border_color = input_box.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert border_color == expected_color, f"预期边框颜色为{border_color}"
        assert not change.has_fail_message()

    @allure.story("添加资源切换信息 填写资源，前生产特征和后生产特征 不填写切换时间 不允许提交")
    # @pytest.mark.run(order=1)
    def test_changespec_addtimefails(self, login_to_changespec):
        driver = login_to_changespec  # WebDriver 实例
        change = ChangeR(driver)  # 用 driver 初始化 ChangeR

        change.click_add_button()
        # 点击资源
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[1]'
        )
        # 勾选框
        random_int = random.randint(3, 8)
        change.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int}]')
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 点击前生产特征
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[2]'
        )
        # 勾选框
        random_int = random.randint(3, 8)
        sleep(1)
        change.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int}]')
        sleep(1)
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 点击后生产特征
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[3]'
        )
        # 勾选框
        random_int1 = random.randint(3, 8)
        sleep(1)
        change.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int1}]')
        sleep(1)
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        sleep(1)
        # 清除切换时间数字
        time = change.get_find_element_xpath(
            '(//label[text()="切换时间(分钟)"])[1]/parent::div//input'
        )
        time.send_keys(Keys.BACK_SPACE, "a")
        sleep(1)

        # 点击确定
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(1)
        time = change.get_find_element_xpath(
            '(//label[text()="切换时间(分钟)"])[1]/parent::div/div/div'
        )
        border_color = time.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert border_color == expected_color, f"预期边框颜色为{border_color}"
        assert not change.has_fail_message()

    @allure.story("添加资源切换信息 填写资源，前生产特征和后生产特征，填写切换时间，不填写优先度 不允许提交")
    # @pytest.mark.run(order=1)
    def test_changespec_addprioritizationfail(self, login_to_changespec):
        driver = login_to_changespec  # WebDriver 实例
        change = ChangeR(driver)  # 用 driver 初始化 ChangeR

        change.click_add_button()
        # 点击资源
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[1]'
        )
        # 勾选框
        random_int = random.randint(3, 8)
        change.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int}]')
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 点击前生产特征
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[2]'
        )
        # 勾选框
        random_int = random.randint(3, 8)
        sleep(1)
        change.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int}]')
        sleep(1)
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 点击后生产特征
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[3]'
        )
        # 勾选框
        random_int1 = random.randint(3, 8)
        sleep(1)
        change.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int1}]')
        sleep(1)
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        sleep(1)
        # 清除优先度
        prioritization = change.get_find_element_xpath(
            '(//label[text()="优先度"])[1]/parent::div//input'
        )
        prioritization.send_keys(Keys.BACK_SPACE, "a")
        sleep(1)

        # 点击确定
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(1)
        time = change.get_find_element_xpath(
            '(//label[text()="优先度"])[1]/parent::div/div/div'
        )
        border_color = time.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert border_color == expected_color, f"预期边框颜色为{border_color}"
        assert not change.has_fail_message()

    @allure.story("数字文本框 只允许填写数字")
    # @pytest.mark.run(order=1)
    def test_changespec_addnum(self, login_to_changespec):
        driver = login_to_changespec  # WebDriver 实例
        change = ChangeR(driver)  # 用 driver 初始化 ChangeR

        change.click_add_button()  # 检查点击添加
        # 切换时间
        time = change.get_find_element_xpath(
            '//label[text()="切换时间(分钟)"]/ancestor::div[1]//input[1]'
        )
        # 删除资源量输入框
        time.send_keys(Keys.BACK_SPACE, "a")
        # 输入文本
        change.enter_texts(
            '//label[text()="切换时间(分钟)"]/ancestor::div[1]//input[1]',
            "1文字abc。？~1+1-=3",
        )
        sleep(1)
        # 获取表示顺序数字框
        changeRnum = change.get_find_element_xpath(
            '//label[text()="切换时间(分钟)"]/ancestor::div[1]//input[1]'
        ).get_attribute("value")
        assert changeRnum == "1113", f"预期{changeRnum}"
        assert not change.has_fail_message()

    @allure.story("添加数据成功")
    # @pytest.mark.run(order=1)
    def test_changespec_addweeksuccess(self, login_to_changespec):
        driver = login_to_changespec  # WebDriver 实例
        change = ChangeR(driver)  # 用 driver 初始化 ChangeR
        code1 = "11"
        code2 = "22"
        change.click_add_button()
        # 点击资源
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[1]'
        )
        # 勾选框
        rows = driver.find_elements(By.XPATH, f"//table[.//tr[td[3]//span[text()='{code1}']]]//tr")
        for index, row in enumerate(rows, start=1):
            td3_text = row.find_elements(By.TAG_NAME, "td")[2].text.strip()
            if f"{code1}" in td3_text:
                print(f"✅ 找到匹配行，行号为：{index}")

                # 3. 使用这个行号 idx 构造另一个 XPath
                target_xpath = f'(//table[.//tr[{index}]/td[2][contains(@class,"col--checkbox")]])[2]//tr[{index}]/td[2]/div/span'
                target_element = change.get_find_element_xpath(target_xpath)

                # 4. 操作目标元素
                target_element.click()
                break  # 如果只处理第一个匹配行，可以 break
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 点击前生产特征
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[2]'
        )

        # 勾选框
        rows = driver.find_elements(By.XPATH, f'//div[@class="h-0px flex-grow1"]//table[@class="vxe-table--body" and .//tr[td[3] and .//span[text()="{code2}"]]]//tr')
        for index, row in enumerate(rows, start=1):
            td3_text = row.find_elements(By.TAG_NAME, "td")[2].text.strip()
            if f"{code2}" == td3_text:
                print(f"✅ 找到匹配行，行号为：{index}")

                # 3. 使用这个行号 idx 构造另一个 XPath
                target_xpath = f'//div[@class="h-0px flex-grow1"]//table[@class="vxe-table--body"]//tr[{index}]/td[2]//div/span'
                # 点击前重新获取元素，防止 stale
                try:
                    target_element = change.get_find_element_xpath(target_xpath)
                    target_element.click()
                except StaleElementReferenceException:
                    print("⚠️ 元素过期，重新获取一次")
                    target_element = change.get_find_element_xpath(target_xpath)
                    target_element.click()

        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 点击后生产特征
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[3]'
        )
        # 勾选框
        change.click_button('//div[@class="h-0px flex-grow1"]//table[@class="vxe-table--body"]//tr[3]/td[2]//div/span')
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 获取勾选的资源
        resource = change.get_find_element_xpath(
            '(//label[text()="资源"])[1]/parent::div//input'
        ).get_attribute("value")
        # 获取前资源
        item1 = change.get_find_element_xpath(
            '(//label[text()="前生产特征"])[1]/parent::div//input'
        ).get_attribute("value")
        sleep(1)
        # 获取后资源
        item2 = change.get_find_element_xpath(
            '(//label[text()="后生产特征"])[1]/parent::div//input'
        ).get_attribute("value")
        sleep(1)

        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(1)
        change.click_button(
            '//div[p[text()="更新时间"]]/div[1]'
        )
        sleep(1)
        change.click_button(
            '//div[p[text()="更新时间"]]/div[1]'
        )

        addresource = change.get_find_element_xpath(
            f'(//span[text()="{resource}"])[1]/ancestor::tr[1]/td[2]'
        ).text
        additem1 = change.get_find_element_xpath(
            f'(//span[text()="{resource}"])[1]/ancestor::tr[1]/td[3]'
        ).text
        additem2 = change.get_find_element_xpath(
            f'(//span[text()="{resource}"])[1]/ancestor::tr[1]/td[4]'
        ).text
        assert addresource == resource and additem1 == item1 and additem2 == item2
        assert not change.has_fail_message()

    @allure.story("添加数据重复")
    # @pytest.mark.run(order=1)
    def test_changespec_addrepe(self, login_to_changespec):
        driver = login_to_changespec  # WebDriver 实例
        change = ChangeR(driver)  # 用 driver 初始化 ChangeR
        code1 = "11"
        code2 = "22"
        change.click_add_button()
        # 点击资源
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[1]'
        )
        # 勾选框
        rows = driver.find_elements(By.XPATH, f"//table[.//tr[td[3]//span[text()='{code1}']]]//tr")
        for index, row in enumerate(rows, start=1):
            td3_text = row.find_elements(By.TAG_NAME, "td")[2].text.strip()
            if f"{code1}" in td3_text:
                print(f"✅ 找到匹配行，行号为：{index}")

                # 3. 使用这个行号 idx 构造另一个 XPath
                target_xpath = f'(//table[.//tr[{index}]/td[2][contains(@class,"col--checkbox")]])[2]//tr[{index}]/td[2]/div/span'
                target_element = change.get_find_element_xpath(target_xpath)

                # 4. 操作目标元素
                target_element.click()
                break  # 如果只处理第一个匹配行，可以 break
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 点击前生产特征
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[2]'
        )

        # 勾选框
        rows = driver.find_elements(By.XPATH,
                                    f'//div[@class="h-0px flex-grow1"]//table[@class="vxe-table--body" and .//tr[td[3] and .//span[text()="{code2}"]]]//tr')
        for index, row in enumerate(rows, start=1):
            td3_text = row.find_elements(By.TAG_NAME, "td")[2].text.strip()
            if f"{code2}" == td3_text:
                print(f"✅ 找到匹配行，行号为：{index}")

                # 3. 使用这个行号 idx 构造另一个 XPath
                target_xpath = f'//div[@class="h-0px flex-grow1"]//table[@class="vxe-table--body"]//tr[{index}]/td[2]//div/span'
                # 点击前重新获取元素，防止 stale
                try:
                    target_element = change.get_find_element_xpath(target_xpath)
                    target_element.click()
                except StaleElementReferenceException:
                    print("⚠️ 元素过期，重新获取一次")
                    target_element = change.get_find_element_xpath(target_xpath)
                    target_element.click()

        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 点击后生产特征
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[3]'
        )
        # 勾选框
        change.click_button(
            '//div[@class="h-0px flex-grow1"]//table[@class="vxe-table--body"]//tr[3]/td[2]//div/span')
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(1)
        eles = driver.find_elements(By.XPATH, '//div[text()=" 记录已存在,请检查！ "]')
        assert len(eles) == 1
        assert not change.has_fail_message()

    @allure.story("删除数据成功")
    # @pytest.mark.run(order=1)
    def test_changespec_delsuccess2(self, login_to_changespec):
        driver = login_to_changespec  # WebDriver 实例
        change = ChangeR(driver)  # 用 driver 初始化 ChangeR
        code1 = "11"
        code2 = "22"
        # 定位第一行
        change.click_button(
            f'//table[@xid="2" and @class="vxe-table--body"]//tr[td[2]//span[text()="{code1}"] and td[3]//span[text()="{code2}"]]//td[2]'
        )
        changedata1 = change.get_find_element_xpath(
            '(//span[contains(text(),"条记录")])[1]'
        ).text
        change.click_del_button()  # 点击删除
        # 点击确定
        # 找到共同的父元素
        parent = change.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        # 定位
        changedata = change.get_find_element_xpath(
            '(//span[contains(text(),"条记录")])[1]'
        ).text
        sleep(1)
        ele = driver.find_elements(
            By.XPATH,
            f'//table[@xid="2" and @class="vxe-table--body"]//tr[td[2]//span[text()="{code1}"] and td[3]//span[text()="{code2}"]]//td[2]'
        )
        assert (
                changedata != changedata1 and
                len(ele) == 0
        ), f"删除后的数据{changedata}，删除前的数据{changedata1}"
        assert not change.has_fail_message()

    @allure.story("取消删除数据")
    # @pytest.mark.run(order=1)
    def test_changespec_delcancel(self, login_to_changespec):
        driver = login_to_changespec  # WebDriver 实例
        change = ChangeR(driver)  # 用 driver 初始化 ChangeR
        # 定位第一行
        change.click_button(
            '//div[@class="vxe-table--body-wrapper body--wrapper"]/table[@class="vxe-table--body"]//tr[1]//td[2]'
        )
        changedata1 = change.get_find_element_xpath(
            '//div[@class="vxe-table--body-wrapper body--wrapper"]/table[@class="vxe-table--body"]//tr[1]//td[2]'
        ).text
        change.click_del_button()  # 点击删除
        # 点击取消
        change.get_find_element_class("ivu-btn-text").click()
        # 定位第一行
        changedata = change.get_find_element_xpath(
            '//div[@class="vxe-table--body-wrapper body--wrapper"]/table[@class="vxe-table--body"]//tr[1]//td[2]'
        ).text
        assert changedata1 == changedata, f"预期{changedata}"
        assert not change.has_fail_message()

    @allure.story("修改资源切换资源成功")
    # @pytest.mark.run(order=1)
    def test_changespec_editcodesuccess(self, login_to_changespec):
        driver = login_to_changespec  # WebDriver 实例
        change = ChangeR(driver)  # 用 driver 初始化 ChangeR
        # 定位第一行
        change.click_button(
            '//div[@class="vxe-table--body-wrapper body--wrapper"]/table[@class="vxe-table--body"]//tr[1]//td[2]'
        )
        # 点击修改按钮
        change.click_edi_button()
        # 点击资源
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[1]'
        )

        # 勾选框
        random_int = random.randint(3, 8)
        change.click_button(
            '(//span[@class="vxe-checkbox--icon iconfont icon-fuxuankuangdaiding"])[2]'
        )
        change.click_button(
            '(//span[@class="vxe-checkbox--icon vxe-icon-checkbox-checked-fill"])[2]'
        )
        change.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int}]')

        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )
        sleep(1)
        # 获取勾选的资源代码
        resource = change.get_find_element_xpath(
            '(//label[text()="资源"])[1]/parent::div//input'
        ).get_attribute("value")

        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(1)
        change.click_button(
            '//div[p[text()="更新时间"]]/div[1]'
        )
        sleep(1)
        change.click_button(
            '//div[p[text()="更新时间"]]/div[1]'
        )
        adddata = change.get_find_element_xpath(
            f'(//span[text()="{resource}"])[1]/ancestor::tr[1]/td[2]'
        ).text
        assert adddata == resource
        assert not change.has_fail_message()

    @allure.story("修改切换优先度成功")
    # @pytest.mark.run(order=1)
    def test_changespec_editprioritizationsuccess(self, login_to_changespec):
        driver = login_to_changespec  # WebDriver 实例
        change = ChangeR(driver)  # 用 driver 初始化 ChangeR
        # 定位第一行
        change.click_button(
            '//div[@class="vxe-table--body-wrapper body--wrapper"]/table[@class="vxe-table--body"]//tr[1]//td[2]'
        )
        # 点击修改按钮
        change.click_edi_button()

        # 优先度
        random_int = random.randint(1, 100)
        prioritizationinput = change.get_find_element_xpath(
            '(//label[text()="优先度"])[1]/parent::div//input'
        )
        prioritizationinput.send_keys(Keys.CONTROL, "a")
        prioritizationinput.send_keys(Keys.BACK_SPACE)
        sleep(1)
        change.enter_texts(
            '(//label[text()="优先度"])[1]/parent::div//input', f"{random_int}"
        )
        prioritization = change.get_find_element_xpath(
            '(//label[text()="优先度"])[1]/parent::div//input'
        ).get_attribute("value")

        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(1)
        change.click_button(
            '//div[p[text()="更新时间"]]/div[1]'
        )
        sleep(1)
        change.click_button(
            '//div[p[text()="更新时间"]]/div[1]'
        )
        adddata = change.get_find_element_xpath(
            '//div[@class="vxe-table--body-wrapper body--wrapper"]/table[@class="vxe-table--body"]//tr[1]//td[6]'
        ).text
        assert adddata == prioritization
        assert not change.has_fail_message()

    @allure.story("刷新成功")
    # @pytest.mark.run(order=1)
    def test_changespec_refreshsuccess(self, login_to_changespec):
        driver = login_to_changespec  # WebDriver 实例
        change = ChangeR(driver)  # 用 driver 初始化 ChangeR
        # 资源切换筛选框输入123
        change.enter_texts(
            '//p[text()="资源"]/ancestor::div[2]//input', "123"
        )
        change.click_ref_button()
        changeRtext = change.get_find_element_xpath(
            '//p[text()="资源"]/ancestor::div[2]//input'
        ).text
        assert changeRtext == "", f"预期{changeRtext}"
        assert not change.has_fail_message()

    @allure.story("查询资源成功")
    # @pytest.mark.run(order=1)
    def test_changespec_selectcodesuccess(self, login_to_changespec):
        driver = login_to_changespec  # WebDriver 实例
        change = ChangeR(driver)  # 用 driver 初始化 ChangeR
        sleep(2)
        after = change.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][3]/td[2]'
        ).text
        # 点击查询
        change.click_sel_button()
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
        # 点击资源切换代码
        change.click_button('//div[text()="资源" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        change.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        change.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        change.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            f"{after}",
        )
        sleep(1)

        # 点击确认
        change.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行是否为开料
        changeRcode = change.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]'
        )
        assert changeRcode.text == after
        assert not change.has_fail_message()

    @allure.story("输入全部数据，添加保存成功")
    # @pytest.mark.run(order=1)
    def test_changespec_addall(self, login_to_changespec):
        driver = login_to_changespec  # WebDriver 实例
        change = ChangeR(driver)  # 用 driver 初始化 ChangeR
        adds = AddsPages(driver)
        input_value = '11测试全部数据'
        change.click_add_button()
        text_list = [
            '//label[text()="备注"]/following-sibling::div//input',
        ]
        adds.batch_modify_input(text_list, input_value)

        value_bos = '(//div[@class="vxe-modal--body"]//table[@class="vxe-table--body"]//tr[1]/td[2])[2]/div/span'
        box_list = [
            '//label[text()="资源"]/following-sibling::div//i',
            '//label[text()="前生产特征"]/following-sibling::div//i',
            '//label[text()="后生产特征"]/following-sibling::div//i',
        ]
        adds.batch_modify_dialog_box(box_list, value_bos)
        resource_value = change.get_find_element_xpath('//label[text()="资源"]/following-sibling::div//input').get_attribute("value")

        code_value = '//span[text()="AdvanceAlongResourceWorkingTime"]'
        code_list = [
            '//label[text()="切换时间调整表达式"]/following-sibling::div//i',
        ]
        adds.batch_modify_code_box(code_list, code_value)

        input_num_value = '1'
        num_list = [
            '//label[text()="优先度"]/following-sibling::div//input',
            '//label[text()="切换时间(分钟)"]/following-sibling::div//input',
        ]
        adds.batch_modify_input(num_list, input_num_value)

        box_input_list = [xpath.replace("//i", "//input") for xpath in box_list]
        code_input_list = [xpath.replace("//i", "//input") for xpath in code_list]
        all_value = text_list + box_input_list + code_input_list + num_list
        len_num = len(all_value)
        before_all_value = adds.batch_acquisition_input(all_value)
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]//span[text()="确定"]')
        sleep(1)
        driver.refresh()
        sleep(3)
        num = adds.go_settings_page()
        sleep(2)
        change.click_button(
            '//div[p[text()="更新时间"]]/div[1]'
        )
        sleep(1)
        change.click_button(
            '//div[p[text()="更新时间"]]/div[1]'
        )
        change.click_button(
            f'(//div[@class="vxe-table--main-wrapper"])[2]//table[@class="vxe-table--body"]//tr/td[2][.//span[text()="{resource_value}"]]')
        sleep(1)
        change.click_edi_button()
        after_all_value = adds.batch_acquisition_input(all_value)
        username = change.get_find_element_xpath(
            '//label[text()="更新者"]/following-sibling::div//input').get_attribute(
            "value")
        updatatime = change.get_find_element_xpath(
            '//label[text()="更新时间"]/following-sibling::div//input').get_attribute("value")
        today_str = date.today().strftime('%Y/%m/%d')
        assert before_all_value == after_all_value and username == DateDriver().username and today_str in updatatime and int(
            num) == (int(len_num) + 2)
        assert all(before_all_value), "列表中存在为空或为假值的元素！"
        assert not change.has_fail_message()

    @allure.story("删除全部数据功")
    # @pytest.mark.run(order=1)
    def test_changespec_deleteall(self, login_to_changespec):
        driver = login_to_changespec  # WebDriver 实例
        change = ChangeR(driver)  # 用 driver 初始化 ChangeR
        change.click_button(
            '//div[p[text()="更新时间"]]/div[1]'
        )
        sleep(1)
        change.click_button(
            '//div[p[text()="更新时间"]]/div[1]'
        )
        sleep(1)
        changedata1 = change.get_find_element_xpath(
            '(//span[contains(text(),"条记录")])[1]'
        ).text
        change.click_button(
            '//div[@class="vxe-table--body-wrapper body--wrapper"]/table[@class="vxe-table--body"]//tr[1]//td[2]')
        change.click_del_button()
        # 点击确定
        # 找到共同的父元素
        parent = change.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        # 定位
        changedata = change.get_find_element_xpath(
            '(//span[contains(text(),"条记录")])[1]'
        ).text
        assert (
                changedata != changedata1
        ), f"删除后的数据{changedata}，删除前的数据{changedata1}"
        assert not change.has_fail_message()

    @allure.story("删除布局成功")
    # @pytest.mark.run(order=1)
    def test_changespec_delsuccesslayout(self, login_to_changespec):
        driver = login_to_changespec  # WebDriver 实例
        change = ChangeR(driver)  # 用 driver 初始化 ChangeR
        layout = "测试布局A"

        # 获取目标 div 元素，这里的目标是具有特定文本的 div
        target_div = change.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        )

        # 获取父容器下所有 div
        # 这一步是为了确定目标 div 在其父容器中的位置
        parent_div = change.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon" and ./div[text()=" {layout} "]]'
        )
        all_children = parent_div.find_elements(By.XPATH, "./div")

        # 获取目标 div 的位置索引（从0开始）
        # 这里是为了后续操作，比如点击目标 div 相关的按钮
        index = all_children.index(target_div)
        print(f"目标 div 是第 {index + 1} 个 div")  # 输出 3（如果从0开始则是2）
        sleep(2)
        change.click_button(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]//i'
        )
        # 根据目标 div 的位置，点击对应的“删除布局”按钮
        change.click_button(f'(//li[text()="删除布局"])[{index + 1}]')
        sleep(2)
        # 点击确认删除的按钮
        change.click_button('//button[@class="ivu-btn ivu-btn-primary ivu-btn-large"]')
        # 等待一段时间，确保删除操作完成
        sleep(1)
        # 再次查找页面上是否有目标 div，以验证是否删除成功
        after_layout = driver.find_elements(
            By.XPATH, f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        )
        assert 0 == len(after_layout)
        assert not change.has_fail_message()

