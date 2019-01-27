# sagemakerにある推薦モデルをアップデートする
# sagemekerの起動を行う

import os
# ブラウザ操作
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def process():

    # ログイン画面の設定
    options = Options()
    options.binary_location = os.environ['BINARY_LOCATION']
    options.add_argument('--headless')
    driver = webdriver.Chrome('chromedriver', chrome_options=options)
    driver.get(os.environ['AWS_LOGIN_URL'])

    # ID/PASSでAWSにログイン
    id = driver.find_element_by_id("username")
    id.send_keys(os.environ['AWS_LOGIN_NAME'])
    password = driver.find_element_by_id("password")
    password.send_keys(os.environ['AWS_LOGIN_PASS'])
    time.sleep(1)
    login_button = driver.find_element_by_id("signin_button")
    login_button.click()

    # notebookの画面
    driver.get(os.environ['AWS_NOTEBOOK_URL'])
    time.sleep(20)
    run_all_cell = driver.find_element_by_xpath('//*[@id="run_int"]/button[4]')
    run_all_cell.click()
    time.sleep(5)

    # sagemaker実行
    restart_run = driver.find_element_by_xpath('/html/body/div[8]/div/div/div[3]/button[2]')
    restart_run.click()
    time.sleep(5)
    driver.quit()
