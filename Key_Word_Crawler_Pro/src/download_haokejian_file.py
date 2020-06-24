#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import requests
from bs4 import BeautifulSoup
import time
import random
from download_file import download_file_use_middle_website
from download_file import download_good_kejian_middle_website
from utils import save_supplement_data
from urllib.parse import quote


def download_haokejian_page(search_key, base_url):
    print('开始解析haokejian start...')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',

    }
    ss = quote(search_key, encoding='GBK')
    url = base_url + ss
    print(url)

    response = requests.get(url, headers=headers)
    web_page = response.content
    soup = BeautifulSoup(web_page, 'html.parser')  # 使用python默认的解析器
    page_num_list = 1
    if page_num_list == 1:
        print('当前关键字在好课件上的资源搜索结果仅有一页资源,start download', search_key, page_num_list)
        download_page(soup, search_key)
    else:
        print('当前关键字在好课件上上的资源搜索结果有多页，逐页爬取', search_key, page_num_list)
        for page_idx in page_num_list:
            curr_page = 'http://tiku.gaokao.com/search/type0/' + search_key + '/pg' + page_idx + '0'
            # print(curr_page)
            download_next_page(curr_page, search_key)
            sleep_time = max(0.1, 1 + random.random() * 1 if (random.random() > 0.5) else -1)
            time.sleep(sleep_time)
        print('好课件上关于该关键词 ', search_key, ' 的相关资源已经获取结束！！！')
    print('好课件上文件下载结束...')
    return


def download_next_page(url, search_key):
    response = requests.get(url)
    web_page = response.content
    soup = BeautifulSoup(web_page, 'html.parser')  # 使用python默认的解析器
    download_page(soup, search_key)


def download_page(soup, search_key):
    is_have_search_result = False
    res = soup.find_all('div', class_='list_soft')
    if len(res) > 0:
        is_have_search_result = True
    else:
        print('好课件上没有找到该关键字 --->', search_key, ' <---相关的资源。请注意检查！！！')
    if is_have_search_result:
        curr_titles = []
        curr_middle_websites = []
        curr_introduction_contents = []
        print('get 好课件上 title & middle_website & introduction INFO')
        titles = soup.find_all('div', class_='list_soft')  # download_url = soup.find_all('a')
        url_base = 'http://www.goodkejian.com/'
        for title in titles:
            for ss in title.find_all('span', class_='soft_name'):
                curr_titles.append(ss.get_text().replace(' ', ''))
                for a in ss.find_all('a', href=True):
                    if a.get_text(strip=True):
                        # print(a['href'])
                        curr_middle_websites.append(url_base + a['href'])
        # print(curr_titles, curr_middle_websites)
        '''
        # 保存爬取的文件名简介等信息，暂时先不打开
        # save_supplement_data(search_key, curr_titles, curr_middle_websites, curr_introduction_contents)
        '''
        # 下载文件
        download_good_kejian_middle_website(search_key, curr_titles, curr_middle_websites)
        return
