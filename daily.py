import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd


def daily(usr, pw):
    fail = False
    checkpoint = time.time()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)

    # 打开网页
    url = "https://gipr.meet48.xyz/#/task"
    browser.get(url)

    # 等待登录按钮可点击
    login_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '(//div[contains(text(), "登录")])[1]')))
    login_button.click()

    # 等待用户名输入框可见
    username_input = browser.find_element_by_xpath('//div[contains(@class, "style_inputBox__pytTH")][1]//input')
    username_input.send_keys(usr)

    password_input = browser.find_element_by_xpath('//div[contains(@class, "style_inputBox__pytTH")][2]//input')
    password_input.send_keys(pw)

    time.sleep(5)
    try:
        login_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "style_btn__VEzut"))
        )
        login_button.click()
    except:
        with open("daily_fail.txt","a") as file:
            file.write(usr+"\n")
            print("登录失败")


    print("用户: %s" % usr)

    time.sleep(3)
    # 每日登录
    print("开始领取每日奖励")
    try:
        daily_login = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '(//div[contains(text(), "网站-每日登录")])')))
        daily_login.click()
        time.sleep(1)

        claim_reward = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '(//div[contains(text(), "领取奖励")])')))
        claim_reward.click()
        print("每日登录领取成功")
    except:
        fail = True
        with open("daily_fail.txt","a") as file:
            file.write(usr+"\n")
        print("每日登录领取失败")
    time.sleep(7)



    # 随机小测验 点开答题网页准备答题
    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '(//div[contains(text(), "每日随机小测验")])'))).click()
        time.sleep(2)
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '(//div[contains(text(), "开始答题")])'))).click()
        time.sleep(3)

        print("开始答题")

        df = mk_df()
        time.sleep(2)
        # 开始答题 全选C
        for i in range(5):
            element = browser.find_element_by_xpath('//div[contains(@class, "style_question__MULj1")]//div[@class="style_title__cMEku"]')
            question = element.text
            print(question)

            try:
                answer = constract_ques(df, question)
                print(answer)
                answer_xpath = f"//div[@class='style_text__UG4zk' and @title='{answer}']"
                time.sleep(1)
                browser.find_element_by_xpath(answer_xpath).click()
            except:
                print("找不到答案")
                options_elements = browser.find_elements_by_class_name("style_text__UG4zk")
                options = [element.text for element in options_elements]
                browser.find_element_by_xpath('//div[contains(@class, "style_answer__F5PHw")][2]').click()
                with open("questionlist.txt", "a") as file:
                    file.write("问题：%s\n 答案: %s \n A:%s B:%s C:%s\n" % (question,answer,options[0],options[1],options[2]))

            time.sleep(3)
            WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "style_nextBtn__Zefsz"))
            ).click()
            time.sleep(1)

        time.sleep(3)
        claim_reward = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '(//div[contains(text(), "领取奖励")])')))
        claim_reward.click()
        print("答题领取成功")
    except:
        if fail == False:
            with open("daily_fail.txt","a") as file:
                file.write(usr+"\n")
            print("答题领取失败")


    time.sleep(3)
    browser.quit()

    if fail == False:
        with open("daily_success.txt","a") as file:
            file.write(usr+"\n")

    print("用户: %s 已登出" % usr)
    checkpoint2=time.time()
    print("此用户时间: %s秒" % ((checkpoint2 - checkpoint)))


def mk_df():
    file_path = '1.xlsx'
    df = pd.read_excel(file_path,dtype={'身高': str, '生日': str})
    df = df.dropna()
    return df


def constract_ques(df,question_text):
    matching_columns = [col for col in df.columns if col in question_text]
    if matching_columns:
        matching_column = matching_columns[0]
        matching_rows = df[df['姓名'].apply(lambda x: x in question_text)]

        if not matching_rows.empty:
            row_index = matching_rows.index[0]
            extracted_content = df.loc[row_index, matching_column]

    return extracted_content



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