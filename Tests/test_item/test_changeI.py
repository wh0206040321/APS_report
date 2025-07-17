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

from Pages.changeI_page import ChangeI
from Pages.login_page import LoginPage
from Utils.data_driven import DateDriver
from Utils.driver_manager import create_driver, safe_quit, all_driver_instances
from Utils.shared_data_util import SharedDataUtil


@pytest.fixture  # (scope="class")这个参数表示整个测试类共用同一个浏览器，默认一个用例执行一次
def login_to_changeI():
    """初始化并返回 driver"""
    driver_path = DateDriver().driver_path
    driver = create_driver(driver_path)
    driver.implicitly_wait(3)

    # 初始化登录页面
    page = LoginPage(driver)  # 初始化登录页面
    page.navigate_to(DateDriver().url)  # 导航到登录页面
    page.login(DateDriver().username, DateDriver().password, DateDriver().planning)
    page.click_button('(//span[text()="计划管理"])[1]')  # 点击计划管理
    page.click_button('(//span[text()="计划切换定义"])[1]')  # 点击计划切换定义
    page.click_button('(//span[text()="物品切换"])[1]')  # 点击物品切换
    yield driver  # 提供给测试用例使用
    safe_quit(driver)


@allure.feature("物品切换表测试用例")
@pytest.mark.run(order=12)
class TestChangeIPage:
    @allure.story("添加物品切换信息 不填写数据点击确认 不允许提交")
    # @pytest.mark.run(order=1)
    def test_changeI_addfail(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        changeI = ChangeI(driver)  # 用 driver 初始化 ChangeI
        layout = "测试布局A"
        changeI.add_layout()
        sleep(1)
        changeI.enter_texts(
            '//div[text()="当前布局:"]/following-sibling::div//input', f"{layout}"
        )
        checkbox1 = changeI.get_find_element_xpath(
            '//div[text()="是否默认启动:"]/following-sibling::label/span'
        )

        # 检查复选框是否未被选中
        if checkbox1.get_attribute("class") == "ivu-checkbox":
            # 如果未选中，则点击复选框进行选中
            changeI.click_button(
                '//div[text()="是否默认启动:"]/following-sibling::label/span'
            )
        sleep(1)

        changeI.click_button('(//div[text()=" 显示设置 "])[1]')
        # 获取是否可见选项的复选框元素
        checkbox2 = changeI.get_find_element_xpath(
            '(//div[./div[text()="是否可见:"]])[1]/label/span'
        )
        # 检查复选框是否未被选中
        if checkbox2.get_attribute("class") == "ivu-checkbox":
            # 如果未选中，则点击复选框进行选中
            changeI.click_button('(//div[./div[text()="是否可见:"]])[1]/label/span')
            # 点击确定按钮保存设置
            changeI.click_button('(//div[@class="demo-drawer-footer"])[3]/button[2]')
        else:
            # 如果已选中，直接点击确定按钮保存设置
            changeI.click_button('(//div[@class="demo-drawer-footer"])[3]/button[2]')
        # 获取布局名称的文本元素
        name = changeI.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        ).text

        changeI.click_add_button()
        changeI.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        # 资源
        inputresource_box = changeI.get_find_element_xpath(
            '(//label[text()="资源"])[1]/parent::div//input'
        )
        # 前品目
        inputitem_box1 = changeI.get_find_element_xpath(
            '(//label[text()="前品目"])[1]/parent::div//input'
        )
        # 后品目
        inputitem_box2 = changeI.get_find_element_xpath(
            '(//label[text()="后品目"])[1]/parent::div//input'
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
        assert layout == name
        assert not changeI.has_fail_message()

    @allure.story("添加物品切换信息 填写资源不填写前品目和后品目 不允许提交")
    # @pytest.mark.run(order=1)
    def test_changeI_addresourcefail(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        changeI = ChangeI(driver)  # 用 driver 初始化 ChangeI

        changeI.click_add_button()
        # 点击资源
        changeI.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[1]'
        )
        # 勾选框
        random_int = random.randint(3, 8)
        sleep(1)
        changeI.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int}]')
        sleep(1)
        changeI.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 前品目
        inputitem_box1 = changeI.get_find_element_xpath(
            '(//label[text()="前品目"])[1]/parent::div//input'
        )
        # 后品目
        inputitem_box2 = changeI.get_find_element_xpath(
            '(//label[text()="后品目"])[1]/parent::div//input'
        )

        changeI.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        borderitem_color1 = inputitem_box1.value_of_css_property("border-color")
        borderitem_color2 = inputitem_box2.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert borderitem_color1 == expected_color, f"预期边框颜色为{borderitem_color1}"
        assert borderitem_color2 == expected_color, f"预期边框颜色为{borderitem_color1}"
        assert not changeI.has_fail_message()

    @allure.story("添加物品切换信息 填写前品目和后品目不填写资源 不允许提交")
    # @pytest.mark.run(order=1)
    def test_changeI_additemfail(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        changeI = ChangeI(driver)  # 用 driver 初始化 ChangeI

        changeI.click_add_button()
        # 资源
        input_box = changeI.get_find_element_xpath(
            '(//label[text()="资源"])[1]/parent::div//input'
        )

        # 点击前品目
        changeI.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[2]'
        )
        # 勾选框
        random_int = random.randint(3, 8)
        sleep(1)
        changeI.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int}]')
        sleep(1)
        changeI.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 点击后品目
        changeI.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[3]'
        )
        # 勾选框
        random_int1 = random.randint(3, 9)
        sleep(1)
        changeI.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int1}]')
        sleep(1)
        changeI.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 点击确定
        changeI.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        # 断言边框颜色是否为红色（可以根据实际RGB值调整）
        sleep(1)
        border_color = input_box.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert border_color == expected_color, f"预期边框颜色为{border_color}"
        assert not changeI.has_fail_message()

    @allure.story("添加物品切换信息 填写资源，前品目和后品目 不填写切换时间 不允许提交")
    # @pytest.mark.run(order=1)
    def test_changeI_addtimefails(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        changeI = ChangeI(driver)  # 用 driver 初始化 ChangeI

        changeI.click_add_button()
        # 点击资源
        changeI.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[1]'
        )
        # 勾选框
        random_int = random.randint(3, 8)
        changeI.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int}]')
        changeI.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 点击前品目
        changeI.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[2]'
        )
        # 勾选框
        random_int = random.randint(3, 9)
        sleep(1)
        changeI.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int}]')
        sleep(1)
        changeI.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 点击后品目
        changeI.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[3]'
        )
        # 勾选框
        random_int1 = random.randint(3, 9)
        sleep(1)
        changeI.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int1}]')
        sleep(1)
        changeI.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        sleep(1)
        # 清除切换时间数字
        time = changeI.get_find_element_xpath(
            '(//label[text()="切换时间(分钟)"])[1]/parent::div//input'
        )
        time.send_keys(Keys.BACK_SPACE, "a")
        sleep(1)

        # 点击确定
        changeI.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(1)
        time = changeI.get_find_element_xpath(
            '(//label[text()="切换时间(分钟)"])[1]/parent::div/div/div'
        )
        border_color = time.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert border_color == expected_color, f"预期边框颜色为{border_color}"
        assert not changeI.has_fail_message()

    @allure.story("添加物品切换信息 填写资源，前品目和后品目 不填写切换时间 不允许提交")
    # @pytest.mark.run(order=1)
    def test_changeI_addprioritizationfail(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        changeI = ChangeI(driver)  # 用 driver 初始化 ChangeI

        changeI.click_add_button()
        # 点击资源
        changeI.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[1]'
        )
        # 勾选框
        random_int = random.randint(3, 8)
        changeI.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int}]')
        changeI.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 点击前品目
        changeI.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[2]'
        )
        # 勾选框
        random_int = random.randint(3, 9)
        sleep(1)
        changeI.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int}]')
        sleep(1)
        changeI.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 点击后品目
        changeI.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[3]'
        )
        # 勾选框
        random_int1 = random.randint(3, 9)
        sleep(1)
        changeI.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int1}]')
        sleep(1)
        changeI.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        sleep(1)
        # 清除切换时间数字
        prioritization = changeI.get_find_element_xpath(
            '(//label[text()="优先度"])[1]/parent::div//input'
        )
        prioritization.send_keys(Keys.BACK_SPACE, "a")
        sleep(1)

        # 点击确定
        changeI.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(1)
        time = changeI.get_find_element_xpath(
            '(//label[text()="优先度"])[1]/parent::div/div/div'
        )
        border_color = time.value_of_css_property("border-color")
        expected_color = "rgb(237, 64, 20)"  # 红色的 rgb 值
        assert border_color == expected_color, f"预期边框颜色为{border_color}"
        assert not changeI.has_fail_message()

    @allure.story("数字文本框 只允许填写数字")
    # @pytest.mark.run(order=1)
    def test_changeI_addnum(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        changeI = ChangeI(driver)  # 用 driver 初始化 ChangeI

        changeI.click_add_button()  # 检查点击添加
        # 切换时间
        time = changeI.get_find_element_xpath(
            '//label[text()="切换时间(分钟)"]/ancestor::div[1]//input[1]'
        )
        # 删除资源量输入框
        time.send_keys(Keys.BACK_SPACE, "a")
        # 输入文本
        changeI.enter_texts(
            '//label[text()="切换时间(分钟)"]/ancestor::div[1]//input[1]',
            "1文字abc。？~1+1-=3",
        )
        sleep(1)
        # 获取表示顺序数字框
        changeInum = changeI.get_find_element_xpath(
            '//label[text()="切换时间(分钟)"]/ancestor::div[1]//input[1]'
        ).get_attribute("value")
        assert changeInum == "1113", f"预期{changeInum}"
        assert not changeI.has_fail_message()

    @allure.story("输入全部数据，添加保存成功")
    # @pytest.mark.run(order=1)
    def test_changeI_addall(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        changeI = ChangeI(driver)  # 用 driver 初始化 ChangeI
        # 清空之前的共享数据
        SharedDataUtil.clear_data()
        data_list = 20
        changeI.click_add_button()  # 检查点击添加
        resource, item1, item2, time = changeI.add_input_all(data_list)
        # 保存数据
        SharedDataUtil.save_data(
            {"resource": resource, "item1": item1, "item2": item2, "time": time}
        )
        sleep(1)
        changeI.click_button(
            '//p[text()="更新时间"]/following-sibling::div'
        )
        sleep(1)
        changeI.click_button(
            '//p[text()="更新时间"]/following-sibling::div'
        )
        sleep(1)
        # 缩放到最小（例如 60%）
        driver.execute_script("document.body.style.zoom='0.6'")
        sleep(1)

        row_xpath = '//table[@xid="2" and @class="vxe-table--body"]//tr[1]'
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
        bef_text = [f'{resource}', f'{item1}', f'{item2}', f'{data_list}', f'{data_list}', f'{data_list}',
                    f'{DateDriver.username}', '2025', f'{time}']
        assert len(columns_text) == len(bef_text), f"长度不一致：actual={len(columns_text)}, expected={len(bef_text)}"
        for i, (a, e) in enumerate(zip(columns_text, bef_text), start=1):
            if i == 8:
                assert str(e) in str(a), f"第{i}项包含断言失败：'{e}' not in '{a}'"
            else:
                assert a == e, f"第{i + 1}项不一致：actual='{a}', expected='{e}'"
        assert not changeI.has_fail_message()

    @allure.story("重新打开浏览器，数据还存在")
    # @pytest.mark.run(order=1)
    def test_changeI_restart(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        changeI = ChangeI(driver)  # 用 driver 初始化 ChangeI
        data_list = "20"
        shared_data = SharedDataUtil.load_data()
        resource = shared_data.get("resource")
        item1 = shared_data.get("item1")
        item2 = shared_data.get("item2")
        time = shared_data.get("time")
        changeI.click_button(
            '//p[text()="更新时间"]/following-sibling::div'
        )
        sleep(1)
        changeI.click_button(
            '//p[text()="更新时间"]/following-sibling::div'
        )
        sleep(1)
        # 缩放到最小（例如 60%）
        driver.execute_script("document.body.style.zoom='0.6'")
        sleep(1)

        row_xpath = '//table[@xid="2" and @class="vxe-table--body"]//tr[1]'
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
        bef_text = [f'{resource}', f'{item1}', f'{item2}', f'{data_list}', f'{data_list}', f'{data_list}',
                    f'{DateDriver.username}', '2025', f'{time}']
        assert len(columns_text) == len(bef_text), f"长度不一致：actual={len(columns_text)}, expected={len(bef_text)}"
        for i, (a, e) in enumerate(zip(columns_text, bef_text), start=1):
            if i == 8:
                assert str(e) in str(a), f"第{i}项包含断言失败：'{e}' not in '{a}'"
            else:
                assert a == e, f"第{i}项不一致：actual='{a}', expected='{e}'"
        assert not changeI.has_fail_message()

    @allure.story("删除全部input数据成功")
    # @pytest.mark.run(order=1)
    def test_changeI_delall(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        changeI = ChangeI(driver)  # 用 driver 初始化 ChangeI

        changeI.click_button(
            '//p[text()="更新时间"]/following-sibling::div'
        )
        sleep(1)
        changeI.click_button(
            '//p[text()="更新时间"]/following-sibling::div'
        )
        sleep(1)
        # 定位
        changeI.click_button('//table[@xid="2" and @class="vxe-table--body"]//tr[1]/td[2]')
        changeIdata1 = changeI.get_find_element_xpath(
            '(//span[contains(text(),"条记录")])[1]'
        ).text
        changeI.click_del_button()  # 点击删除
        sleep(1)
        # 点击确定
        # 找到共同的父元素
        parent = changeI.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()
        sleep(1)
        changeIdata = changeI.get_find_element_xpath(
            '(//span[contains(text(),"条记录")])[1]'
        ).text
        assert (
                changeIdata != changeIdata1
        ), f"删除后的数据{changeIdata}，删除前的数据{changeIdata1}"
        assert not changeI.has_fail_message()

    @allure.story("添加数据成功")
    # @pytest.mark.run(order=1)
    def test_changeI_addweeksuccess(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        change = ChangeI(driver)  # 用 driver 初始化 ChangeR
        code1 = "11"
        code2 = "2339-50"
        change.click_add_button()
        # 点击资源
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[1]'
        )
        # 勾选框
        rows = driver.find_elements(By.XPATH, f"//table[.//tr[td[3]//span[text()='{code1}']]]//tr")
        for index, row in enumerate(rows, start=1):
            td3_text = row.find_elements(By.TAG_NAME, "td")[2].text.strip()
            if f"{code1}" == td3_text:
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

        # 点击前目录
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[2]'
        )
        sleep(3)
        # 勾选框
        rows = driver.find_elements(By.XPATH, '(//div[@class="vxe-table--body-wrapper body--wrapper"])[last()]//table//tr')
        for index, row in enumerate(rows, start=1):
            td3_text = row.find_elements(By.TAG_NAME, "td")[2].text.strip()
            if f"{code2}" in td3_text:
                print(f"✅ 找到匹配行，行号为：{index}")

                # 3. 使用这个行号 idx 构造另一个 XPath
                target_xpath = f'(//table[.//tr[{index}]/td[2][contains(@class,"col--checkbox")]])[2]//tr[{index}]/td[.//span[@class="vxe-cell--checkbox"]]//div/span'
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

        # 点击后目录
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[3]'
        )
        # 勾选框
        change.click_button(f'(//table[.//tr[3]/td[2][contains(@class,"col--checkbox")]])[2]//tr[3]/td[.//span[@class="vxe-cell--checkbox"]]//div/span')
        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )

        # 获取勾选的资源
        resource = change.get_find_element_xpath(
            '(//label[text()="资源"])[1]/parent::div//input'
        ).get_attribute("value")
        # 获取前目录
        item1 = change.get_find_element_xpath(
            '(//label[text()="前品目"])[1]/parent::div//input'
        ).get_attribute("value")
        sleep(1)
        # 获取后目录
        item2 = change.get_find_element_xpath(
            '(//label[text()="后品目"])[1]/parent::div//input'
        ).get_attribute("value")
        sleep(1)

        change.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(1)
        change.click_button(
            '(//div[@class="h-23px w-20px text-align-c cursor-pointer"])[8]'
        )
        sleep(1)
        change.click_button(
            '(//div[@class="h-23px w-20px text-align-c cursor-pointer"])[8]'
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
    def test_changeI_addrepe(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        change = ChangeI(driver)  # 用 driver 初始化 changeI
        code1 = "11"
        code2 = "2339-50"
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

        # 点击前目录
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[2]'
        )
        sleep(3)
        # 勾选框
        rows = driver.find_elements(By.XPATH,
                                    '(//div[@class="vxe-table--body-wrapper body--wrapper"])[last()]//table//tr')
        for index, row in enumerate(rows, start=1):
            td3_text = row.find_elements(By.TAG_NAME, "td")[2].text.strip()
            if f"{code2}" in td3_text:
                print(f"✅ 找到匹配行，行号为：{index}")

                # 3. 使用这个行号 idx 构造另一个 XPath
                target_xpath = f'(//table[.//tr[{index}]/td[2][contains(@class,"col--checkbox")]])[2]//tr[{index}]/td[.//span[@class="vxe-cell--checkbox"]]//div/span'
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

        # 点击后目录
        change.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[3]'
        )
        # 勾选框
        change.click_button(
            f'(//table[.//tr[3]/td[2][contains(@class,"col--checkbox")]])[2]//tr[3]/td[.//span[@class="vxe-cell--checkbox"]]//div/span')
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
    def test_changeI_delsuccess(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        change = ChangeI(driver)  # 用 driver 初始化 changeI
        code1 = "11"
        code2 = "2339-50"
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
    def test_changeI_delcancel(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        changeI = ChangeI(driver)  # 用 driver 初始化 ChangeI
        # 定位第一行
        changeI.click_button(
            '(//table[@style="margin-top: 0px; width: 980px; margin-left: 0px;"])[1]//tr[1]/td[2]'
        )
        changeIdata1 = changeI.get_find_element_xpath(
            '(//table[@style="margin-top: 0px; width: 980px; margin-left: 0px;"])[1]//tr[1]/td[2]'
        ).text
        changeI.click_del_button()  # 点击删除
        # 点击取消
        changeI.get_find_element_class("ivu-btn-text").click()
        # 定位第一行
        changeIdata = changeI.get_find_element_xpath(
            '(//table[@style="margin-top: 0px; width: 980px; margin-left: 0px;"])[1]//tr[1]/td[2]'
        ).text
        assert changeIdata1 == changeIdata, f"预期{changeIdata}"
        assert not changeI.has_fail_message()

    @allure.story("修改物品切换资源成功")
    # @pytest.mark.run(order=1)
    def test_changeI_editcodesuccess(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        changeI = ChangeI(driver)  # 用 driver 初始化 ChangeI
        # 定位第一行
        changeI.click_button(
            '(//table[@style="margin-top: 0px; width: 980px; margin-left: 0px;"])[1]//tr[1]/td[2]'
        )
        # 点击修改按钮
        changeI.click_edi_button()
        # 点击资源
        changeI.click_button(
            '(//i[@class="ivu-icon ivu-icon-md-albums ivu-input-icon ivu-input-icon-normal"])[1]'
        )

        # 勾选框
        random_int = random.randint(3, 8)
        changeI.click_button(
            '(//span[@class="vxe-checkbox--icon iconfont icon-fuxuankuangdaiding"])[2]'
        )
        changeI.click_button(
            '(//span[@class="vxe-checkbox--icon vxe-icon-checkbox-checked-fill"])[2]'
        )
        changeI.click_button(f'(//span[@class="vxe-cell--checkbox"])[{random_int}]')

        changeI.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[2]/button[1]'
        )
        sleep(1)
        # 获取勾选的资源代码
        resource = changeI.get_find_element_xpath(
            '(//label[text()="资源"])[1]/parent::div//input'
        ).get_attribute("value")

        changeI.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(1)
        changeI.click_button(
            '(//div[@class="h-23px w-20px text-align-c cursor-pointer"])[8]'
        )
        sleep(1)
        changeI.click_button(
            '(//div[@class="h-23px w-20px text-align-c cursor-pointer"])[8]'
        )
        adddata = changeI.get_find_element_xpath(
            f'(//span[text()="{resource}"])[1]/ancestor::tr[1]/td[2]'
        ).text
        assert adddata == resource
        assert not changeI.has_fail_message()

    @allure.story("修改物品切换优先度成功")
    # @pytest.mark.run(order=1)
    def test_changeI_editprioritizationsuccess(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        changeI = ChangeI(driver)  # 用 driver 初始化 ChangeI
        # 定位第一行
        changeI.click_button(
            '(//table[@style="margin-top: 0px; width: 980px; margin-left: 0px;"])[1]//tr[1]/td[2]'
        )
        # 点击修改按钮
        changeI.click_edi_button()

        # 优先度
        random_int = random.randint(1, 100)
        prioritizationinput = changeI.get_find_element_xpath(
            '(//label[text()="优先度"])[1]/parent::div//input'
        )
        prioritizationinput.send_keys(Keys.CONTROL, "a")
        prioritizationinput.send_keys(Keys.BACK_SPACE)
        sleep(1)
        changeI.enter_texts(
            '(//label[text()="优先度"])[1]/parent::div//input', f"{random_int}"
        )
        prioritization = changeI.get_find_element_xpath(
            '(//label[text()="优先度"])[1]/parent::div//input'
        ).get_attribute("value")

        changeI.click_button(
            '(//div[@class="h-40px flex-justify-end flex-align-items-end b-t-s-d9e3f3"])[1]/button[1]'
        )
        sleep(1)
        changeI.click_button(
            '(//div[@class="h-23px w-20px text-align-c cursor-pointer"])[8]'
        )
        sleep(1)
        changeI.click_button(
            '(//div[@class="h-23px w-20px text-align-c cursor-pointer"])[8]'
        )
        adddata = changeI.get_find_element_xpath(
            '(//table[@style="margin-top: 0px; width: 980px; margin-left: 0px;"])[1]//tr[1]/td[6]'
        ).text
        assert adddata == prioritization
        assert not changeI.has_fail_message()

    @allure.story("刷新成功")
    # @pytest.mark.run(order=1)
    def test_changeI_refreshsuccess(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        changeI = ChangeI(driver)  # 用 driver 初始化 ChangeI
        # 物品切换筛选框输入123
        changeI.enter_texts(
            '//p[text()="资源"]/ancestor::div[2]//input', "123"
        )
        changeI.click_ref_button()
        changeItext = changeI.get_find_element_xpath(
            '//p[text()="资源"]/ancestor::div[2]//input'
        ).text
        assert changeItext == "", f"预期{changeItext}"
        assert not changeI.has_fail_message()

    @allure.story("查询资源成功")
    # @pytest.mark.run(order=1)
    def test_changeI_selectcodesuccess(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        changeI = ChangeI(driver)  # 用 driver 初始化 ChangeI
        ele = changeI.get_find_element_xpath(
            '//table[@xid=2 and @class="vxe-table--body"]//tr[2]/td[2]'
        ).text
        # 点击查询
        changeI.click_sel_button()
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
        # 点击物品切换代码
        changeI.click_button('//div[text()="资源" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击比较关系框
        changeI.click_button(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
        )
        sleep(1)
        # 点击=
        changeI.click_button('//div[text()="=" and contains(@optid,"opt_")]')
        sleep(1)
        # 点击输入数值
        changeI.enter_texts(
            '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
            ele,
        )
        sleep(1)

        # 点击确认
        changeI.click_button(
            '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[3]'
        )
        sleep(1)
        # 定位第一行是否为开料
        changeIcode = changeI.get_find_element_xpath(
            '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]'
        ).text
        assert changeIcode == ele
        assert not changeI.has_fail_message()

    @allure.story("删除布局成功")
    # @pytest.mark.run(order=1)
    def test_changeI_delete(self, login_to_changeI):
        driver = login_to_changeI  # WebDriver 实例
        changeI = ChangeI(driver)  # 用 driver 初始化 ChangeI
        layout = "测试布局A"
        # 获取目标 div 元素，这里的目标是具有特定文本的 div
        target_div = changeI.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        )
        # 获取父容器下所有 div
        # 这一步是为了确定目标 div 在其父容器中的位置
        parent_div = changeI.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon" and ./div[text()=" {layout} "]]'
        )
        all_children = parent_div.find_elements(By.XPATH, "./div")

        # 获取目标 div 的位置索引（从0开始）
        # 这里是为了后续操作，比如点击目标 div 相关的按钮
        index = all_children.index(target_div)
        print(f"目标 div 是第 {index + 1} 个 div")  # 输出 3（如果从0开始则是2）
        sleep(2)
        changeI.click_button(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]//i'
        )
        # 根据目标 div 的位置，点击对应的“删除布局”按钮
        changeI.click_button(f'(//li[text()="删除布局"])[{index + 1}]')
        sleep(2)
        # 点击确认删除的按钮
        changeI.click_button('//button[@class="ivu-btn ivu-btn-primary ivu-btn-large"]')
        # 等待一段时间，确保删除操作完成
        sleep(1)

        # 再次查找页面上是否有目标 div，以验证是否删除成功
        after_layout = driver.find_elements(
            By.XPATH, f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        )
        assert 0 == len(after_layout)
        assert not changeI.has_fail_message()
