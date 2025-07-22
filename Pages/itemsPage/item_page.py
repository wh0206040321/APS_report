from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.base_page import BasePage


class ItemPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)  # 调用基类构造函数

    def click_add_button(self):
        """点击添加按钮."""
        self.click(By.XPATH, '//p[text()="新增"]')

    def click_edi_button(self):
        """点击修改按钮."""
        self.click(By.XPATH, '//p[text()="编辑"]')

    def click_del_button(self):
        """点击删除按钮."""
        self.click(By.XPATH, '//p[text()="删除"]')

    def click_sel_button(self):
        """点击查询按钮."""
        self.click(By.XPATH, '//p[text()="查询"]')

    def click_ref_button(self):
        """点击刷新按钮."""
        self.click(By.XPATH, '//p[text()="刷新"]')

    def enter_texts(self, xpath, text):
        """输入文字."""
        self.enter_text(By.XPATH, xpath, text)

    def click_button(self, xpath):
        """点击按钮."""
        self.click(By.XPATH, xpath)

    def go_item(self):
        """前往物料页面,deleteteststart.py和start.py页面使用"""
        self.click_button('(//span[text()="计划管理"])[1]')  # 点击计划管理
        self.click_button('(//span[text()="计划基础数据"])[1]')  # 点击计划基础数据
        self.click_button('(//span[text()="物品"])[1]')  # 点击物品

    def add_item(self, material_code, material_name):
        """添加物料信息.start.py页面使用"""
        self.click_add_button()
        self.enter_texts(
            '(//label[text()="物料代码"])[1]/parent::div//input', material_code
        )
        self.enter_texts(
            '(//label[text()="物料名称"])[1]/parent::div//input', material_name
        )
        self.click_button('(//button[@type="button"]/span[text()="确定"])[4]')

    def delete_item(self, material_code):
        """删除物料信息."""
        # 定位内容为‘1测试A’的行
        self.click_button(
            f'(//span[text()="{material_code}"])[1]/ancestor::tr[1]/td[2]'
        )
        self.click_del_button()  # 点击删除
        # 点击确定
        # 找到共同的父元素
        parent = self.get_find_element_class("ivu-modal-confirm-footer")

        # 获取所有button子元素
        all_buttons = parent.find_elements(By.TAG_NAME, "button")

        # 选择需要的button 第二个确定按钮
        second_button = all_buttons[1]
        second_button.click()

    def check_item_exists(self, item_name):
        """检查物料是否存在."""
        try:
            self.get_find_element_xpath(f'//span[text()="{item_name}"]')
            return True
        except:
            return False

    def get_find_element_xpath(self, xpath):
        """获取用户头像元素，返回该元素。如果元素未找到，返回None。"""
        try:
            return self.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return None

    def get_find_element_class(self, classname):
        """获取用户头像元素，返回该元素。如果元素未找到，返回None。"""
        try:
            return self.find_element(By.CLASS_NAME, classname)
        except NoSuchElementException:
            return None

    def get_find_message(self):
        """获取错误信息"""
        message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="ivu-message"]//span')
            )
        )
        return message

    def add_layout(self, layout):
        """添加布局."""
        self.click_button('//div[@class="newDropdown"]//i')
        self.click_button('//li[text()="添加新布局"]')
        self.enter_texts(
            '//div[text()="当前布局:"]/following-sibling::div//input', f"{layout}"
        )
        checkbox1 = self.get_find_element_xpath(
            '//div[text()="是否默认启动:"]/following-sibling::label/span'
        )

        # 检查复选框是否未被选中
        if checkbox1.get_attribute("class") == "ivu-checkbox":
            # 如果未选中，则点击复选框进行选中
            self.click_button(
                '//div[text()="是否默认启动:"]/following-sibling::label/span'
            )
        sleep(1)

        self.click_button('(//div[text()=" 显示设置 "])[1]')
        # 获取是否可见选项的复选框元素
        checkbox2 = self.get_find_element_xpath(
            '(//div[./div[text()="是否可见:"]])[1]/label/span'
        )
        # 检查复选框是否未被选中
        if checkbox2.get_attribute("class") == "ivu-checkbox":
            # 如果未选中，则点击复选框进行选中
            self.click_button('(//div[./div[text()="是否可见:"]])[1]/label/span')
            # 点击确定按钮保存设置
            self.click_button('(//div[@class="demo-drawer-footer"])[3]/button[2]')
        else:
            # 如果已选中，直接点击确定按钮保存设置
            self.click_button('(//div[@class="demo-drawer-footer"])[3]/button[2]')

    def del_all(self, value=[]):
        for index, xpath in enumerate(value, start=1):
            try:
                self.click_button(f'//tr[./td[2][.//span[text()="{xpath}"]]]/td[2]')
                self.click_del_button()  # 点击删除
                sleep(1)
                # 点击确定
                # 找到共同的父元素
                parent = self.get_find_element_class("ivu-modal-confirm-footer")

                # 获取所有button子元素
                all_buttons = parent.find_elements(By.TAG_NAME, "button")

                # 选择需要的button 第二个确定按钮
                second_button = all_buttons[1]
                second_button.click()
                sleep(1)
            except NoSuchElementException:
                print(f"未找到元素: {xpath}")
            except Exception as e:
                print(f"操作 {xpath} 时出错: {str(e)}")

    def del_loyout(self, layout):
        # 获取目标 div 元素，这里的目标是具有特定文本的 div
        target_div = self.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]'
        )

        # 获取父容器下所有 div
        # 这一步是为了确定目标 div 在其父容器中的位置
        parent_div = self.get_find_element_xpath(
            f'//div[@class="tabsDivItemCon" and ./div[text()=" {layout} "]]'
        )
        all_children = parent_div.find_elements(By.XPATH, "./div")

        # 获取目标 div 的位置索引（从0开始）
        # 这里是为了后续操作，比如点击目标 div 相关的按钮
        index = all_children.index(target_div)
        print(f"目标 div 是第 {index + 1} 个 div")  # 输出 3（如果从0开始则是2）

        self.click_button(
            f'//div[@class="tabsDivItemCon"]/div[text()=" {layout} "]//i'
        )
        # 根据目标 div 的位置，点击对应的“删除布局”按钮
        self.click_button(f'(//li[text()="删除布局"])[{index + 1}]')
        sleep(2)
        # 点击确认删除的按钮
        self.click_button('//button[@class="ivu-btn ivu-btn-primary ivu-btn-large"]')