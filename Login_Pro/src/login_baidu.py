#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import time
from selenium import webdriver

def login_yibu(url):
    print('开始解析高考网网页 start...')

    username = "凌烟阁主人"
    passwd = "ljf674361437"

    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"')

    driver = webdriver.Chrome(
        executable_path=r"G:\work\Login_Pro\src\drive2\chromedriver.exe",
        chrome_options=options
    )
    # driver.maximize_window()
    driver.set_page_load_timeout(20)
    log_dir = 'https://login.bce.baidu.com/?fromai=1&redirect=https%3A%2F%2Faistudio.baidu.com%2Faistudio%2Findex'
    driver.get(log_dir)
    print(driver.page_source)  # 打印网页源代码
    time.sleep(2)
    log_sele = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__footerULoginBtn"]/img')
    if log_sele:
        log_sele.click()
    driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__userName"]').send_keys(username)
    elem2 = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__password"]')
    elem2.send_keys(passwd)
    time.sleep(5)
    elem = driver.find_element_by_xpath('//*[@id="TANGRAM__PSP_4__submit"]')
    elem.click()
    print('成功登录 login success')
    time.sleep(2)

    info_page = driver.find_element_by_xpath('//*[@id="main"]/div[1]/div[1]/div[1]/div/div[1]/div[3]')
    info_page.click()
    first_class = driver.find_element_by_xpath('//*[@id="main"]/header/div/a[2]')
    first_class.click()
    # my_pro = driver.find_element_by_xpath('//*[@id="tab-private"]')
    # my_pro.click()
    # my_pro1 = driver.find_element_by_xpath('//*[@id="main"]/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[1]/a/div[1]/span[1]')
    # my_pro1.click()
    # time.sleep(5)
    # start_pro = driver.find_element_by_xpath('//*[@id="main"]/div[1]/div[2]/div[2]/div/div/div[1]/div[1]/div/button[1]/span')
    # start_pro.click()
    #
    # enter = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/div[3]/button[1]/span')
    # enter.click()
    return driver


if __name__ =='__main__':
    login_yibu('ss')