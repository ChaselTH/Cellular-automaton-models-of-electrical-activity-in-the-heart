from selenium import webdriver
import time
import csv

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
time.sleep(5)

# 访问二叉树页面
driver.get("https://www.atomy.com/tw/Home/MyAtomy/GroupTree")

# 点击查找按钮
find_button = driver.find_element(by='xpath', value='//a[@href="javascript:srchDisplay();"]/img')
find_button.click()
alert = driver.switch_to.alert
alert.accept()

# 等待页面加载完成
time.sleep(5)

# 获取所有成员信息
members = []
member_rows = driver.find_elements(by='xpath', value="//div[@class='table']/div[@class='table-row']")
for member_row in member_rows:
    member_info = member_row.text.split('\n')
    members.append(member_info)

# 将成员信息写入 CSV 文件
with open('members.csv', mode='w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['姓名', 'ID', '直推人数', '开通日期'])
    for member in members:
        writer.writerow(member)

# 关闭浏览器
driver.quit()
