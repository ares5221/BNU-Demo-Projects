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
    website_url = 'http://www.bzrzy.cn/bbs/boards.asp?assort=2'
    save_path = os.path.join(root_path, 'bzrzy')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if True:
        crawl_bzrzy_page(website_url, save_path)
        print('已经爬取目标网站的所有资源并保存', website_url, '\n\n')


def crawl_bzrzy_page(url,target_path):
    root_url = 'http://www.bzrzy.cn/bbs/'
    try:
        response = requests.get(url, headers=headers)
        # print(response.status_code)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        # 教育大家谈模块全部子模块
        jiaoyudajiatan = soup.find_all('table', {'class': 'tablebox_sim'})
        for table in jiaoyudajiatan:
            # 对当前节点前面的标签和字符串进行查找
            sub_modules = table.find_all('div', {'class': 'oneline forumname'})
            for sub_module in sub_modules:
                sub_module_name = sub_module.text
                sub_module_name = sub_module_name.replace(' ', '').replace('\n','')
                sub_module_href = sub_module.find_all('a')[0].get('href')
                crawl_sub_page(target_path,sub_module_name, root_url, sub_module_href)
    except Exception as e:
        print(e)
        print('获取教育大家谈模块信息失败，请检查网址信息、useragent等')


def crawl_sub_page(target_path, sub_module_name, root_url, sub_module_href):
    curr_path = os.path.join(target_path,sub_module_name)
    if not os.path.exists(curr_path):
        os.makedirs(curr_path)
    curr_url = root_url + sub_module_href
    print(curr_url)
    try:
        response = requests.get(curr_url, headers=headers)
        # print(response.status_code)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        # 获取页面个数信息
        page_nums = soup.find_all('div', class_='j_page')
        count = 0
        for nums in page_nums:
            num = nums.find_all('a')[-1].text
            if num == '下页':
                num = nums.find_all('a')[-2].text[3:]
                num = int(num)
            else:
                num = int(num)
            # print(num)
            count +=1
            if count >0:
                break
        for page_idx in range(1,num):
            single_page_url = curr_url + '&page=' + str(page_idx)
            crawl_page(curr_path, single_page_url)

    except Exception as e:
        print(e)
        print('获取子模块信息失败，请检查网址信息、useragent等')


def crawl_page(curr_path, single_page_url):
    print(curr_path, single_page_url)
    try:
        response = requests.get(single_page_url, headers=headers)
        # print(response.status_code)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 获取页面所有帖子信息title及url
        titles = soup.find_all('tr', class_='b_list')

        base_url = 'http://www.bzrzy.cn/bbs'

        for title in titles:
            name = title.find_all('span',class_='word-break-all')[0].text
            tmp_url = title.find_all('span',class_='word-break-all')[0].find_all('a')[0].get('href')

            curr_url = base_url + tmp_url[2:]
            page_content = get_content(curr_url)
            file_name = str(uuid.uuid1()) + '-' + name + '.txt'
            save_path = os.path.join(curr_path, file_name)
            save_post(save_path,page_content)
    except Exception as e:
        print(e)
        print('获取子模块每个网页信息失败，请检查网址信息、useragent等')


def get_content(url):
    # print(url)
    try:
        response = requests.get(url, headers=headers)
        # print(response.status_code)
        soup = BeautifulSoup(response.text, 'html.parser')
        bbs_posts = soup.find_all('div', class_='anc_table_div')
        post_list = []
        for post in bbs_posts:
            part1s = post.find_all('td',class_='tdright a_topiccontent')
            for part1 in part1s:
                part2s = part1.find_all('div',class_='a_content')
                for part2 in part2s:
                    part3s = part2.find_all('div',class_='word-break-all')
                    for part3 in part3s:
                        part4s = part3.text
                        # 正则表达式去掉所有标签
                        pattern = r'\[[a-zA-Z0-9-=(),/ .:_等线#宋体&%$#@!^*"仿黑楷微软雅]+\]'
                        html_label_pattern = re.compile(pattern)
                        # print(html_label_pattern.findall(part4s))  # 查看下匹配到什么
                        content = re.sub(html_label_pattern, "", part4s)
                        post_list.append(content)
                        post_list.append('\n\n')

        print('本帖子中全部内容为：', post_list)
        time.sleep(0.5)# 每爬完一页休眠0.5s，防止频繁访问
    except Exception as e:
        print(e)
        print('获取网页信息失败，请检查网址信息、useragent等')
    return post_list


def save_post(path, data_list):
    with open(path,'a',encoding='utf-8') as f_write:
        for post_content in data_list:
            f_write.write(post_content)


if __name__ == '__main__':
    main()