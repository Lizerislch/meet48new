import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import platform

#

os_name = platform.system()
if os_name == "Windows":
    from pywinauto.keyboard import send_keys
    import winsound


def daily(usr, pw):
    wallet = "0xc2cacd78d22613d3361f857bc440e23f2af274c9"
    checkpoint = time.time()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)

    # 打开网页
    url = "https://gipr.meet48.xyz/#/shop"
    browser.get(url)

    time.sleep(2)

    # 等待登录按钮可点击
    login_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '(//div[contains(text(), "登录")])[1]')))
    login_button.click()

    # 等待用户名输入框可见
    username_input = browser.find_element_by_xpath('//div[contains(@class, "style_inputBox__pytTH")][1]//input')
    username_input.send_keys(usr)

    password_input = browser.find_element_by_xpath('//div[contains(@class, "style_inputBox__pytTH")][2]//input')
    password_input.send_keys(pw)

    time.sleep(5)
    login_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "style_btn__VEzut"))
    )
    login_button.click()

    print("用户: %s" % usr)


    time.sleep(3)
    # 使用Selenium定位並獲取"PICK积分"元素
    pick_points_element = browser.find_element_by_xpath("//p[@class='style_point__7+4GA']")
    # 獲取"PICK积分"的數值
    pick_points = int(pick_points_element.text)
    print(pick_points)
    # 当pick point 大于20，兑换
    # 兑换结束转移棒子 输入地址
    while pick_points >= 20:
        exchange_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '(//div[contains(text(), "立即兑换")])[1]')))
        exchange_button.click()
        time.sleep(7)
        pick_points -= 20
        print("兑换成功！剩余积分: %s " % pick_points)

    browser.execute_script("window.scrollBy(0, -2000);")
    time.sleep(3)


    number_element = browser.find_element_by_xpath("(//div[@class='style_details__CizAH']/p[@class='style_point__7+4GA'])[2]")
    # 獲取數字文本
    number = int(number_element.text)
    print("打Call棒数量: %s" % number)

    if number > 0:
        transfer_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '(//div[contains(text(), "转移打Call棒")])')))
        transfer_button.click()

        time.sleep(2)

        # 使用XPath定位輸入框元素
        input_element = browser.find_element_by_xpath(
            "//input[@class='style_input__GghUy' and @placeholder='请输入您本次转移打Call棒的数量']")
        # 輸入數字
        input_element.send_keys(number)

        time.sleep(2)

        wallet_element = browser.find_element_by_xpath(
            "//input[@class='style_input__GghUy' and @placeholder='请输入您的BEP20测试链地址']")
        # 輸入數字
        wallet_element.send_keys(wallet)

        confirm_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '(//div[contains(text(), "确定")])')))
        confirm_button.click()

        print("转移成功")
        time.sleep(2)

    browser.quit()




def read_from_usrlist():
    start_time = time.time()
    file_path = 'daily.csv'  # Update with your CSV file path
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            usr = row.get('usr')
            pw = row.get('pw')
            daily(usr, pw)
            end_time = time.time()
            print("总用时: %s秒" % ((end_time - start_time)))



if __name__ == "__main__":
    read_from_usrlist()