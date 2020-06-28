#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from bs4 import BeautifulSoup
import requests
import os
import re
import uuid
import time


root_path = './../../../../raw_data/scrapy_data'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

def main():
    website_url = 'http://www.seewww.cn'
    save_path = os.path.join(root_path, 'seewww/part1')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if True:
        crawl_seewww_page(website_url, save_path)
        print('已经爬取目标网站的所有资源并保存', website_url, '\n\n')


def crawl_seewww_page(url,target_path):
    try:
        response = requests.get(url, headers=headers)
        # print(response.status_code)
        response.encoding = 'GBK'
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        # 导航栏 内容
        navigation_bar = soup.find_all('div', class_='provin_nv')
        for table in navigation_bar:
            navigation = table.find_all('a')
            for tmp in navigation:
                module_name = tmp.text
                module_href = tmp.get('href')
                # print(module_name,module_href)
                if module_name in ['招生培训','招聘教师','投稿']:
                    break
                crawl_sub_page(target_path,module_name, url, module_href)
    except Exception as e:
        print(e)
        print('获取导航栏信息失败，请检查网址信息、useragent等')


def crawl_sub_page(target_path,module_name, url, module_href):
    curr_path = os.path.join(target_path,module_name)
    if not os.path.exists(curr_path):
        os.makedirs(curr_path)
    curr_url = url + module_href
    print(curr_url)
    try:
        response = requests.get(curr_url, headers=headers)
        response.encoding = 'GBK'
        # print(response.status_code)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        # 获取页面个数信息
        page_nums = soup.find_all('div', id='pagenav')
        count = 0
        for nums in page_nums:
            num = nums.text.split(' ')[0].split('/')[1].split(' ')[0]
            num = int(num)
            count +=1
            if count >0:
                break
        for page_idx in range(1,num):
            if page_idx <2:
                single_page_url = curr_url + 'index.html'
            else:
                single_page_url = curr_url + 'index_' + str(page_idx) + '.html'
            crawl_page(curr_path, single_page_url)

    except Exception as e:
        print(e)
        print('获取子模块信息失败，请检查网址信息、useragent等')


def crawl_page(curr_path, single_page_url):
    # print(curr_path, single_page_url)
    try:
        response = requests.get(single_page_url, headers=headers)
        response.encoding = 'GBK'
        soup = BeautifulSoup(response.text, 'html.parser')
        # 获取页面所有帖子信息title及url
        titles = soup.find_all('ul', class_='ul_list14')

        for title in titles:
            for li in title.find_all('li'):
                name = li.text
                tmp_url = li.find_all('a')[0].get('href')
                page_content = get_content(tmp_url)
                file_name = str(uuid.uuid1()) + '-' + name + '.txt'
                save_path = os.path.join(curr_path, file_name)
                save_post(save_path,page_content)
    except Exception as e:
        print(e)
        print('获取子模块每个网页信息失败，请检查网址信息、useragent等')


def get_content(url):
    print(url)
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'GBK'
        soup = BeautifulSoup(response.text, 'html.parser')
        content_list = []
        level_1s = soup.find_all('div', id='mcontent',class_='page_wz')
        for level_1 in level_1s:
            # divs = level_1.find_all('div')
            # for content in divs:
            #     content_list.append(content.text)
            articles = level_1.find_all('p')
            for content in articles:
                curr_content = content.text
                pattern = r"function(.+?)\n(.+?)\n(.+?)\n(.+?)\n(.+?)\n}"
                html_label_pattern = re.compile(pattern)
                # print('222',html_label_pattern.findall(curr_content))  # 对于读取到的js代码通过正则去除
                if html_label_pattern.findall(curr_content):
                    break
                else:
                    content_list.append(curr_content)
        print('本帖子中全部内容为：', content_list)
        time.sleep(0.5)# 每爬完一页休眠0.5s，防止频繁访问
    except Exception as e:
        print(e)
        print('获取网页信息失败，请检查网址信息、useragent等')
    return content_list


def save_post(path, data_list):
    with open(path,'a',encoding='utf-8') as f_write:
        for post_content in data_list:
            f_write.write(post_content)


if __name__ == '__main__':
    main()