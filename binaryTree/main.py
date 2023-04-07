import re
from selenium import webdriver
from selenium.webdriver import ActionChains
import time

# 创建 Chrome 浏览器对象
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

# 访问登录页面
driver.get("https://www.atomy.com/tw/Home/Account/Login")

# 登录
username_input = driver.find_element(by='name', value='userId')
username_input.send_keys("16615263")
password_input = driver.find_element(by='name', value='userPw')
password_input.send_keys("16816888")
login_button = driver.find_element(by='xpath', value="//p[@class='logbtn']/a[@class='btnGlay6 pl16r34 fs16']")
login_button.click()

# 等待页面加载完成
time.sleep(1)

# 访问二叉树页面
driver.get("https://www.atomy.com/tw/Home/MyAtomy/GroupTree")

# 点击查找按钮
find_button = driver.find_element(by='xpath', value='//a[@href="javascript:srchDisplay();"]/img')
find_button.click()
alert = driver.switch_to.alert
alert.accept()

# 等待页面加载完成
time.sleep(1)


def is_endpoint(driver, member_row):
    # 获取当前成员节点的位置信息和大小信息
    member_location = member_row.location
    member_size = member_row.size

    # 计算出当前成员节点正下方的点的位置信息
    down_point = {'x': member_location['x'] + member_size['width'] / 2, 'y': member_location['y'] + member_size['height']}

    print(down_point)

    endpoint_down = driver.find_elements(by='xpath',
                                         value=f"//img[@src='https://static-global.atomy.com/tw/Resource/Home/Mall/img/dot_03.gif' and @style='position:absolute; width:3px; height:59px; @top>={down_point['y'] - 20} and @top<={down_point['y'] + 20} and @left>={down_point['x'] - 20} and @left<={down_point['x'] + 20}']")

    if len(endpoint_down) == 0:
        return True
    else:
        return False


def find_member(driver, search_id):
    # 先查找当前页面是否存在成员
    member_rows = driver.find_elements(by='xpath',
                                       value="//table[contains(@id, 't') and translate(substring-after(@id, 't'), '0123456789', '') = '']")
    for member_row in member_rows:
        member_info = member_row.text.split('\n')
        member_id = re.findall(r'\d+', member_info[0])[0]
        if member_id == search_id:
            action_chains = ActionChains(driver)
            action_chains.double_click(member_row).perform()
            return True

        time.sleep(1)
        if is_endpoint(driver, member_row):
            # 如果当前节点是端节点，则展开子节点
            action_chains = ActionChains(driver)
            action_chains.double_click(member_row).perform()
            if find_member(driver, search_id):
                return True

    # 如果所有节点都已经遍历完成还没有找到成员，则返回False
    return False


# 使用示例
search_id = "26601927"
find_member(driver, search_id)


time.sleep(1)

# 关闭浏览器
input("按 Enter 键退出...")
