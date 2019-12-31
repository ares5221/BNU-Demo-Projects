#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import requests
from selenium import webdriver
import time
import os
import shutil
from bs4 import BeautifulSoup
import random
from utils import save_supplement_data


def download_xuekewang_page(search_key, base_url):
    url = base_url + search_key
    response = requests.get(url)
    print('开始解析学科网 关键字', search_key)
    if response.status_code == 200:
        print('学科网网页正常响应')
        loop_xuekewang_page(response, search_key)
    else:
        print('获取网页失败', response.status_code)
        return


def loop_xuekewang_page(response, search_key):
    is_get_search_result, page_num = judge_search_result(response)
    if is_get_search_result:
        # todo 学科网的搜索结果都是为300页，由于账户限制只能下载五个文件
        #  demo仅取第一页即可
        if page_num > 1:
            page_num = 2
        # 启动模拟浏览器
        driver = webdriver.Chrome(
            executable_path=r"G:/Download/Key_Word_Crower_Demo/src/drive/chromedriver.exe")
        # driver.maximize_window()
        driver.set_page_load_timeout(20)
        # 这里需要做登录验证
        is_login_success = False
        if not is_login_success:
            driver = login(driver)
            for page_index in range(1, page_num):
                source_url = 'http://search.zxxk.com/books/index-'
                curr_url = source_url + str(page_index) + '.html?level=1&kw=' + search_key
                print('获取学科网该关键字第一页的所有可下载的链接', curr_url)
                response = requests.get(curr_url)
                web_page = response.content
                soup = BeautifulSoup(web_page, 'html.parser')  # 使用python默认的解析器
                curr_titles = []
                curr_middle_websites = []
                curr_introduction_contents = []
                print('get 学科网title & middle_website & introduction')
                list_item = soup.find_all('div', class_="list-item clearfix")  # download_url = soup.find_all('a')
                for ls_item in list_item:
                    for mid_tmp in ls_item.find_all('div', class_='rebindsoftlist'):
                        for tmp in mid_tmp.find_all('a', class_='high_light'):
                            curr_titles.append(tmp.get_text().replace('\n', '').replace(' ', ''))
                            curr_middle_websites.append(tmp.get('href'))
                    for mid2_tmp in ls_item.find_all('ul', class_='attribute'):
                        for tmp2 in mid2_tmp.find_all('li', class_='jiaocai'):
                            curr_introduction_contents.append(tmp2.get_text().replace(' ', ''))
                '''
                # 保存爬取的信息
                # save_supplement_data(search_key, curr_titles, curr_middle_websites, curr_introduction_contents)
                '''
                print('开始下载学科网文件')
                download_xueke_file_use_middle_website(search_key, curr_titles, curr_middle_websites, driver)
        driver.close()
        print('学科网文件下载成功...')
        remove_xueke_file(search_key)
    else:
        # todo
        print('该关键字在学科网没有搜索结果', search_key)
    return


def judge_search_result(response):
    '''
    用来判断该关键词在学科网搜索结果是否存在，并返回搜索结果页面
    如果没有搜到结果则为False，0
    一般都有搜索结果, 最大页码300
    :param response:
    :return:
    '''
    web_page = response.content
    soup = BeautifulSoup(web_page, 'html.parser')  # 使用python默认的解析器
    pages_infos = soup.find_all('div', class_="list-page clearfix")  # download_url = soup.find_all('a')
    no_res = soup.find_all('div', class_="no-result-tips-wrap")
    page_num = 0
    for pi in pages_infos:
        hr = pi.find_all('span', class_="sun")
        for h in hr:
            page_num = int(h.get_text()[1:-1])  # 去除上一页 下一页的str
    print('获取到搜索页面为：', page_num)
    if page_num > 0:
        return True, page_num
    else:
        return False, 0


def remove_xueke_file(search_key):
    '''
    将文件从默认下载的路径剪切到data_v2/source/key_word/路径下
    :param search_key:
    :return:
    '''
    src_dir = r'C:\Users\12261\Downloads'
    base_dir = './../data_v2/source'
    tar_dir = os.path.join(base_dir, search_key)
    for fname in os.listdir(src_dir):
        curr_file_dir = os.path.join(src_dir, fname)
        curr_tar_dir = os.path.join(tar_dir, fname)
        if not os.path.exists(curr_tar_dir):
            shutil.move(curr_file_dir, curr_tar_dir)
        else:
            print('source/key_word/下已经存在该文件')
            del_dir = os.path.join('./../data_v2/backup', fname)
            shutil.move(curr_file_dir, del_dir)


def download_xueke_file_use_middle_website(search_key, titles, middle_websites, driver):
    # 这个网页是js操作的，只能用模拟操作
    # todo 学科网普通账户只能下载五个文件，因此只选前4个即可
    middle_websites = middle_websites[0:4]
    print('curr middle website', middle_websites)
    for curr_url in middle_websites:
        driver.get(curr_url)
        time.sleep(1)
        # label_list = driver.find_elements_by_link_text("下载")
        # label_list1 = driver.find_element_by_class_name("download")
        ls = driver.find_element_by_xpath('//*[@id="btnSoftDownload"]/div')
        driver.implicitly_wait(10)
        time.sleep(1)
        ls.click()
    return


def login(browser):
    # username = "18734825221"
    # passwd = "123456"
    # test account id passwd
    username = "18811766097"
    passwd = "123456"
    print('开始登录学科网')
    browser.get('https://sso.zxxk.com/login')
    browser.implicitly_wait(10)
    # 从默认二维码登录跳转到账号密码登录
    id_pass_login = browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/a')
    id_pass_login.click()
    time.sleep(1 + random.random())
    elem = browser.find_element_by_name("username")
    elem.send_keys(username)
    elem = browser.find_element_by_name("password")
    elem.send_keys(passwd)
    time.sleep(1)
    elem = browser.find_element_by_id("CommonLogin")
    elem.click()
    time.sleep(10)
    print('login success登录学科网成功')
    return browser


if __name__ == '__main__':
    url = ['http://www.zxxk.com/soft/11963073.html?spm=a1.b4.c3.d25']
    file_name = ['苏教版七年级生物上册第6章第5节光合作用和呼吸作用原理的应用(课件)(共21张PPT)']
    driver = webdriver.Chrome(
        executable_path=r"G:/Download/Key_Word_Crower_Demo/src/drive/chromedriver.exe")
    # driver.maximize_window()
    driver.set_page_load_timeout(20)
    driver = login(driver)
    download_xueke_file_use_middle_website('光合作用', file_name, url, driver)
