#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
def login_yibu():
    print('开始解析yibu网页 start...')

    username = "674361437@qq.com"
    passwd = "18734825221Liu."

    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"')

    driver = webdriver.Chrome(
        executable_path=r"G:\work\Login_Pro\src\drive3\chromedriver.exe",
        chrome_options=options
    )
    # driver.maximize_window()
    driver.set_page_load_timeout(20)
    log_dir = 'https://sso.ptpress.cn/login?pubAppId=0718A6B0&lg=1&service=https%3A%2F%2Fwww.epubit.com%2Fpubcloud%2Fsystem%2Fcallback%3F_client%3Dcas%26redirect%3Dhttps%253A%252F%252Fwww.epubit.com%252F&pubAppId=0718A6B0'
    driver.get(log_dir)
    print(driver.page_source)  # 打印网页源代码
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)
    elem2 = driver.find_element_by_xpath('//*[@id="password"]')
    elem2.send_keys(passwd)
    time.sleep(3)
    elem = driver.find_element_by_xpath('//*[@id="passwordLoginBtn"]')
    elem.click()
    print('成功登录 login success')
    # 点击签到
    info_page = driver.find_element_by_xpath('//*[@id="entry"]/div[1]/nav/div[2]/div[4]')
    info_page.click()
    # 点击图书
    # info = driver.find_element_by_xpath('//*[@id="entry"]/div[1]/nav/div[1]/ul/li[3]/div/span')
    # info.click()
    # 点击固定位置的书籍信息
    ActionChains(driver).move_by_offset(186, 261).click().perform()  # 鼠标左键点击， 200为x坐标， 100为y坐标
    # ActionChains(dr).move_by_offset(200, 100).context_click().perform()  # 鼠标右键点击
    print('ss')
    time.sleep(2)
    return driver

def login_yibu_dear():
    print('开始解析yibu网页 start...')

    username = "18734806395"
    passwd = "674361437Liu"

    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"')

    driver = webdriver.Chrome(
        executable_path=r"G:\work\Login_Pro\src\drive3\chromedriver.exe",
        chrome_options=options
    )
    # driver.maximize_window()
    driver.set_page_load_timeout(20)
    log_dir = 'https://sso.ptpress.cn/login?pubAppId=0718A6B0&lg=1&service=https%3A%2F%2Fwww.epubit.com%2Fpubcloud%2Fsystem%2Fcallback%3F_client%3Dcas%26redirect%3Dhttps%253A%252F%252Fwww.epubit.com%252F&pubAppId=0718A6B0'
    driver.get(log_dir)
    print(driver.page_source)  # 打印网页源代码
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)
    elem2 = driver.find_element_by_xpath('//*[@id="password"]')
    elem2.send_keys(passwd)
    time.sleep(3)
    elem = driver.find_element_by_xpath('//*[@id="passwordLoginBtn"]')
    elem.click()
    print('成功登录 login success')
    # 点击签到
    info_page = driver.find_element_by_xpath('//*[@id="entry"]/div[1]/nav/div[2]/div[4]')
    info_page.click()
    # 点击图书
    # info = driver.find_element_by_xpath('//*[@id="entry"]/div[1]/nav/div[1]/ul/li[3]/div/span')
    # info.click()
    # 点击固定位置的书籍信息
    ActionChains(driver).move_by_offset(186, 261).click().perform()  # 鼠标左键点击， 200为x坐标， 100为y坐标
    # ActionChains(dr).move_by_offset(200, 100).context_click().perform()  # 鼠标右键点击
    print('ss')
    time.sleep(2)
    return driver


if __name__ =='__main__':
    login_yibu()
    login_yibu_dear()