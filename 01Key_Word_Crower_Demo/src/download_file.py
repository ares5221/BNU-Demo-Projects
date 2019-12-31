#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
import requests
import wget
import time
from bs4 import BeautifulSoup
import shutil

def download_with_requests(url, file_name):
    base_dir = './../test_func'
    save_path = os.path.join(base_dir, file_name)
    curr_time = time.strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists(save_path):
        ss = requests.get(url)
        with open(save_path, 'wb') as f:
            f.write(ss.content)
        print(file_name, ' 该文件下载完成 ', 'curr time----> :', curr_time)
    else:
        print(file_name, ' 文件已经存在 ', 'curr time----> :', curr_time)


def download_with_wget(file_name, url, key):
    '''
    直接将文件下载保存到data_v2/source/key/路径下
    :param file_name:
    :param url:
    :param key:
    :return:
    '''
    base_dir = './../data_v2/source'
    save_dir = os.path.join(base_dir, key)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # filename = wget.download(url, out=save_path) # 可以直接指定输出路径，但是不确定文件后缀类型
    filename = wget.download(url)  # 中文文件名会出现乱码，但是可以知道文件类型[tiku.gaokao.com]é«ä¿ç»ä¹ .doc
    suffix_type = '.' + filename.split('.')[-1]
    file_name += suffix_type
    save_path = os.path.join(save_dir, file_name)

    curr_time = time.strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists(save_path):
        os.rename(filename, save_path)
        print(file_name, ' 该文件下载完成 ', 'curr time----> :', curr_time)
    else:
        print(file_name, ' 文件已经存在 存储在backup', 'curr time----> :', curr_time)
        del_dir = os.path.join('./../data_v2/backup', filename)
        shutil.move(filename, del_dir)


def download_file_use_middle_website(search_key, titles, middle_websites):
    download_website = []
    if len(middle_websites) < 1:
        print('获取的中间网页信息有误，请查看网址')
        return
    for curr_url in middle_websites:
        response = requests.get(curr_url)
        web_page = response.content
        soup = BeautifulSoup(web_page, 'html.parser')
        download_info = soup.find_all('a', class_="download lm10 op8")
        for dlw in download_info:
            download_website.append(dlw.get('href'))
    print('真正开始下载高考网文件')
    for index in range(len(titles)):
        download_with_wget(titles[index], download_website[index], search_key)


if __name__ == '__main__':
    url = 'http://tiku.gaokao.com/download/type6/id7483'
    file_name = '高中生物必修1光合作用同步练习1.docx'
    # test this Func
    download_with_requests(url, file_name)
    # download_with_wget(url, file_name)
