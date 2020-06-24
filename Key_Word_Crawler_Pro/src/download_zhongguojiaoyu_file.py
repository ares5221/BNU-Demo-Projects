#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import shutil
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import random
import time
import os
from selenium import webdriver
from utils import save_supplement_data


def download_jiaoyu_page(search_key, base_url):
    url = base_url + search_key
    response = requests.get(url)
    print('开始解析中国教育网 关键字', search_key)
    if response.status_code == 200:
        print('中国教育网 网页正常响应')
        loop_jiaoyu_page(response, search_key)
    else:
        print('获取网页失败', response.status_code)
        return


def loop_jiaoyu_page(response, search_key):
    is_get_search_result, page_num = judge_jiaoyu_result(response)
    if is_get_search_result:
        # todo 中国教育网网的搜索结果都是为5页，时间限制demo只爬取第一页即可
        if page_num >= 1:
            page_num = 2
            download_jiaoyu_website(search_key, page_num)
    else:
        print('中国教育网网没有找到该关键字 --->', search_key, ' <---的相关资源。请注意检查！！！')
    return


def judge_jiaoyu_result(response):
    '''
    用来判断中国教育网得到的搜索结果是否存在，并返回搜索结果页面
    如果没有搜到结果则为False，0
    一般都有搜索结果, 最大页码300
    :param response:
    :return:
    '''
    web_page = response.content
    soup = BeautifulSoup(web_page, 'html.parser')  # 使用python默认的解析器
    pages_infos = soup.find_all('div', class_="fenye0 fn-m20")
    page_num = 0
    ss = []
    # print(pages_infos)
    if len(pages_infos) > 0:
        for pi in pages_infos:
            ss.append(pi.get_text())
        print(ss)
        if '2' in ss[0]:
            page_num = 2
        else:
            page_num = 1
        if page_num > 0:
            return True, page_num
    else:
        return False, 0


def download_jiaoyu_website(search_key, page_num):
    is_login_jiaoyu_web = False
    if not is_login_jiaoyu_web:
        driver = login_jiaoyu()
    ss = quote(search_key, encoding='gbk')  # 这个网站用的是GBK的编码方式，如果默认utf-8，则不会转换为正确的网址
    base_url = 'http://www.zzstep.com/xiaoxue/xiao_search.php?key='
    print('获取可下载的所有文件信息')
    for index in range(1, page_num):
        curr_url = base_url + ss + '&page=' + str(index)
        response = requests.get(curr_url)
        print(curr_url)
        web_page = response.content
        soup = BeautifulSoup(web_page, 'html.parser')  # 使用python默认的解析器
        curr_titles = []
        curr_middle_websites = []
        curr_introduction_contents = []

        print('获取中国教育网的下载资源的 title & middle_website & introduction')
        list_item = soup.find_all('li', class_="bg")
        for ls_item in list_item:
            curr_titles.append(ls_item.get_text())
            for a in ls_item.find_all('a', href=True):
                if a.get_text(strip=True):
                    print(a['href'])
                    curr_middle_websites.append( a['href'])

        # for mid2_tmp in ls_item.find_all('li', class_='info fn-mt20'):
        #     tmp_intro = []
        #     for tmp2 in mid2_tmp.find_all('div', class_='fn-left leibei fn-ml20'):
        #         # print(tmp2.get_text())
        #         tmp_intro.append(tmp2.get_text())
        #     curr_introduction_contents.append(tmp_intro)
        '''       
        # 保存爬取的信息
        # save_supplement_data(search_key, curr_titles, curr_middle_websites, curr_introduction_contents)
        '''
        print('真正下载中国教育网的文件资源')
        download_jiaoyu_file_use_middle_website_2(search_key, curr_titles, curr_middle_websites, driver)
    print('中国教育网的文件下载完成，开始存储文件到正确路径...')
    remove_xueke_file(search_key)


def login_jiaoyu():
    username = "ares5221"
    passwd = "123456"
    # 备用账号
    username1 = "674361437@qq.com"
    passwd1 = "123456"
    # username = "gaojingjian"
    # passwd = "123456"
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')

    driver = webdriver.Chrome(
        executable_path=r"G:\Download\Key_Word_Crawler_Pro\src\drive2\chromedriver.exe",
        chrome_options=options
    )
    # driver.maximize_window()
    driver.set_page_load_timeout(20)
    log_dir = 'http://www.zzstep.com/userlogin.php?refer=http%3A%2F%2Fwww.zzstep.com%2F'
    driver.get(log_dir)
    # print(driver.page_source)  # 打印网页源代码
    time.sleep(1)
    # todo 这里访问的是首页，需要手动点击切换到登录页面
    # log_ele = driver.find_element_by_xpath('//*[@id="login"]/span[1]/a')
    # log_ele.click()
    # driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)
    # 这个地方特别注意，在输入密码的时候，需要先点击以下输入框才可以
    elem2 = driver.find_element_by_xpath('//*[@id="txt"]')
    elem2.clear()
    elem2.click()
    elem2 = driver.find_element_by_xpath('//*[@id="pass"]')
    elem2.send_keys(passwd)
    time.sleep(1)
    elem = driver.find_element_by_id("submit1")
    elem.click()
    print('成功登录中国教育网 login success')
    time.sleep(1)
    return driver


def remove_xueke_file(search_key):
    src_dir = r'C:\Users\12261\Downloads'
    base_dir = './../crawler_data/source'
    tar_dir = os.path.join(base_dir, search_key)
    for fname in os.listdir(src_dir):
        curr_file_dir = os.path.join(src_dir, fname)
        curr_tar_dir = os.path.join(tar_dir, fname)
        if not os.path.exists(curr_tar_dir):
            shutil.move(curr_file_dir, curr_tar_dir)
        else:
            print('source/key_word/下已经存在该文件')
            del_dir = os.path.join('./../crawler_data/backup', fname)
            shutil.move(curr_file_dir, del_dir)


def download_jiaoyu_file_use_middle_website_2(search_key, titles, middle_websites, driver):
    time.sleep(1)
    # todo demo只下载前4个即可
    middle_websites = middle_websites[0:4]
    print(middle_websites)
    base_url = 'http://www.zzstep.com'
    driver.set_page_load_timeout(30)
    # driver.implicitly_wait(10)
    for midd_url in middle_websites:
        curr_url = base_url + midd_url
        driver.get(midd_url)
        # print(driver.page_source)  # 打印网页源代码
        ls = driver.find_element_by_class_name('actDown2')
        driver.implicitly_wait(10)
        ls.click()
        time.sleep(5)
    # driver.close()
    return


if __name__ == '__main__':
    url = ['/5274103-download.html']
    file_name = ['七年级生物上册3.4.1植物的光合作用随堂练习新版苏科版']
    download_jiaoyu_file_use_middle_website_2('光合作用', file_name, url)
