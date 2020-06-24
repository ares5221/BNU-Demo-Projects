#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import requests
from bs4 import BeautifulSoup
import time
import random
from download_file import download_file_use_middle_website
from utils import save_supplement_data


def download_gaokaowang_page(search_key, base_url):
    print('开始解析高考网网页 start...')
    headers = {
        'user-agent': 'Mozilla/5.0'
    }
    url = base_url + search_key
    response = requests.get(url, headers=headers)
    # 1 get web page data
    web_page = response.content
    # 2 phrase web page data
    soup = BeautifulSoup(web_page, 'html.parser')  # 使用python默认的解析器
    # print(soup)
    next_page = soup.find_all('div', class_="page-b")
    # 存储该关键字搜索出现的搜索页码信息，是一个str的列表
    page_num_list = ['1']
    for np in next_page:
        for hr in np.find_all('a'):
            if hr.get_text().isdigit():
                page_num_list.append(hr.get_text())
    if len(page_num_list) == 1:
        print('当前关键字在高考网上的资源搜索结果仅有一页资源,start download', search_key, page_num_list)
        download_page(soup, search_key)
    else:
        print('当前关键字在高考网上的资源搜索结果有多页，逐页爬取', search_key, page_num_list)
        for page_idx in page_num_list:
            curr_page = 'http://tiku.gaokao.com/search/type0/' + search_key + '/pg' + page_idx + '0'
            # print(curr_page)
            download_next_page(curr_page, search_key)
            sleep_time = max(0.1, 1 + random.random() * 1 if (random.random() > 0.5) else -1)
            time.sleep(sleep_time)
        print('高考网关于该关键词 ', search_key, ' 的相关资源已经获取结束！！！')
    print('高考网文件下载结束...')
    return


def download_next_page(url, search_key):
    response = requests.get(url)
    web_page = response.content
    soup = BeautifulSoup(web_page, 'html.parser')  # 使用python默认的解析器
    download_page(soup, search_key)


def download_page(soup, search_key):
    is_have_search_result = False
    res = soup.find_all('article', class_="result-item")
    if len(res) > 0:
        is_have_search_result = True
    else:
        print('高考网没有找到该关键字 --->', search_key, ' <---相关的资源。请注意检查！！！')
    if is_have_search_result:
        curr_titles = []
        curr_middle_websites = []
        curr_introduction_contents = []
        print('get 高考网 title & middle_website & introduction INFO')
        titles = soup.find_all('a', class_="c-l2")  # download_url = soup.find_all('a')
        for title in titles:
            curr_titles.append(title.get_text().replace(' ', ''))
            curr_middle_websites.append(title.get('href'))
        introduction_contents = soup.find_all('p', class_="c-b6 ti2")
        for idc in introduction_contents:
            curr_introduction_contents.append(idc.get_text())
        '''
        # 保存爬取的文件名简介等信息，暂时先不打开
        # save_supplement_data(search_key, curr_titles, curr_middle_websites, curr_introduction_contents)
        '''
        # 下载文件
        print(curr_middle_websites)
        download_file_use_middle_website(search_key, curr_titles, curr_middle_websites)
        return
