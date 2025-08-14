# import random
# from time import sleep
#
# import allure
# import pytest
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
#
# from Pages.materialPage.warehouseLocation_page import WarehouseLocationPage
# from Pages.itemsPage.login_page import LoginPage
# from Utils.data_driven import DateDriver
# from Utils.driver_manager import create_driver, safe_quit, all_driver_instances
#
#
# @pytest.fixture(scope="module")
# def login_to_item():
#     """初始化并返回 driver"""
#     driver_path = DateDriver().driver_path
#     driver = create_driver(driver_path)
#     driver.implicitly_wait(3)
#
#     # 初始化登录页面
#     page = LoginPage(driver)  # 初始化登录页面
#     page.navigate_to(DateDriver().url)  # 导航到登录页面
#     page.login(DateDriver().username, DateDriver().password, DateDriver().planning)
#     page.click_button('(//span[text()="物控管理"])[1]')  # 点击计划管理
#     page.click_button('(//span[text()="物控基础数据"])[1]')  # 点击计划基础数据
#     page.click_button('(//span[text()="供应商配额"])[1]')  # 点击供应商配额
#     yield driver  # 提供给测试用例使用
#     safe_quit(driver)
#
#
# @allure.feature("供应商配额测试用例")
# @pytest.mark.run(order=117)
# class TestItemPage:
#     @pytest.fixture(autouse=True)
#     def setup(self, login_to_item):
#         self.driver = login_to_item
#         self.item = WarehouseLocationPage(self.driver)
#         # 必填新增输入框xpath
#         self.req_input_add_xpath_list = [
#             "//div[@id='p34nag46-7evf']//input",
#             "//div[@id='x1k7t87i-tvc3']//input",
#             "//div[@id='7z1rv7fs-trb6']//input",
#             "//div[@id='u2tgl5h9-otp1']//input"
#         ]
#         # 必填编辑输入框xpath
#         self.req_input_edit_xpath_list = [
#             "//div[@id='vvm9iqeg-tbx9']//input",
#             "//div[@id='e5s27hnn-1bee']//input",
#             "//div[@id='xa1b27y2-3ad1']//input",
#             "//div[@id='450asdnv-buor']//input"
#         ]
#
#         # 必填新增日期xpath
#         self.req_date_add_xpath_list = ["//div[@id='p5b7jm60-veaq']//input", "//div[@id='cl9uutxm-4iwp']//input"]
#         # 必填编辑日期xpath
#         self.req_date_edit_xpath_list = ["//div[@id='kyt4bqre-7me0']//input", "//div[@id='pvh788fq-2g5u']//input"]
#
#         # 全部新增输入框xpath
#         self.all_input_add_xpath_list = [
#             "//div[@id='p34nag46-7evf']//input",
#             "//div[@id='x1k7t87i-tvc3']//input",
#             "//div[@id='o7c9sdve-vat3']//input",
#             "//div[@id='7z1rv7fs-trb6']//input",
#             "//div[@id='13j55ae1-8hj2']//input",
#             "//div[@id='u2tgl5h9-otp1']//input",
#             "//div[@id='ctfddy1k-hbmj']//input",
#             "//div[@id='zxc6ccwu-bnwe']//input",
#             "//div[@id='15qig6pt-sj1x']//input",
#             "//div[@id='vtxj45fl-aisi']//input",
#             "//div[@id='owcpuvmy-it09']//input",
#             "//div[@id='06giwjn5-paij']//input",
#             "//div[@id='69p938gi-8t8g']//input",
#             "//div[@id='pez84iac-hqov']//input",
#             "//div[@id='430cwjpr-7ja0']//input",
#             "//div[@id='egffq655-hmom']//input",
#             "//div[@id='v37polqo-hvji']//input",
#             "//div[@id='x8cw4z28-h20d']//input",
#             "//div[@id='tqs9hw9y-p2iw']//input",
#             "//div[@id='x0lzodb5-z6o2']//input",
#             "//div[@id='yn6jl4x2-3qd0']//input",
#             "//div[@id='bhbv8kgo-ii8r']//input",
#             "//div[@id='w78gtakt-i7sc']//input",
#             "//div[@id='cregu5ru-ntm9']//input",
#             "//div[@id='bnnxkovb-0axb']//input",
#             "//div[@id='1i3b0g5r-g2ew']//input",
#             "//div[@id='sc1ufdsi-b5qh']//input",
#             "//div[@id='l5zxkq3r-1iy5']//input",
#             "//div[@id='tl22a7er-fqaq']//input",
#             "//div[@id='t0mf4dzw-02ym']//input",
#             "//div[@id='hymhbalf-0h3d']//input",
#             "//div[@id='fba4wnmv-24tz']//input",
#             "//div[@id='43pfex9g-mlbn']//input",
#             "//div[@id='dan12xz9-fipn']//input",
#             "//div[@id='z2o1a2nz-oai0']//input",
#             "//div[@id='jdd3gu9w-vmak']//input",
#             "//div[@id='6hakdgsp-inn3']//input",
#             "//div[@id='75kj1lgn-art5']//input",
#             "//div[@id='mr9xr6nk-hjuj']//input",
#             "//div[@id='8e7zmjf6-maik']//input",
#             "//div[@id='vlny9yeq-f73q']//input",
#             "//div[@id='s40nqrjk-2jrg']//input",
#             "//div[@id='bktr9sma-30d9']//input",
#             "//div[@id='8sd7ff14-ub9z']//input",
#             "//div[@id='w6730iur-vs1h']//input",
#             "//div[@id='0z8smrh5-i97v']//input",
#             "//div[@id='1kdvyv9j-zq70']//input",
#             "//div[@id='rs94o2zt-874t']//input",
#             "//div[@id='by97fez4-0pw8']//input",
#             "//div[@id='ynl43ole-a2mv']//input",
#             "//div[@id='7gvinb18-91ol']//input"
#         ]
#         # 全部编辑输入框xpath
#         self.all_input_edit_xpath_list = [
#             "//div[@id='p34nag46-7evf']//input",
#             "//div[@id='ywz9q11i-sp3b']//input",
#             "//div[@id='u2tgl5h9-otp1']//input",
#             "//div[@id='izykzohi-1l5u']//input",
#             "//div[@id='ctfddy1k-hbmj']//input",
#             "//div[@id='7z1rv7fs-trb6']//input",
#             "//div[@id='u9i1q4uf-3oli']//input",
#             "//div[@id='1xvizeqn-gffj']//input",
#             "//div[@id='e67g7odw-v396']//input",
#             "//div[@id='z0h20cps-xzrs']//input",
#             "//div[@id='35lc2nk6-812s']//input",
#             "//div[@id='hguo4esk-gii0']//input",
#             "//div[@id='989l7loi-6nc4']//input",
#             "//div[@id='8nwpr6jl-sqt5']//input",
#             "//div[@id='z0pnhx2y-7qx3']//input",
#             "//div[@id='izx0sysf-otie']//input",
#             "//div[@id='0t8pfkrw-y5i1']//input"
#         ]
#         # 全部新增日期xpath
#         self.all_date_add_xpath_list = [
#             "//div[@id='dlmc4h3z-eofa']//input",
#             "//div[@id='l7p1eln5-w34j']//input",
#             "//div[@id='54xpaxv5-kcvd']//input",
#             "//div[@id='dsosvk7u-fg07']//input",
#             "//div[@id='fyqeuxkw-hani']//input",
#             "//div[@id='7pwkrz9l-r5zu']//input",
#             "//div[@id='qucmz24h-wri3']//input"
#         ]
#         # 全部编辑日期xpath
#         self.all_date_edit_xpath_list = [
#             "//div[@id='dlmc4h3z-eofa']//input",
#             "//div[@id='l7p1eln5-w34j']//input",
#             "//div[@id='54xpaxv5-kcvd']//input",
#             "//div[@id='dsosvk7u-fg07']//input",
#             "//div[@id='fyqeuxkw-hani']//input",
#             "//div[@id='7pwkrz9l-r5zu']//input",
#             "//div[@id='qucmz24h-wri3']//input"
#         ]
#
#     @allure.story("添加供应商配额信息 不填写数据点击确认 不允许提交")
#     # @pytest.mark.run(order=1)
#     def test_warehouselocation_addfail(self, login_to_item):
#         # 点击新增按钮
#         self.item.click_add_button()
#         # 点击确定
#         self.item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
#         sleep(1)
#         # 声明必填项的xpath和判断的边框颜色
#         color_value = "rgb(255, 0, 0)"
#         # 获取必填项公共方法判断颜色的结果
#         val = self.item.add_none(self.req_input_add_xpath_list, color_value)
#         assert val
#         assert not self.item.has_fail_message()
#
#     @allure.story("添加供应商配额信息，有多个必填只填写一项，不允许提交")
#     # @pytest.mark.run(order=2)
#     def test_item_addcodefail(self, login_to_item):
#         # 点击新增按钮
#         self.item.click_add_button()
#         # 输入第一个必填项
#         self.item.enter_texts("//div[@id='p34nag46-7evf']//input", "text1231")
#         # 点击确定
#         self.item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
#         sleep(1)
#         # 声明必填项的xpath和判断的边框颜色
#         xpath_list = [
#             "//div[@id='ywz9q11i-sp3b']//input",
#             "//div[@id='l7p1eln5-w34j']//input"
#         ]
#         color_value = "rgb(255, 0, 0)"
#         # 获取必填项公共方法判断颜色的结果
#         val = self.item.add_none(xpath_list, color_value)
#         assert val
#         assert not self.item.has_fail_message()
#
#     @allure.story("添加必填数据成功")
#     # @pytest.mark.run(order=1)
#     def test_item_addsuccess(self, login_to_item):
#
#         self.item.click_add_button()  # 检查点击添加
#         # 输入框要修改的值
#         text_str = "111"
#         date_str = "2025/07/23 00:00:00"
#         sleep(1)
#         # 批量修改输入框
#         self.item.batch_modify_input(self.req_input_add_xpath_list, text_str)
#         self.item.batch_modify_input(self.req_date_add_xpath_list, date_str)
#
#         sleep(1)
#         # 点击确定
#         self.item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
#         sleep(1)
#         # 选中新增行
#         self.item.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
#         # 点击编辑按钮
#         self.item.click_edi_button()
#         sleep(1)
#         # 批量获取输入框的value
#         input_values = self.item.batch_acquisition_input(self.req_input_edit_xpath_list, text_str)
#         # 批量获取日期选择框的value
#         input_values2 = self.item.batch_acquisition_input(self.req_date_edit_xpath_list, date_str)
#
#         sleep(1)
#         assert (
#                 len(self.req_input_add_xpath_list) == len(input_values) and
#                 len(self.req_date_add_xpath_list) == len(input_values2)
#         )
#         assert not self.item.has_fail_message()
#
#     @allure.story("添加数据重复")
#     # @pytest.mark.run(order=1)
#     def test_item_addrepeat(self, login_to_item):
#
#         self.item.click_add_button()  # 检查点击添加
#
#         # 输入框要修改的值
#         text_str = "111"
#         date_str = "2025/07/23 00:00:00"
#
#         sleep(1)
#         # 批量修改输入框
#         self.item.batch_modify_input(self.req_input_add_xpath_list, text_str)
#         self.item.batch_modify_input(self.req_date_add_xpath_list, date_str)
#
#         sleep(1)
#         # 点击确定
#         self.item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
#         sleep(1)
#         # 获取重复弹窗文字
#         error_popup = self.item.get_find_element_xpath(
#             '//div[text()=" 记录已存在,请检查！ "]'
#         ).text
#         assert (
#             error_popup == "记录已存在,请检查！"
#         ), f"预期数据是记录已存在,请检查，实际得到{error_popup}"
#         assert not self.item.has_fail_message()
#
#     @allure.story("取消删除数据")
#     # @pytest.mark.run(order=1)
#     def test_item_delcancel(self, login_to_item):
#
#         # 定位内容为‘111’的行
#         self.item.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
#         self.item.click_del_button()  # 点击删除
#         sleep(1)
#         # 点击取消
#         self.item.click_button('//button[@class="ivu-btn ivu-btn-text"]')
#         sleep(1)
#         # 定位内容为‘111’的行
#         itemdata = self.item.get_find_element_xpath(
#             '//tr[./td[2][.//span[text()="111"]]]/td[2]'
#         ).text
#         assert itemdata == "111", f"预期{itemdata}"
#         assert not self.item.has_fail_message()
#
#     @allure.story("添加测试数据")
#     # @pytest.mark.run(order=1)
#     def test_item_addsuccess1(self, login_to_item):
#
#         self.item.click_add_button()  # 检查点击添加
#         # 输入框要修改的值
#         text_str = "222"
#         date_str = "2025/07/23 00:00:00"
#
#         sleep(1)
#         # 批量修改输入框
#         self.item.batch_modify_input(self.req_input_add_xpath_list, text_str)
#         self.item.batch_modify_input(self.req_date_add_xpath_list, date_str)
#
#         sleep(1)
#         # 点击确定
#         self.item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
#         sleep(1)
#         # 选中新增行
#         self.item.click_button('//tr[./td[2][.//span[text()="222"]]]/td[2]')
#         # 点击编辑按钮
#         self.item.click_edi_button()
#         sleep(1)
#         # 批量获取输入框的value
#         input_values = self.item.batch_acquisition_input(self.req_input_edit_xpath_list, text_str)
#         # 批量获取日期选择框的value
#         input_values2 = self.item.batch_acquisition_input(self.req_date_edit_xpath_list, date_str)
#
#         sleep(1)
#         assert (
#                 len(self.req_input_add_xpath_list) == len(input_values) and
#                 len(self.req_date_add_xpath_list) == len(input_values2)
#         )
#         assert not self.item.has_fail_message()
#
#     @allure.story("修改测试数据成功")
#     # @pytest.mark.run(order=1)
#     def test_item_editcodesuccess(self, login_to_item):
#
#         # 输入框要修改的值
#         text_str = "333"
#         date_str = "2025/07/23 00:00:00"
#         # 输入框的xpath
#
#
#         # 选中刚刚新增的测试数据
#         self.item.click_button('//tr[./td[2][.//span[text()="222"]]]/td[2]')
#         # 点击修改按钮
#         self.item.click_edi_button()
#         sleep(1)
#
#         # 批量修改输入框
#         self.item.batch_modify_input(self.req_input_edit_xpath_list, text_str)
#         self.item.batch_modify_input(self.req_date_edit_xpath_list, date_str)
#
#         sleep(1)
#         # 点击确定
#         self.item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
#         sleep(1)
#         # 选中刚刚编辑的数据
#         self.item.click_button('//tr[./td[2][.//span[text()="333"]]]/td[2]')
#         # 点击编辑按钮
#         self.item.click_edi_button()
#         sleep(1)
#         # 批量获取输入框的value
#         input_values = self.item.batch_acquisition_input(self.req_input_edit_xpath_list, text_str)
#         input_values2 = self.item.batch_acquisition_input(self.req_date_edit_xpath_list, date_str)
#         sleep(1)
#         assert (
#                 len(self.req_input_edit_xpath_list) == len(input_values) and
#                 len(self.req_date_edit_xpath_list) == len(input_values2)
#         )
#         assert not self.item.has_fail_message()
#
#     @allure.story("修改数据重复")
#     # @pytest.mark.run(order=1)
#     def test_item_editrepeat(self, login_to_item):
#
#         # 选中1测试A工厂代码
#         self.item.click_button('//tr[./td[2][.//span[text()="333"]]]/td[2]')
#         # 点击修改按钮
#         self.item.click_edi_button()
#
#         # 物料代码等输入111
#         text_str = "111"
#         self.item.batch_modify_input(self.req_input_edit_xpath_list, text_str)
#         # 点击确定
#         self.item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
#         sleep(1)
#         # 获取重复弹窗文字
#         error_popup = self.item.get_find_element_xpath(
#             '//div[text()=" 记录已存在,请检查！ "]'
#         ).text
#         assert error_popup == "记录已存在,请检查！", f"预期数据{error_popup}"
#         assert not self.item.has_fail_message()
#
#     @allure.story("删除数据成功")
#     # @pytest.mark.run(order=1)
#     def test_item_delsuccess1(self, login_to_item):
#         # 定位内容为‘111’的行
#         self.item.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
#         self.item.click_del_button()  # 点击删除
#         sleep(1)
#         # 点击确定
#         # 找到共同的父元素
#         parent = self.item.get_find_element_class("ivu-modal-confirm-footer")
#
#         # 获取所有button子元素
#         all_buttons = parent.find_elements(By.TAG_NAME, "button")
#
#         # 选择需要的button 第二个确定按钮
#         second_button = all_buttons[1]
#         second_button.click()
#         self.item.click_ref_button()
#         sleep(1)
#         # 定位内容为‘111’的行
#         itemdata = self.driver.find_elements(
#             By.XPATH, '//tr[./td[2][.//span[text()="111"]]]/td[2]'
#         )
#         assert len(itemdata) == 0
#         assert not self.item.has_fail_message()
#
#     @allure.story("编辑全部选项成功")
#     # @pytest.mark.run(order=1)
#     def test_item_editnamesuccess(self, login_to_item):
#
#         # 输入框要修改的值
#         text_str = "111"
#         date_str = "2025/07/23 00:00:00"
#
#         # 选中编辑数据
#         self.item.click_button('//tr[./td[2][.//span[text()="333"]]]/td[2]')
#         # 点击修改按钮
#         self.item.click_edi_button()
#         sleep(1)
#
#         # 批量修改输入框
#         self.item.batch_modify_input(self.all_input_edit_xpath_list, text_str)
#         self.item.batch_modify_input(all_date_edit_xpath_list, date_str)
#
#         sleep(1)
#         # 点击确定
#         self.item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
#         sleep(1)
#         # 选中刚刚编辑的数据行
#         self.item.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
#         # 点击编辑按钮
#         self.item.click_edi_button()
#         sleep(1)
#         # 批量获取输入框的value
#         input_values = self.item.batch_acquisition_input(self.all_input_edit_xpath_list, text_str)
#         input_values2 = self.item.batch_acquisition_input(self.all_date_edit_xpath_list, date_str)
#         sleep(1)
#         assert (
#             len(self.all_input_edit_xpath_list) == len(input_values) and
#             len(self.all_date_edit_xpath_list) == len(input_values2)
#         )
#         assert not self.item.has_fail_message()
#
#     @allure.story("删除测试数据成功")
#     # @pytest.mark.run(order=1)
#     def test_item_delsuccess2(self, login_to_item):
#
#         # 定位内容为‘111’的行
#         self.item.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
#         self.item.click_del_button()  # 点击删除
#         sleep(1)
#         # 点击确定
#         # 找到共同的父元素
#         parent = self.item.get_find_element_class("ivu-modal-confirm-footer")
#
#         # 获取所有button子元素
#         all_buttons = parent.find_elements(By.TAG_NAME, "button")
#
#         # 选择需要的button 第二个确定按钮
#         second_button = all_buttons[1]
#         second_button.click()
#         self.item.click_ref_button()
#         sleep(1)
#         # 定位内容为‘111’的行
#         itemdata = self.driver.find_elements(
#             By.XPATH, '//tr[./td[2][.//span[text()="111"]]]/td[2]'
#         )
#         assert len(itemdata) == 0
#         assert not self.item.has_fail_message()
#
#     @allure.story("过滤刷新成功")
#     # @pytest.mark.run(order=1)
#     def test_item_refreshsuccess(self, login_to_item):
#
#         filter_results = self.item.filter_method('//span[text()=" 主料号"]/ancestor::div[3]//span//span//span')
#         print('filter_results', filter_results)
#         assert filter_results
#         assert not self.item.has_fail_message()
#
#     @allure.story("新增全部数据测试")
#     # @pytest.mark.run(order=1)
#     def test_item_add_success(self, login_to_item):
#         # 输入框要修改的值
#         text_str = "111"
#         # 日期要修改的值
#         date_str = "2025/07/17 00:00:00"
#         self.item.click_add_button()  # 点击添加
#         sleep(1)
#
#         # 批量修改输入框
#         self.item.batch_modify_input(self.all_input_add_xpath_list, text_str)
#         # 批量修改日期
#         self.item.batch_modify_input(self.all_date_add_xpath_list, date_str)
#
#         sleep(1)
#         # 点击确定
#         self.item.click_button('(//button[@type="button"]/span[text()="确定"])[4]')
#         sleep(1)
#         # 选中物料代码
#         self.item.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
#         # 点击编辑按钮
#         self.item.click_edi_button()
#         sleep(1)
#         # 批量获取输入框的value
#         input_values = self.item.batch_acquisition_input(self.all_input_edit_xpath_list, text_str)
#         # 批量获取日期的value
#         date_values = self.item.batch_acquisition_input(self.all_date_edit_xpath_list, date_str)
#         sleep(1)
#         assert (
#                 len(self.all_input_add_xpath_list) == len(input_values)
#                 and len(self.all_date_add_xpath_list) == len(date_values)
#         )
#         assert not self.item.has_fail_message()
#
#     @allure.story("查询测试数据成功")
#     # @pytest.mark.run(order=1)
#     def test_item_selectcodesuccess(self, login_to_item):
#         driver = login_to_item  # WebDriver 实例
#         item = WarehouseLocationPage(driver)  # 用 driver 初始化 ItemPage
#
#         # 点击查询
#         item.click_sel_button()
#         sleep(1)
#         # 定位名称输入框
#         element_to_double_click = driver.find_element(
#             By.XPATH,
#             '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[4]',
#         )
#         # 创建一个 ActionChains 对象
#         actions = ActionChains(driver)
#         # 双击命令
#         actions.double_click(element_to_double_click).perform()
#         sleep(1)
#         # 点击工厂代码
#         item.click_button('//div[text()="主料号" and contains(@optid,"opt_")]')
#         sleep(1)
#         # 点击比较关系框
#         item.click_button(
#             '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
#         )
#         sleep(1)
#         # 点击=
#         item.click_button('//div[text()="=" and contains(@optid,"opt_")]')
#         sleep(1)
#         # 点击输入数值
#         item.enter_texts(
#             '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
#             "111",
#         )
#         sleep(1)
#
#         # 点击确认
#         item.click_button(
#             '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[2]'
#         )
#         sleep(1)
#         # 定位第一行是否为产品A
#         itemcode = item.get_find_element_xpath(
#             '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]'
#         ).text
#         # 定位第二行没有数据
#         itemcode2 = driver.find_elements(
#             By.XPATH,
#             '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][2]/td[2]',
#         )
#         assert itemcode == "111" and len(itemcode2) == 0
#         assert not item.has_fail_message()
#
#     @allure.story("没有数据时显示正常")
#     # @pytest.mark.run(order=1)
#     def test_item_selectnodatasuccess(self, login_to_item):
#
#         # 点击查询
#         self.item.click_sel_button()
#         sleep(1)
#         # 定位名称输入框
#         element_to_double_click = self.driver.find_element(
#             By.XPATH,
#             '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[4]',
#         )
#         # 创建一个 ActionChains 对象
#         actions = ActionChains(self.driver)
#         # 双击命令
#         actions.double_click(element_to_double_click).perform()
#         sleep(1)
#         # 点击交付单号
#         self.item.click_button('//div[text()="主料号" and contains(@optid,"opt_")]')
#         sleep(1)
#         # 点击比较关系框
#         self.item.click_button(
#             '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[5]//input'
#         )
#         sleep(1)
#         # 点击=
#         self.item.click_button('//div[text()="=" and contains(@optid,"opt_")]')
#         sleep(1)
#         # 点击输入数值
#         self.item.enter_texts(
#             '(//div[@class="vxe-table--render-wrapper"])[3]/div[1]/div[2]//tr[1]/td[6]//input',
#             "没有数据",
#         )
#         sleep(1)
#
#         # 点击确认
#         self.item.click_button(
#             '(//button[@class="ivu-btn ivu-btn-primary"]/span[text()="确定"])[2]'
#         )
#         sleep(1)
#         itemcode = self.driver.find_elements(
#             By.XPATH,
#             '(//table[contains(@class, "vxe-table--body")])[2]//tr[@class="vxe-body--row"][1]/td[2]',
#         )
#         assert len(itemcode) == 0
#         assert not self.item.has_fail_message()
#
#     @allure.story("删除数据成功")
#     # @pytest.mark.run(order=1)
#     def test_item_delsuccess3(self, login_to_item):
#         # 定位内容为‘111’的行
#         self.item.click_button('//tr[./td[2][.//span[text()="111"]]]/td[2]')
#         self.item.click_del_button()  # 点击删除
#         sleep(1)
#         # 点击确定
#         # 找到共同的父元素
#         parent = self.item.get_find_element_class("ivu-modal-confirm-footer")
#
#         # 获取所有button子元素
#         all_buttons = parent.find_elements(By.TAG_NAME, "button")
#
#         # 选择需要的button 第二个确定按钮
#         second_button = all_buttons[1]
#         second_button.click()
#         self.item.click_ref_button()
#         sleep(1)
#         # 定位内容为‘111’的行
#         itemdata = self.driver.find_elements(
#             By.XPATH, '//tr[./td[2][.//span[text()="111"]]]/td[2]'
#         )
#         assert len(itemdata) == 0
#         assert not self.item.has_fail_message()
