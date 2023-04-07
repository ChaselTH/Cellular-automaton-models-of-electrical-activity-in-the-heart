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

search_id = "16840189"
notFound = True
# 获取所有成员信息
lines = driver.find_elements(by='xpath', value="//img[contains(@src, 'dot_03.gif')]")
member_rows = driver.find_elements(by='xpath', value="//table[contains(@id, 't') and translate(substring-after(@id, 't'), '0123456789', '') = '']")
for member_row in member_rows:
    member_info = member_row.text.split('\n')
    member_id = re.findall(r'\d+', member_info[0])[0]
    print(member_info)
    if member_id == search_id:
        action_chains = ActionChains(driver)
        action_chains.double_click(member_row).perform()
        notFound = False
        break

#if notFound:



time.sleep(1)

# 关闭浏览器
input("按 Enter 键退出...")